# assignment.py

import json
from datetime import datetime
from student import get_student_by_id

def add_assignment(class_name, subject, deadline):
    from datetime import datetime
    import json

    assignment = {
        "class": class_name,
        "subject": subject,
        "deadline": deadline,
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

def submit_assignment(student_id, subject):
    # Step 1: Load student data
    try:
        with open("students.json", "r") as f:
            students = json.load(f).get("students", [])
    except FileNotFoundError:
        print("❌ students.json not found.")
        return

    student_class = None
    for student in students:
        if str(student["id"]) == str(student_id):
            student_class = student["class"]
            break

    if not student_class:
        print("❌ Student ID not found.")
        return

    # Step 2: Load subjects.json and validate subject for class
    try:
        with open("subjects.json", "r") as f:
            class_subjects = json.load(f)
    except FileNotFoundError:
        print("❌ subjects.json not found.")
        return

    valid_subjects = class_subjects.get(student_class, [])
    if subject.strip().lower() not in [s.lower() for s in valid_subjects]:
        print(f"❌ '{subject}' is not assigned to class '{student_class}'. Submission denied.")
        return

    # Step 3: Create submission entry
    submission = {
        "class": student_class,
        "student_id": student_id,
        "subject": subject,
        "submitted_on": str(datetime.now().date())
    }

    # Step 4: Save to assignment_submissions.json
    try:
        with open("assignment_submissions.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(submission)

    with open("assignment_submissions.json", "w") as f:
        json.dump(data, f, indent=4)

    print(f"✅ Submission recorded for Student ID: {student_id}")

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