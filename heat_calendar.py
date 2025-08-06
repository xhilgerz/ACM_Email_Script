import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta



# Load the CSV

def load_csv(filename):
    df = pd.read_csv(filename)
    create_dataframe(df)

# --- Step 1: Parse Time Slots and Days ---
def parse_time_and_days(row):
    time_str = row["Times"]
    days_str = row["Meeting Days"].strip().upper()
    
    # Split start/end times (e.g., "9:00-9:50am" → ["9:00", "9:50am"])
    start_time, end_time = time_str.split("-")
    
    # Parse AM/PM
    period = "am" if "am" in end_time.lower() else "pm"
    end_time = end_time.replace("am", "").replace("pm", "")
    
    # Convert to datetime objects
    start = datetime.strptime(f"{start_time}{period}", "%I:%M%p")
    end = datetime.strptime(f"{end_time}{period}", "%I:%M%p")
    
    # Generate 5-minute intervals
    time_slots = []
    current = start
    while current <= end:
        time_slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=5)
    
    # Map days (e.g., "MWF" → ["Monday", "Wednesday", "Friday"])
    day_map = {
        "M": "Monday",
        "T": "Tuesday",
        "W": "Wednesday",
        "R": "Thursday",
        "F": "Friday",
        "S": "Saturday"
    }
    days = []
    i = 0
    while i < len(days_str):
        if days_str[i:i+2] == "TH":
            days.append(day_map["Th"])
            i += 2
        else:
            days.append(day_map[days_str[i]])
            i += 1
    print(f"Parsing days_str: {days_str} -> days: {days}")
    return time_slots, days

# --- Step 2: Aggregate Class Counts ---
# Initialize a DataFrame for heatmap

def create_dataframe(df):
    time_range = [f"{h:02d}:{m:02d}" for h in range(24) for m in range(0, 60, 5)]
    days_ordered = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    heatmap_data = pd.DataFrame(0, index=time_range, columns=days_ordered)

    # Populate counts
    for _, row in df.iterrows():
        if pd.isna(row["Times"]) or pd.isna(row["Meeting Days"]):
            continue
        time_slots, days = parse_time_and_days(row)
        for day in days:
            for time_slot in time_slots:
                if time_slot in heatmap_data.index and day in heatmap_data.columns:
                    heatmap_data.loc[time_slot, day] += 1

    print(heatmap_data.columns)
    print(heatmap_data.head())
    print(heatmap_data["Saturday"].sum())  # Should be > 0 if there are Saturday classes
    # --- Step 3: Plot Heatmap ---
    plt.figure(figsize=(14, 10))
    sns.heatmap(
        heatmap_data,
        cmap="blues",  # Change to your preferred color map
        annot=False,     # Show counts
        fmt="d",        # Integer format
        linewidths=0,
        cbar_kws={"label": "Number of Classes"}
    )

    plt.title("Computer Science Classes Crowding", fontsize=16)
    plt.xlabel("Day of Week", fontsize=12)
    plt.ylabel("Time Slot (5-minute intervals)", fontsize=12)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    yticks = plt.gca().get_yticks()
    yticklabels = [heatmap_data.index[int(tick)] for tick in yticks if int(tick) < len(heatmap_data.index)]
    for time_label in ["05:00","06:00","07:00", "08:00", "09:00","10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00" ,"17:00", "18:00", "19:00", "20:00","21:00", "22:00"]:
        if time_label in heatmap_data.index:
            idx = heatmap_data.index.get_loc(time_label)
            plt.axhline(idx, color='black', linestyle='-', linewidth=1)
    yticklabels_12hr = [
        datetime.strptime(label, "%H:%M").strftime("%I:%M %p") for label in yticklabels
    ]
    plt.gca().set_yticklabels(yticklabels_12hr)
    plt.gca().set_facecolor("#f0f0f0")  # Light gray background
    
    plt.tight_layout()

    plt.savefig("heatmap.png")
    plt.show()