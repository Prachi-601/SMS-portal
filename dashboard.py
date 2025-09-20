import json
from attendance import get_attendance_summary_by_id, get_monthly_attendance
from assignment import get_assignment_summary_by_name, get_total_assignments_by_class
from test import get_test_marks_by_name
from student import get_student_by_id

def get_student_class_by_id(student_id, admin_id):
    try:
        with open("students.json", "r") as f:
            students = json.load(f).get("students", [])
    except FileNotFoundError:
        print("❌ students.json not found.")
        return None

    for student in students:
        if str(student.get("id")) == str(student_id) and student.get("admin_id") == admin_id:
            return student["class"]
    return None

def student_dashboard(name, student_id, admin_id):
    print(f"\n📋 Dashboard for {name}")

    # 1️⃣ Attendance
    try:
        with open("attendance.json", "r") as f:
            records = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        records = []

    present = 0
    absent = 0
    for entry in records:
        if entry.get("admin_id") != admin_id:
            continue
        for r in entry.get("records", []):
            if str(r.get("id")) == str(student_id):
                if r["status"] == "P":
                    present += 1
                elif r["status"] == "A":
                    absent += 1
    print(f"✅ Attendance: {present} Present, {absent} Absent")

    # 2️⃣ Assignments submitted count
    try:
        with open("assignment_submissions.json", "r") as f:
            submissions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        submissions = []

    submitted = sum(
        1 for s in submissions
        if str(s.get("student_id")) == str(student_id) and s.get("admin_id") == admin_id
    )

    print(f"📝 Assignments Submitted: {submitted}")

    # 3️⃣ Test marks
    try:
        with open("test_marks.json", "r") as f:
            all_marks = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_marks = []

    marks = [
        m for m in all_marks
        if str(m.get("student_id")) == str(student_id) and m.get("admin_id") == admin_id
    ]
    print("📊 Test Marks:")
    if marks:
        for m in marks:
            print(f"  Subject: {m['subject']}, Date: {m['date']}, Marks: {m['marks']}")
    else:
        print("  No test marks found.")

    # 4️⃣ Class-specific assignment total
    student_class = get_student_class_by_id(student_id, admin_id)
    if student_class:
        total_assignments = get_total_assignments_by_class(student_class, admin_id)
    else:
        total_assignments = 0

    # 5️⃣ Summary line
    total_days = present + absent
    attendance_percent = (present / total_days * 100) if total_days > 0 else 0

    print(f"\n📌 Summary:")
    print(f"Attendance: {attendance_percent:.0f}%")
    print(f"- Assignments Submitted: {submitted} of {total_assignments}")

if __name__ == "__main__":
    admin_id = "admin001"  # Default for testing
    try:
        student_id = int(input("Enter student ID to view dashboard: ").strip())
    except ValueError:
        print("❌ Invalid ID format.")
    else:
        student = get_student_by_id(student_id, admin_id)
        if student:
            student_dashboard(student["name"], student_id, admin_id)
        else:
            print("❌ Student not found.")