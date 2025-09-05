def view_assignments(student_name):
    import json
    from collections import defaultdict

    try:
        with open("students.json", "r") as f:
            students = json.load(f).get("students", [])
    except FileNotFoundError:
        print("❌ students.json not found.")
        return

    student_class = None
    for student in students:
        if student["name"].strip().lower() == student_name.strip().lower():
            student_class = student["class"]
            break

    if not student_class:
        print("❌ Student not found.")
        return

    try:
        with open("subjects.json", "r") as f:
            subject_map = json.load(f)
    except FileNotFoundError:
        print("❌ subjects.json not found.")
        return

    valid_subjects = [s["subject"] for s in subject_map if s["class"].strip().lower() == student_class.strip().lower()]

    try:
        with open("assignments.json", "r") as f:
            assignments = json.load(f)
    except FileNotFoundError:
        print("❌ assignments.json not found.")
        return

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
            print(f"  - Topic: {a.get('topic', 'N/A')}, Deadline: {a.get('deadline', 'N/A')}")

def view_submissions_by_id(student_id, subject_filter="", date_filter=""):

    try:
        with open("assignment_submissions.json", "r") as f:
            submissions = json.load(f)
    except FileNotFoundError:
        print("📭 No submissions found.")
        return []

    # Filter by student ID
    filtered = [s for s in submissions if str(s.get("student_id")) == str(student_id)]

    # Apply subject filter if provided
    if subject_filter:
        filtered = [s for s in filtered if s.get("subject", "").strip().lower() == subject_filter.strip().lower()]

    # Apply date filter if provided
    if date_filter:
        filtered = [s for s in filtered if s.get("submitted_on", "").strip() == date_filter.strip()]

    # Return structured output
    return [
        {
            "class": s["class"],
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
    except FileNotFoundError:
        print("⚠️ No assignments found.")
        return

    class_assignments = [
        a for a in all_assignments if a.get("class") == student_class
    ]

    try:
        with open("assignment_submissions.json", "r") as f:
            submissions = json.load(f)
    except FileNotFoundError:
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

