import io
import re
import zipfile

import altair as alt
import pandas as pd
import streamlit as st

from Backend.data import ACM_Data
from Backend.script import ACM_Script
from Backend.heat_calendar import plot_heatmap_matplotlib
from Backend import scraper

DEFAULT_NAME = "FIRST_NAME LAST_NAME"

# Sequential blue ramp (validated dataviz palette) — light->dark by class count.
HEATMAP_COLOR_RANGE = ["#cde2fb", "#0d366b"]
HOUR_TICKS = [f"{h:02d}:00" for h in range(5, 23)]


def default_script(name: str) -> str:
    return (
        "Greetings!\n\tI hope the start of the semester has been treating you well. "
        f"My name is {name} and I am the membership officer of the Association of Computer "
        "Machinery or ACM. If you haven't heard of ACM before we are a computer science "
        "organization that strives to help fellow students learn more about coding and "
        "programming through community, workshops, hackathons, and other events. As ACM's "
        "Open House approaches, we wanted to see if we could send a representative of ACM "
        "to very briefly present what ACM is about and our upcoming events for the semester. "
        "If your interested please let us know, and confirm if we have all the correct classes below."
    )


def safe_stem(label: str) -> str:
    stem = re.sub(r"\.csv$", "", label or "data", flags=re.IGNORECASE)
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", stem)


def set_raw_df(df: pd.DataFrame, label: str):
    st.session_state.raw_df = df
    st.session_state.source_label = label
    for key in ("signup_df", "scripts_zip", "scripts_count", "heatmap_data"):
        st.session_state.pop(key, None)


def init_state():
    st.session_state.setdefault("raw_df", None)
    st.session_state.setdefault("source_label", None)
    st.session_state.setdefault("presenter_name", DEFAULT_NAME)
    st.session_state.setdefault("script", default_script(DEFAULT_NAME))


def main():
    st.set_page_config(page_title="ACM Email Script", page_icon="📧", layout="wide")
    st.title("ACM Email Script")

    init_state()
    render_data_source_section()

    if st.session_state.raw_df is None:
        st.info("Upload a CSV or import course data with your UTSA cookies to get started.")
        return

    render_script_section()
    render_actions_section()


# ── 1. Data source ────────────────────────────────────────────────────────────

def render_data_source_section():
    st.header("1. Course Data")

    if st.session_state.raw_df is not None:
        st.success(f"Loaded: {st.session_state.source_label} ({len(st.session_state.raw_df)} rows)")
        if st.button("Load different data"):
            set_raw_df(None, None)
            st.rerun()
        return

    tab_csv, tab_cookies = st.tabs(["Upload CSV", "Import from UTSA (cookies)"])

    with tab_csv:
        uploaded_file = st.file_uploader("Upload course search CSV", type="csv")
        if uploaded_file is not None:
            set_raw_df(pd.read_csv(uploaded_file), uploaded_file.name)
            st.rerun()

    with tab_cookies:
        render_cookie_import()


def render_cookie_import():
    st.caption(
        "An alternative to uploading a CSV: log into the UTSA registration portal, open "
        "DevTools → Network, search for a course so the searchResults request fires, then "
        "copy the full 'Cookie' request header from that request. Cookies are only held in "
        "memory for this session — they are never written to disk."
    )
    cookies_raw = st.text_input("Banner cookie string", type="password")
    term_label = st.selectbox("Term", list(scraper.TERMS.keys()))
    subjects = st.multiselect(
        "Subjects (leave empty to fetch all)",
        options=scraper.SUBJECTS,
    )

    if st.button("Fetch Courses", disabled=not cookies_raw):
        subjects_to_use = subjects or scraper.SUBJECTS
        progress = st.progress(0.0, text="Starting...")

        def on_progress(i, total, subject):
            progress.progress(i / total, text=f"Fetched {subject} ({i}/{total})")

        try:
            df = scraper.scrape_courses(
                cookies_raw,
                scraper.TERMS[term_label],
                subjects=subjects_to_use,
                progress_cb=on_progress,
            )
        except scraper.ScraperAuthError as e:
            progress.empty()
            st.error(f"{e} Log back into the registration portal and copy a fresh cookie value.")
            return
        except Exception as e:
            progress.empty()
            st.error(f"Scrape failed: {e}")
            return

        progress.empty()
        if df.empty:
            st.warning("No sections found — check your cookies and term/subject selection.")
            return

        st.session_state.scraped_df = df
        st.session_state.scraped_label = f"UTSA import ({term_label})"
        st.rerun()

    if st.session_state.get("scraped_df") is not None:
        render_scrape_filters()


def render_scrape_filters():
    df = st.session_state.scraped_df
    st.divider()
    st.caption(f"Fetched {len(df)} sections. Optionally narrow them down before loading:")

    levels = st.multiselect("Course level", options=scraper.COURSE_LEVELS)
    meeting_types = st.multiselect("Meeting type", options=sorted(df["meeting_type"].dropna().unique()))
    campuses = st.multiselect("Campus", options=sorted(df["campus"].dropna().unique()))
    meeting_days = st.multiselect(
        "Meeting days (keeps sections meeting on ANY selected day)",
        options=scraper.MEETING_DAY_CODES,
    )

    if st.button("Load Courses"):
        filtered = scraper.filter_sections(
            df,
            levels=levels or None,
            meeting_types=meeting_types or None,
            campuses=campuses or None,
            meeting_days=meeting_days or None,
        )
        if filtered.empty:
            st.warning("No sections match those filters.")
            return
        set_raw_df(filtered, st.session_state.scraped_label)
        st.session_state.pop("scraped_df", None)
        st.session_state.pop("scraped_label", None)
        st.rerun()


