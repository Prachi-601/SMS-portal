import json
from attendance import get_attendance_summary_by_name
from assignment import get_assignment_summary_by_name, get_total_assignments_by_class
from test import get_test_marks_by_name


def get_student_class(student_name):
    """Return the class (e.g., TYCS, BCOM) for a given student name."""
    try:
        with open("students.json", "r") as f:
            students = json.load(f).get("students", [])
    except FileNotFoundError:
        print("❌ students.json not found.")
        return None

    for student in students:
        if student["name"].strip().lower() == student_name.strip().lower():
            return student["class"]
    return None

def student_dashboard(name):
    print(f"\n📋 Dashboard for {name}")

    # 1️⃣ Attendance
    present, absent = get_attendance_summary_by_name(name)
    print(f"✅ Attendance: {present} Present, {absent} Absent")

    # 2️⃣ Assignments submitted count
    submitted = get_assignment_summary_by_name(name)
    print(f"📝 Assignments Submitted: {submitted}")

    # 3️⃣ Test marks
    marks = get_test_marks_by_name(name)
    print("📊 Test Marks:")
    if marks:
        for m in marks:
            print(f"  Subject: {m['subject']}, Date: {m['date']}, Marks: {m['marks']}")
    else:
        print("  No test marks found.")

    # 4️⃣ Class-specific assignment total
    student_class = get_student_class(name)
    if student_class:
        total_assignments = get_total_assignments_by_class(student_class)
    else:
        total_assignments = 0

    # 5️⃣ Summary line
    total_days = present + absent
    attendance_percent = (present / total_days * 100) if total_days > 0 else 0

    print(f"\n📌 Summary:")
    print(f"Attendance: {attendance_percent:.0f}%")
    print(f"- Assignments Submitted: {submitted} of {total_assignments}")

if __name__ == "__main__":
    student_name = input("Enter student name to view dashboard: ").strip()
    student_dashboard(student_name)
