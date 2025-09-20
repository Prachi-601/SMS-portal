import json
from datetime import datetime, timedelta
from subjects import load_subjects

def enter_subjects_for_class(admin_id):
    class_name = input("Enter class name (e.g., TY BSC CS): ").strip()
    subjects_input = input("Enter subjects for this class (comma-separated): ").strip()
    subjects = [s.strip() for s in subjects_input.split(",") if s.strip()]

    try:
        with open("subjects.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if admin_id not in data:
        data[admin_id] = {}

    if class_name in data[admin_id]:
        print(f"⚠️ Class '{class_name}' already has subjects: {data[admin_id][class_name]}")
        confirm = input("Do you want to overwrite them? (y/n): ").strip().lower()
        if confirm != "y":
            print("❌ Cancelled.")
            return

    data[admin_id][class_name] = subjects

    with open("subjects.json", "w") as f:
        json.dump(data, f, indent=4)

    print(f"✅ Subjects saved for class {class_name}")

def get_subjects_for_class(class_name, admin_id):
    try:
        with open("subjects.json", "r") as f:
            data = json.load(f)
        return data.get(admin_id, {}).get(class_name, [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def load_timetable():
    try:
        with open("timetable.json", "r") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_timetable(data):
    with open("timetable.json", "w") as f:
        json.dump(data, f, indent=4)

def load_default_slots(class_name):
    try:
        with open("default_slots.json", "r") as f:
            data = json.load(f)
        return data.get(class_name, [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_default_slots(class_name, slots):
    try:
        with open("default_slots.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    data[class_name] = slots
    with open("default_slots.json", "w") as f:
        json.dump(data, f, indent=2)

def add_timetable_for_date(date, slot_list):
    data = load_timetable()
    data[date] = slot_list
    save_timetable(data)

def get_today_timetable_for_class(class_name):
    today = datetime.today().strftime('%d-%m-%Y')
    data = load_timetable()
    slots = data.get(today, [])
    class_schedule = []

    for slot in slots:
        subject = slot.get(class_name, "Not Scheduled")
        class_schedule.append({"time": slot["time"], "subject": subject})

    return class_schedule

def get_current_subject_for_teacher(teacher):
    today = datetime.today().strftime('%d-%m-%Y')
    current_time = datetime.now().strftime('%H:%M')
    timetable = load_timetable()
    today_slots = timetable.get(today, [])

    for slot in today_slots:
        try:
            start, end = slot["time"].split("–")
        except ValueError:
            continue

        if start <= current_time <= end:
            for class_name in teacher.get("class_list", []):
                scheduled_subject = slot.get(class_name)
                if scheduled_subject:
                    return scheduled_subject
    return None

def get_custom_time_slots():
    slots = []
    print("Enter time slots (e.g., 09:00–10:00). Type 'done' to finish:")
    while True:
        slot = input("Time slot: ").strip()
        if slot.lower() == "done":
            break
        if "–" not in slot or len(slot) != 11:
            print("❌ Invalid format. Use HH:MM–HH:MM.")
            continue
        slots.append(slot)
    return slots

def build_new_slots(class_name, admin_id):
    subjects = get_subjects_for_class(class_name, admin_id)
    slots = []
    num_slots = int(input("Enter number of slots: "))
    for _ in range(num_slots):
        time = input("Enter time slot (e.g., 09:00–10:00): ").strip()
        subject = input(f"Enter subject for {class_name} at {time}: ").strip()
        if subject not in subjects:
            print("⚠️ Subject not valid for this class.")
            continue
        slots.append({"time": time, class_name: subject})
    return slots

def create_timetable_for_class(date, class_name, admin_id):
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
                subject = input(f"Enter subject for {class_name} at {time}: ").strip()
                slots.append({"time": time, class_name: subject})
        else:
            slots = build_new_slots(class_name, admin_id)
    else:
        print("ℹ️ No previous slots found for this class.")
        slots = build_new_slots(class_name, admin_id)

    time_only = [{"time": slot["time"]} for slot in slots]
    save_default_slots(class_name, time_only)

    timetable.setdefault(date, []).extend(slots)
    save_timetable(timetable)
    print(f"✅ Timetable created for {class_name} on {date}")

def view_timetable_for_class(class_name, admin_id, date=None):
    date_str = date if date else datetime.today().strftime('%d-%m-%Y')
    timetable = load_timetable()
    slots = timetable.get(date_str, [])
    if not slots:
        print(f"📭 No timetable made for {class_name} on {date_str}.")
        return
    print(f"\n📅 Timetable for {class_name} on {date_str}:")
    for slot in slots:
        if class_name in slot:
            print(f"{slot['time']} → {slot[class_name]}")

# 🧪 CLI block
if __name__ == "__main__":
    admin_id = "admin001"  # Default for testing
    tomorrow = (datetime.today() + timedelta(days=1)).strftime('%d-%m-%Y')
    class_name = input("Enter class name: ")
    create_timetable_for_class(tomorrow, class_name, admin_id)