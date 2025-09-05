import json
from collections import defaultdict
from utils import get_student_by_id

def view_assignments(student):
    student_class = student["class"]
    student_id = student["id"]
    student_name = student["name"]

    try:
        with open("subjects.json", "r") as f:
            subject_map = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ subjects.json not found.")
        return

    valid_subjects = subject_map.get(student_class, [])

    try:
        with open("assignments.json", "r") as f:
            assignments = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ assignments.json not found.")
        return

    try:
        with open("assignment_submissions.json", "r") as f:
            submissions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        submissions = []

    submitted_subjects = {
        s["subject"].lower()
        for s in submissions
        if str(s["student_id"]) == str(student_id)
    }

    grouped = defaultdict(list)
    for a in assignments:
        if a.get("class", "").strip().lower() == student_class.strip().lower():
            subject = a.get("subject", "Unknown")
            if subject in valid_subjects:
                grouped[subject].append(a)

    if not grouped:
        print(f"📭 No assignments found for class '{student_class}'.")
        return

    print(f"\n📘 Assignments for {student_name} ({student_class}):")
    for subject, items in grouped.items():
        print(f"\n📚 Subject: {subject}")
        for a in items:
            deadline = a.get("deadline", "N/A")
            status = "✅ Submitted" if subject.lower() in submitted_subjects else "🕒 Pending"
            print(f"  - Deadline: {deadline} | {status}")

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
            "class": s.get("class", "Unknown"),
            "subject": s["subject"],
            "date": s["submitted_on"]
        }
        for s in filtered
    ]

def show_pending_assignments(student_id):
    student = get_student_by_id(student_id)
    if not student:
        print("❌ Student not found.")
        return

    student_class = student["class"]

    try:
        with open("assignments.json", "r") as f:
            all_assignments = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ No assignments found.")
        return

    class_assignments = [
        a for a in all_assignments if a.get("class", "").lower() == student_class.lower()
    ]

    try:
        with open("assignment_submissions.json", "r") as f:
            submissions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        submissions = []

    submitted_subjects = {
        s["subject"] for s in submissions if s["student_id"] == student_id
    }

    pending = [
        a for a in class_assignments if a["subject"] not in submitted_subjects
    ]

    if not pending:
        print("✅ No pending assignments.")
    else:
        print("\n📌 Pending Assignments:")
        for a in pending:
            print(f"- Subject: {a['subject']}, Deadline: {a['deadline']}")