# ── 2. Script ─────────────────────────────────────────────────────────────────

def render_script_section():
    st.header("2. Outreach Script")
    col1, col2 = st.columns([1, 3])
    with col1:
        # value= is required alongside key= here: this widget can be first
        # rendered on a script run triggered by our own st.rerun() (after a
        # CSV upload or cookie fetch) rather than by the widget's own
        # interaction, and Streamlit doesn't reliably hydrate a key-only
        # widget's DOM value in that case.
        st.text_input("Presenter name", value=st.session_state.presenter_name, key="presenter_name")
        if st.button("Reset to default script"):
            st.session_state.script = default_script(st.session_state.presenter_name)
            st.rerun()
    with col2:
        st.text_area("Script sent to each professor", value=st.session_state.script, key="script", height=220)


# ── 3. Actions ────────────────────────────────────────────────────────────────

def render_actions_section():
    st.header("3. Actions")
    acm = ACM_Data()
    tab_preview, tab_signup, tab_scripts, tab_heatmap = st.tabs(
        ["Preview", "Sign-Up CSV", "Teacher Scripts", "Heatmap"]
    )

    with tab_preview:
        render_preview_tab(acm)
    with tab_signup:
        render_signup_tab(acm)
    with tab_scripts:
        render_scripts_tab(acm)
    with tab_heatmap:
        render_heatmap_tab(acm)


def render_preview_tab(acm: ACM_Data):
    normalized = acm.normalize_df_headers(st.session_state.raw_df.copy())
    try:
        cleaned = acm.clean_df(normalized)
    except Exception as e:
        st.error(f"Could not clean this data: {e}")
        return
    st.write(f"{len(cleaned)} of {len(normalized)} rows remain after filtering (TBA times, grad courses, unstaffed sections, etc.).")
    st.dataframe(cleaned)


def render_signup_tab(acm: ACM_Data):
    if st.button("Generate Sign-Up CSV"):
        st.session_state.signup_df = acm.create_sign_up_df(st.session_state.raw_df.copy())

    if "signup_df" in st.session_state:
        st.dataframe(st.session_state.signup_df, use_container_width=True)
        csv_bytes = st.session_state.signup_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download sign-up CSV",
            data=csv_bytes,
            file_name=f"{safe_stem(st.session_state.source_label)}_signup.csv",
            mime="text/csv",
        )


def render_scripts_tab(acm: ACM_Data):
    st.caption(
        "If the loaded data already has 'presenter'/'presentation_date' columns (a completed "
        "sign-up roster), those are woven into each professor's script."
    )
    if st.button("Generate Teacher Scripts"):
        manager = acm.create_email_scripts_df(st.session_state.raw_df.copy())
        if not manager.professors:
            st.warning("No professors found — check that the data has an 'instructor' column.")
            st.session_state.pop("scripts_zip", None)
        else:
            st.session_state.scripts_zip = build_scripts_zip(manager, st.session_state.script)
            st.session_state.scripts_count = len(manager.professors)

    if "scripts_zip" in st.session_state:
        st.success(f"Generated scripts for {st.session_state.scripts_count} professors.")
        st.download_button(
            "Download teacher scripts (zip)",
            data=st.session_state.scripts_zip,
            file_name="teacher_scripts.zip",
            mime="application/zip",
        )


def build_scripts_zip(manager, script: str) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for professor in manager.professors:
            filename = ACM_Script.safe_professor_filename(professor)
            content = ACM_Script.build_script_text(professor, script)
            zf.writestr(filename, content)
    return buffer.getvalue()


def render_heatmap_tab(acm: ACM_Data):
    if st.button("Generate Heatmap"):
        try:
            st.session_state.heatmap_data = acm.create_heatmap_df(st.session_state.raw_df.copy())
        except Exception as e:
            st.error(f"Could not build heatmap: {e}")
            st.session_state.pop("heatmap_data", None)

    if "heatmap_data" in st.session_state:
        heatmap_data = st.session_state.heatmap_data
        st.altair_chart(build_heatmap_chart(heatmap_data), use_container_width=True)

        png_path = plot_heatmap_matplotlib(heatmap_data)
        with open(png_path, "rb") as f:
            st.download_button("Download heatmap PNG", data=f.read(), file_name="heatmap.png", mime="image/png")


def build_heatmap_chart(heatmap_data: pd.DataFrame) -> alt.Chart:
    long_df = (
        heatmap_data.reset_index()
        .rename(columns={"index": "time"})
        .melt(id_vars="time", var_name="day", value_name="classes")
    )
    day_order = list(heatmap_data.columns)
    time_order = list(heatmap_data.index)

    return (
        alt.Chart(long_df)
        .mark_rect()
        .encode(
            x=alt.X("day:N", sort=day_order, title="Day"),
            y=alt.Y("time:N", sort=time_order, title="Time", axis=alt.Axis(values=HOUR_TICKS)),
            color=alt.Color(
                "classes:Q",
                title="Classes",
                scale=alt.Scale(range=HEATMAP_COLOR_RANGE),
            ),
            tooltip=[alt.Tooltip("day:N", title="Day"), alt.Tooltip("time:N", title="Time"),
                     alt.Tooltip("classes:Q", title="Classes")],
        )
        .properties(height=900, title="Computer Science Classes Crowding")
    )


if __name__ == "__main__":
    main()
