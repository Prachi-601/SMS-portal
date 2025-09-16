import json
from datetime import datetime
from utils import get_student_by_id

def add_assignment(class_name, subject, deadline):
    try:
        # ✅ Validate deadline format
        datetime.strptime(deadline.strip(), "%d-%m-%Y")
    except ValueError:
        print("❌ Invalid deadline format. Use dd-mm-yyyy.")
        return

    assignment = {
        "class": class_name,
        "subject": subject,
        "deadline": deadline.strip(),
        "created_on": datetime.now().strftime("%d-%m-%Y")
    }

    try:
        with open("assignments.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(assignment)

    with open("assignments.json", "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Assignment added successfully.")

def view_assignments(student_id=None):
    try:
        with open("assignments.json", "r") as f:
            assignments = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ No assignments found.")
        return

    submitted_subjects = set()
    if student_id is not None:
        try:
            with open("assignment_submissions.json", "r") as f:
                submissions = json.load(f)
            submitted_subjects = {
                s["subject"].lower()
                for s in submissions
                if str(s["student_id"]) == str(student_id)
            }
        except (FileNotFoundError, json.JSONDecodeError):
            submitted_subjects = set()

    for a in assignments:
        status = ""
        if student_id is not None:
            status = "✅ Submitted" if a["subject"].lower() in submitted_subjects else "🕒 Pending"
        print(f"Class: {a['class']}, Subject: {a['subject']}, Deadline: {a['deadline']} {status}")

def submit_assignment(student_id, subject):
    student = get_student_by_id(student_id)
    if not student:
        print(f"❌ Student ID {student_id} not found. Skipping.")
        return

    student_class = student["class"]
    today = datetime.now().strftime("%d-%m-%Y")

    submission = {
        "class": student_class,
        "student_id": student_id,
        "subject": subject,
        "submitted_on": today
    }

    try:
        with open("assignment_submissions.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    for s in data:
        if s["student_id"] == student_id and s["subject"].lower() == subject.lower():
            print(f"⚠️ Already submitted: Student {student_id}, Subject {subject}")
            return

    data.append(submission)

    with open("assignment_submissions.json", "w") as f:
        json.dump(data, f, indent=4)

    print(f"✅ Submission recorded for Student ID: {student_id}, Subject: {subject}")

def view_submissions_by_id(student_id, subject_filter="", date_filter=""):
    try:
        with open("assignment_submissions.json", "r") as f:
            submissions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("📭 No submissions found.")
        return []

    filtered = [s for s in submissions if str(s.get("student_id")) == str(student_id)]

    if subject_filter:
        filtered = [s for s in filtered if s.get("subject", "").strip().lower() == subject_filter.strip().lower()]
    if date_filter:
        filtered = [s for s in filtered if s.get("submitted_on", "").strip() == date_filter.strip()]

    return [
        {
            "class": s["class"],
            "subject": s["subject"],
            "date": s["submitted_on"]
        }
        for s in filtered
    ]

def get_total_assignments_by_class(class_name):
    try:
        with open("assignments.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

    return sum(1 for a in data if a.get("class", "").lower() == class_name.lower())

def get_assignment_summary_by_name(name):
    try:
        with open("assignments.json", "r") as f:
            assignments = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    summary = [
        a for a in assignments
        if name.strip().lower() in a.get("subject", "").strip().lower()
    ]
    return summary

# ✅ NEW FUNCTIONS FOR EDIT/DELETE MODULES (ID-Free)

def get_assignments_by_class(class_name):
    try:
        with open("assignments.json", "r") as f:
            assignments = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    return [
        a for a in assignments
        if a.get("class", "").strip().lower() == class_name.strip().lower()
    ]

def edit_assignment_by_fields(class_name, subject, deadline, updated_fields):
    try:
        with open("assignments.json", "r") as f:
            assignments = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    for a in assignments:
        if (
            a.get("class") == class_name and
            a.get("subject") == subject and
            a.get("deadline") == deadline
        ):
            for key in ["class", "subject", "deadline"]:
                if key in updated_fields and updated_fields[key]:
                    a[key] = updated_fields[key]
            break
    else:
        return False

    with open("assignments.json", "w") as f:
        json.dump(assignments, f, indent=4)
    return True

def delete_assignment_by_fields(class_name, subject, deadline):
    try:
        with open("assignments.json", "r") as f:
            assignments = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    updated = [
        a for a in assignments
        if not (
            a.get("class") == class_name and
            a.get("subject") == subject and
            a.get("deadline") == deadline
        )
    ]

    if len(updated) == len(assignments):
        return False

    with open("assignments.json", "w") as f:
        json.dump(updated, f, indent=4)
    return True

def get_submission_records(class_name, subject):
    try:
        with open("assignment_submissions.json", "r") as f:
            submissions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    return [
        s for s in submissions
        if s.get("class", "").lower() == class_name.lower()
        and s.get("subject", "").lower() == subject.lower()
    ]

# ✅ CLI block for testing
if __name__ == "__main__":
    print("📘 Assignment Module Test")
    print("1. Add Assignment")
    print("2. View Assignments")
    print("3. Submit Assignment")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        class_name = input("Class: ")
        subject = input("Subject: ")
        deadline = input("Deadline (dd-mm-yyyy): ")
        add_assignment(class_name, subject, deadline)

    elif choice == "2":
        view_assignments()

    elif choice == "3":
        try:
            student_id = int(input("Student ID: "))
        except ValueError:
            print("❌ Invalid ID format.")
        else:
            subject = input("Subject: ")
            submit_assignment(student_id, subject)