import datetime
import json
import os
from subjects import load_subjects  # Make sure you have subjects.py

# 📘 Load timetable from JSON file
def load_timetable():
    if os.path.exists("timetable.json"):
        with open("timetable.json", "r") as f:
            return json.load(f)
    else:
        return {}

# 📝 Save timetable to JSON file
def save_timetable(data):
    with open("timetable.json", "w") as f:
        json.dump(data, f, indent=4)

# ➕ Add timetable for a specific date
def add_timetable_for_date(date, slot_list):
    data = load_timetable()
    data[date] = slot_list
    save_timetable(data)

# 📅 Get today's timetable for a specific class
def get_today_timetable_for_class(class_name):
    today = datetime.datetime.today().strftime('%d-%m-%Y')
    data = load_timetable()
    slots = data.get(today, [])
    class_schedule = []

    for slot in slots:
        subject = slot.get(class_name, "Not Scheduled")
        class_schedule.append({"time": slot["time"], "subject": subject})

    return class_schedule

# ⏰ Let user define custom time slots
def get_custom_time_slots():
    slots = []
    print("Enter time slots (e.g., 09:00–10:00). Type 'done' to finish:")
    while True:
        slot = input("Time slot: ")
        if slot.lower() == "done":
            break
        slots.append(slot)
    return slots

# 🛠️ Create timetable class-by-class
def create_timetable_for_date(date):
    subjects_data = load_subjects()
    classes = list(subjects_data.keys())  # Dynamically get class names
    time_slots = get_custom_time_slots()
    full_schedule = []

    for cls in classes:
        print(f"\n📘 Creating timetable for {cls}")
        class_slots = {"class": cls, "slots": []}
        for time in time_slots:
            print(f"Select subject for {cls} at {time}:")
            options = subjects_data.get(cls, [])
            for i, sub in enumerate(options, start=1):
                print(f"{i}. {sub}")
            choice = input("Enter subject number or type 'Recess': ")
            if choice.lower() == "recess":
                subject = "Recess"
            else:
                try:
                    subject = options[int(choice)-1]
                except:
                    subject = "Not Scheduled"
            class_slots["slots"].append({"time": time, "subject": subject})
        full_schedule.append(class_slots)

    # Convert to multi-class format for saving
    final_slots = []
    for i in range(len(time_slots)):
        slot = {"time": time_slots[i]}
        for cls_data in full_schedule:
            slot[cls_data["class"]] = cls_data["slots"][i]["subject"]
        final_slots.append(slot)

    add_timetable_for_date(date, final_slots)
    print(f"✅ Timetable for {date} created successfully.")

# 🧪 Run this to create tomorrow's timetable interactively
if __name__ == "__main__":
    tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%d-%m-%Y')
    create_timetable_for_date(tomorrow)
