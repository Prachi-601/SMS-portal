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

    # 🔍 Step 1: Get subject from timetable
    scheduled_subject = get_current_subject_for_teacher(teacher)

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

if __name__ == "__main__":
    name = input("Enter student name to check attendance summary: ").strip()
    present, absent = get_attendance_summary_by_name(name)
    print(f"\n📋 Attendance Summary for {name}")
    print(f"✅ Present: {present}")
    print(f"❌ Absent: {absent}")
