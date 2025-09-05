import datetime
import json
import os
from subjects import load_subjects  # Ensure subjects.py exists

# 📘 Load timetable from JSON file
def load_timetable():
    if os.path.exists("timetable.json"):
        with open("timetable.json", "r") as f:
            return json.load(f)
    return {}

# 📝 Save timetable to JSON file
def save_timetable(data):
    with open("timetable.json", "w") as f:
        json.dump(data, f, indent=4)

# 📘 Load default time slots for a class
def load_default_slots(class_name):
    try:
        with open("default_slots.json", "r") as f:
            data = json.load(f)
        return data.get(class_name, [])
    except FileNotFoundError:
        return []

# 📝 Save default time slots for a class
def save_default_slots(class_name, slots):
    try:
        with open("default_slots.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    data[class_name] = slots
    with open("default_slots.json", "w") as f:
        json.dump(data, f, indent=2)

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

# 🧑‍🏫 Get current subject for a teacher based on time
def get_current_subject_for_teacher(teacher):
    today = datetime.datetime.today().strftime('%d-%m-%Y')
    current_time = datetime.datetime.now().strftime('%H:%M')
    timetable = load_timetable()
    today_slots = timetable.get(today, [])

    for slot in today_slots:
        try:
            start, end = slot["time"].split("–")
        except ValueError:
            continue  # Skip malformed time slots

        if start <= current_time <= end:
            class_name = teacher.get("class")
            return slot.get(class_name)  # May be None or "Recess"

    return None

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

# 🛠️ Create timetable for a class on a specific date
def create_timetable_for_class(date, class_name):
    timetable = load_timetable()
    slots = []

    previous_slots = load_default_slots(class_name)
    if previous_slots:
        print(f"\n📋 Previous default time slots for {class_name}:")
        for slot in previous_slots:
            print(f"{slot['time']}")
        use_defaults = input(f"\nDo you want to reuse these time slots for {class_name}? (y/n): ").lower()
        if use_defaults == 'y':
            for slot in previous_slots:
                time = slot["time"]
                subject = input(f"Enter subject for {class_name} at {time}: ")
                slots.append({"time": time, class_name: subject})
        else:
            slots = build_new_slots(class_name)
    else:
        print("ℹ️ No previous slots found for this class.")
        slots = build_new_slots(class_name)

    # Save time-only defaults
    time_only = [{"time": slot["time"]} for slot in slots]
    save_default_slots(class_name, time_only)

    timetable.setdefault(date, []).extend(slots)
    save_timetable(timetable)
    print(f"✅ Timetable created for {class_name} on {date}")

# 🔧 Helper to build new slots interactively
def build_new_slots(class_name):
    slots = []
    num_slots = int(input("Enter number of slots: "))
    for _ in range(num_slots):
        time = input("Enter time slot (e.g., 09:00–10:00): ")
        subject = input(f"Enter subject for {class_name} at {time}: ")
        slots.append({"time": time, class_name: subject})
    return slots

# 👀 View timetable for a class on a specific date
def view_timetable_for_class(class_name, date=None):
    if not date:
        date = datetime.datetime.today().strftime('%d-%m-%Y')
    timetable = load_timetable()
    slots = timetable.get(date, [])
    print(f"\n📅 Timetable for {class_name} on {date}:")
    for slot in slots:
        if class_name in slot:
            print(f"{slot['time']} → {slot[class_name]}")

# 🧪 Run this to create tomorrow's timetable interactively
if __name__ == "__main__":
    tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%d-%m-%Y')
    class_name = input("Enter class name: ")
    create_timetable_for_class(tomorrow, class_name)
