import sys
from pathlib import Path

import streamlit.web.cli as stcli


def main():
    if "--legacy" in sys.argv:
        from Frontend import gui
        ACM = gui.ACMEmailGenerator()
        ACM.run()
        return

    app_path = Path(__file__).parent / "Frontend" / "streamlit_gui.py"
    sys.argv = ["streamlit", "run", str(app_path)]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
