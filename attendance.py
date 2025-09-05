import json
from datetime import date, datetime
from schedule import get_current_subject_for_teacher

def mark_attendance(teacher):
    try:
        with open("students.json", "r") as f:
            data = json.load(f)
            students = data.get("students", [])
    except FileNotFoundError:
        print("⚠️ Student records not found.")
        return

    if not students:
        print("ℹ️ No students to mark attendance for.")
        return

    # 🔍 Step 0: Ask teacher which class to mark attendance for
    print(f"\n📚 Classes assigned to you: {', '.join(teacher.get('class_list', []))}")
    selected_class = input("Enter class to mark attendance for: ").strip()

    if selected_class not in teacher.get("class_list", []):
        print("❌ You are not assigned to this class.")
        return

    # Filter students by selected class
    students = [s for s in students if s.get("class") == selected_class]
    if not students:
        print(f"ℹ️ No students found for class {selected_class}.")
        return

    # 🔍 Step 1: Get subject from timetable
    scheduled_subject = get_current_subject_for_teacher(teacher, selected_class)

    if scheduled_subject:
        if scheduled_subject.lower() == "recess":
            print("⛔ Cannot mark attendance during recess.")
            return

        print(f"🕒 Scheduled subject right now: {scheduled_subject}")
        confirm = input("Do you want to mark attendance for this subject? (y/n): ").lower()
        if confirm == "y":
            subject = scheduled_subject
        else:
            subject = input("Enter subject manually: ").strip()
    else:
        print("⚠️ No subject scheduled for your class at this time.")
        subject = input("Enter subject manually: ").strip()

    today = str(date.today())
    attendance_record = {
        "date": today,
        "subject": subject,
        "teacher": teacher["username"],
        "class": selected_class,
        "records": []
    }

    print(f"\n📅 Marking Attendance for {today} | Subject: {subject}")
    for student in students:
        print(f"\nStudent: {student['name']} (ID: {student['id']})")
        status = input("Enter status (P/A): ").strip().upper()
        if status not in ["P", "A"]:
            print("❌ Invalid input. Marking as Absent by default.")
            status = "A"
        attendance_record["records"].append({
            "id": student["id"],
            "name": student["name"],
            "status": status
        })

    try:
        with open("attendance.json", "r") as f:
            all_attendance = json.load(f)
    except FileNotFoundError:
        all_attendance = []

    all_attendance.append(attendance_record)

    with open("attendance.json", "w") as f:
        json.dump(all_attendance, f, indent=4)

    print("✅ Attendance marked and saved successfully!")

def get_attendance_summary_by_name(name):
    try:
        with open("attendance.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return 0, 0

    name = name.strip().lower()
    present = 0
    absent = 0

    for entry in data:
        for record in entry.get("records", []):
            record_name = record.get("name", "").strip().lower()
            if name in record_name:
                if record.get("status") == "P":
                    present += 1
                elif record.get("status") == "A":
                    absent += 1

    return present, absent

def get_monthly_attendance(student_name, month, year):
    try:
        with open("attendance.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("⚠️ attendance.json not found.")
        return 0, 0

    present = 0
    total = 0

    for entry in data:
        try:
            date_obj = datetime.strptime(entry["date"], "%Y-%m-%d")
        except ValueError:
            continue

        if date_obj.month == int(month) and date_obj.year == int(year) and date_obj.weekday() != 6:
            for record in entry.get("records", []):
                if record["name"].strip().lower() == student_name.strip().lower():
                    total += 1
                    if record["status"].upper() == "P":
                        present += 1

    return present, total

# Optional test block
if __name__ == "__main__":
    name = input("Enter student name to check attendance summary: ").strip()
    present, absent = get_attendance_summary_by_name(name)
    print(f"\n📋 Attendance Summary for {name}")
    print(f"✅ Present: {present}")
    print(f"❌ Absent: {absent}")
