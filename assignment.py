import json
from datetime import datetime

# ✅ Validate date format
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# ✅ Add a new assignment
def add_assignment(subject, class_name, deadline, notes=""):
    if not is_valid_date(deadline):
        print("❌ Invalid date format. Use YYYY-MM-DD.")
        return

    assignment = {
        "subject": subject,
        "class": class_name,
        "deadline": deadline,
        "notes": notes,
        "created_on": str(datetime.now().date())
    }

    try:
        with open("assignments.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(assignment)

    with open("assignments.json", "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Assignment added successfully.")

# ✅ View all assignments
def view_assignments():
    try:
        with open("assignments.json", "r") as f:
            data = json.load(f)
            for a in data:
                print(f"Subject: {a['subject']}, Deadline: {a['deadline']}, Notes: {a.get('notes', '')}")
    except FileNotFoundError:
        print("No assignments found.")

# ✅ Validate if subject is assigned to student's class
def is_subject_valid_for_student(student_id, subject):
    try:
        with open("students.json", "r") as f:
            student_data = json.load(f)
            students = student_data.get("students", [])
    except FileNotFoundError:
        print("❌ Student data not available.")
        return False

    student_class = None
    for student in students:
        if str(student["id"]) == str(student_id):
            student_class = student["class"]
            break

    if not student_class:
        print("❌ Student ID not found.")
        return False

    try:
        with open("assignments.json", "r") as f:
            assignments = json.load(f)
    except FileNotFoundError:
        print("❌ Assignment data not available.")
        return False

    for a in assignments:
        if a["subject"].strip().lower() == subject.strip().lower() and a["class"].strip().lower() == student_class.strip().lower():
            return True

    print(f"❌ Subject '{subject}' is not assigned to class '{student_class}'.")
    return False

# ✅ Submit an assignment
def submit_assignment(student_input, subject):
    student_id = str(student_input).strip()

    # Try resolving name to ID if input is not numeric
    if not student_id.isdigit():
        try:
            with open("students.json", "r") as f:
                student_data = json.load(f)
                students = student_data.get("students", [])
                input_clean = student_id.lower()
                for student in students:
                    name_clean = student["name"].strip().lower()
                    if input_clean in name_clean:
                        student_id = str(student["id"])
                        print(f"🔍 Matched student: {student['name']} (ID: {student_id})")
                        break
                else:
                    print("❌ Student name not found.")
                    return
        except FileNotFoundError:
            print("❌ Student data not available.")
            return

    # ✅ Validate subject-class match
    if not is_subject_valid_for_student(student_id, subject):
        return

    submission = {
        "student_id": student_id,
        "subject": subject,
        "submitted_on": str(datetime.now().date())
    }

    try:
        with open("assignment_submissions.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    # Optional: prevent duplicate submission
    for s in data:
        if s["student_id"] == student_id and s["subject"] == subject:
            print("⚠️ Submission already recorded for this subject.")
            return

    data.append(submission)

    with open("assignment_submissions.json", "w") as f:
        json.dump(data, f, indent=4)

    print(f"✅ Submission recorded for Student ID: {student_id}")

# ✅ View all submissions
def view_submissions():
    try:
        with open("assignment_submissions.json", "r") as f:
            data = json.load(f)
            sorted_data = sorted(data, key=lambda x: x["submitted_on"])
            for s in sorted_data:
                print(f"Student ID: {s['student_id']}, Subject: {s['subject']}, Submitted on: {s['submitted_on']}")
    except FileNotFoundError:
        print("No submissions found.")

# ✅ Get assignment submission count by student name
def get_assignment_summary_by_name(name):
    name = name.strip().lower()

    # Step 1: Load student ID(s) from name
    try:
        with open("students.json", "r") as f:
            student_data = json.load(f)
            students = student_data.get("students", [])
    except FileNotFoundError:
        return 0

    matched_ids = [
        str(student["id"])
        for student in students
        if name in student["name"].strip().lower()
    ]

    if not matched_ids:
        return 0

    # Step 2: Count submissions for matched IDs
    try:
        with open("assignment_submissions.json", "r") as f:
            submissions = json.load(f)
    except FileNotFoundError:
        return 0

    count = sum(
        1 for s in submissions
        if s.get("student_id") in matched_ids
    )

    return count

# ✅ Get total number of assignments
def get_total_assignments():
    try:
        with open("assignments.json", "r") as f:
            data = json.load(f)
            return len(data)
    except FileNotFoundError:
        return 0

# ✅ Get total assignments for a specific class
def get_total_assignments_by_class(class_name):
    class_name = class_name.strip().lower()
    try:
        with open("assignments.json", "r") as f:
            data = json.load(f)
            return sum(1 for a in data if a.get("class", "").strip().lower() == class_name)
    except FileNotFoundError:
        return 0

# ✅ CLI test block
if __name__ == "__main__":
    student_input = input("Enter student name or ID: ").strip()
    subject = input("Enter subject: ").strip()
    confirm = input("Confirm submission? (y/n): ").strip().lower()
    if confirm == "y":
        submit_assignment(student_input, subject)
