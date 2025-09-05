import json
from datetime import date, datetime
from schedule import get_current_subject_for_teacher

def get_attendance_summary_by_id(student_id):
    try:
        with open("attendance.json", "r") as f:
            records = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0, 0

    present = 0
    absent = 0
    for entry in records:
        for r in entry.get("records", []):
            if str(r.get("id")) == str(student_id):
                if r["status"] == "P":
                    present += 1
                elif r["status"] == "A":
                    absent += 1
    return present, absent


def mark_attendance(teacher):
    try:
        with open("students.json", "r") as f:
            data = json.load(f)
            all_students = data.get("students", [])
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ Student records not found or corrupted.")
        return

    if not all_students:
        print("ℹ️ No students to mark attendance for.")
        return

    # ✅ Step 1: Select class
    print(f"\n📚 Classes assigned to you: {', '.join(teacher.get('class_list', []))}")
    selected_class = input("Enter class to mark attendance for: ").strip()

    if selected_class not in teacher.get("class_list", []):
        print("❌ You are not assigned to this class.")
        return

    students = [s for s in all_students if s.get("class") == selected_class]
    if not students:
        print("⚠️ No students found in this class.")
        return

    # ✅ Step 2: Get subject from timetable
    scheduled_subject = get_current_subject_for_teacher(teacher)

    if scheduled_subject:
        if scheduled_subject.lower() == "recess":
            print("⛔ Cannot mark attendance during recess.")
            return

        print(f"🕒 Scheduled subject right now: {scheduled_subject}")
        confirm = input("Do you want to mark attendance for this subject? (y/n): ").lower()
        subject = scheduled_subject if confirm == "y" else input("Enter subject manually: ").strip()
    else:
        print("⚠️ No subject scheduled for your class at this time.")
        subject = input("Enter subject manually: ").strip()

    today = str(date.today())

    # ✅ Step 3: Prevent duplicate attendance
    try:
        with open("attendance.json", "r") as f:
            all_attendance = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_attendance = []

    for record in all_attendance:
        if record["date"] == today and record["class"] == selected_class and record["subject"].lower() == subject.lower():
            print("⚠️ Attendance already marked for this class and subject today.")
            return

    # ✅ Step 4: Mark attendance
    attendance_record = {
        "date": today,
        "subject": subject,
        "teacher": teacher["username"],
        "class": selected_class,
        "records": []
    }

    print(f"\n📅 Marking Attendance for {today} | Class: {selected_class} | Subject: {subject}")
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

    all_attendance.append(attendance_record)

    with open("attendance.json", "w") as f:
        json.dump(all_attendance, f, indent=4)

    print("✅ Attendance marked and saved successfully!")

def get_monthly_attendance(student_id, month, year):
    try:
        with open("attendance.json", "r") as f:
            records = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0, 0

    present = 0
    total_days = 0

    for entry in records:
        try:
            entry_date = datetime.strptime(entry["date"], "%Y-%m-%d")
        except ValueError:
            continue

        if entry_date.month == month and entry_date.year == year:
            for r in entry.get("records", []):
                if str(r.get("id")) == str(student_id):
                    total_days += 1
                    if r["status"] == "P":
                        present += 1

    return present, total_days

if __name__ == "__main__":
    try:
        student_id = int(input("Enter student ID to check attendance summary: ").strip())
    except ValueError:
        print("❌ Invalid ID format.")
    else:
        present, absent = get_attendance_summary_by_id(student_id)
        print(f"\n📋 Attendance Summary for Student ID {student_id}")
        print(f"✅ Present: {present}")
        print(f"❌ Absent: {absent}")

