import json
from datetime import date

def mark_attendance():
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

    today = str(date.today())
    attendance_record = {"date": today, "records": []}

    print(f"\n📅 Marking Attendance for {today}")
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
