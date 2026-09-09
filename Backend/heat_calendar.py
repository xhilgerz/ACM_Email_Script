import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


TIME_RANGE = [f"{h:02d}:{m:02d}" for h in range(24) for m in range(0, 60, 5)]
DAYS_ORDERED = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

DAY_MAP = {
    "M": "Monday",
    "T": "Tuesday",
    "W": "Wednesday",
    "R": "Thursday",
    "F": "Friday",
    "S": "Saturday",
}


def load_csv(filename):
    from Backend.data import ACM_Data

    df = pd.read_csv(filename)
    acm = ACM_Data()
    df = acm.normalize_df_headers(df)
    df = acm.clean_df(df)
    acm.df_to_csv(df, "heatmap_csv")

    heatmap_data = build_heatmap_dataframe(df)
    plot_heatmap_matplotlib(heatmap_data)
    return heatmap_data


# --- Step 1: Parse Time Slots and Days ---
def parse_time_and_days(row):
    time_str = row["times"]
    days_str = row["meeting_days"].strip().upper()

    # Split start/end times (e.g., "9:00-9:50am" → ["9:00", "9:50am"])
    start_time, end_time = time_str.split("-")

    # Parse AM/PM
    period = "am" if "am" in end_time.lower() else "pm"
    end_time = end_time.replace("am", "").replace("pm", "")

    # Convert to datetime objects
    start = datetime.strptime(f"{start_time}{period}", "%I:%M%p")
    end = datetime.strptime(f"{end_time}{period}", "%I:%M%p")

    # Only the end time carries am/pm, so a class that crosses noon
    # ("11:00-12:15pm") parses its start as 11 PM. Pull it back to the morning.
    if start > end:
        start -= timedelta(hours=12)

    # Generate 5-minute intervals
    time_slots = []
    current = start
    while current <= end:
        time_slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=5)

    # Map days (e.g., "MWF" → ["Monday", "Wednesday", "Friday"])
    days = []
    i = 0
    while i < len(days_str):
        days.append(DAY_MAP[days_str[i]])
        i += 1
    return time_slots, days


# --- Step 2: Aggregate Class Counts ---
def build_heatmap_dataframe(df) -> pd.DataFrame:
    """Pure aggregation: rows -> a Times x Days class-count grid. No plotting."""
    heatmap_data = pd.DataFrame(0, index=TIME_RANGE, columns=DAYS_ORDERED)

    for _, row in df.iterrows():
        if pd.isna(row["times"]) or pd.isna(row["meeting_days"]):
            continue
        if row["times"] in ("", "TBA") or row["meeting_days"] == "":
            continue
        time_slots, days = parse_time_and_days(row)
        for day in days:
            for time_slot in time_slots:
                if time_slot in heatmap_data.index and day in heatmap_data.columns:
                    heatmap_data.loc[time_slot, day] += 1

    return heatmap_data


# --- Step 3: Plot Heatmap (matplotlib/seaborn, for file export) ---
def plot_heatmap_matplotlib(heatmap_data: pd.DataFrame, output_path: str = "heatmap.png") -> str:
    plt.figure(figsize=(14, 10))
    sns.heatmap(
        heatmap_data,
        cmap="Blues",
        annot=False,
        fmt="d",
        linewidths=0,
        cbar_kws={"label": "Number of Classes"},
    )

    plt.title("Computer Science Classes Crowding", fontsize=16)
    plt.xlabel("Day of Week", fontsize=12)
    plt.ylabel("Time Slot (5-minute intervals)", fontsize=12)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    yticks = plt.gca().get_yticks()
    yticklabels = [heatmap_data.index[int(tick)] for tick in yticks if int(tick) < len(heatmap_data.index)]
    for time_label in ["05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00",
                        "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00"]:
        if time_label in heatmap_data.index:
            idx = heatmap_data.index.get_loc(time_label)
            plt.axhline(idx, color='black', linestyle='-', linewidth=1)
    yticklabels_12hr = [
        datetime.strptime(label, "%H:%M").strftime("%I:%M %p") for label in yticklabels
    ]
    plt.gca().set_yticklabels(yticklabels_12hr)
    plt.gca().set_facecolor("#f0f0f0")

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path
