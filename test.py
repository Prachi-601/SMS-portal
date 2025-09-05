import json
def schedule_test():
    class_name = input("Enter class name: ").strip()
    subject = input("Enter subject: ").strip()
    test_date = input("Enter test date (YYYY-MM-DD): ").strip()

    test = {
        "class": class_name,
        "subject": subject,
        "date": test_date
    }

    try:
        with open("tests.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(test)

    with open("tests.json", "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Test scheduled successfully.")


def add_marks():
    subject = input("Enter subject: ").strip()
    test_date = input("Enter test date (YYYY-MM-DD): ").strip()

    try:
        with open("students.json", "r") as f:
            students = json.load(f).get("students", [])
    except FileNotFoundError:
        print("⚠️ No student data found.")
        return

    # Filter students by class based on scheduled test
    try:
        with open("tests.json", "r") as f:
            tests = json.load(f)
    except FileNotFoundError:
        print("⚠️ No test schedule found.")
        return

    test_class = None
    for test in tests:
        if test["subject"] == subject and test["date"] == test_date:
            test_class = test["class"]
            break

    if not test_class:
        print("❌ No matching test found.")
        return

    filtered_students = [s for s in students if s["class"] == test_class]

    marks_data = []
    for student in filtered_students:
        print(f"\nStudent: {student['name']} (ID: {student['id']})")
        try:
            marks = float(input("Enter marks: "))
        except ValueError:
            print("❌ Invalid input. Skipping.")
            continue

        marks_data.append({
            "student_id": student["id"],
            "name": student["name"],
            "subject": subject,
            "date": test_date,
            "marks": marks
        })

    try:
        with open("marks.json", "r") as f:
            existing = json.load(f)
    except FileNotFoundError:
        existing = []

    existing.extend(marks_data)

    with open("marks.json", "w") as f:
        json.dump(existing, f, indent=4)

    print("✅ Marks recorded successfully.")


def view_marks_by_student():
    student_id = input("Enter student ID: ").strip()

    try:
        with open("marks.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("⚠️ No marks data found.")
        return

    found = [m for m in data if str(m["student_id"]) == student_id]

    if not found:
        print("❌ No marks found for this student.")
        return

    print(f"\n📊 Marks for Student ID {student_id}:")
    for m in found:
        print(f"Subject: {m['subject']}, Date: {m['date']}, Marks: {m['marks']}")

def view_marks_by_subject():
    subject = input("Enter subject: ").strip()

    try:
        with open("marks.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("⚠️ No marks data found.")
        return

    found = [m for m in data if m["subject"].lower() == subject.lower()]

    if not found:
        print("❌ No marks found for this subject.")
        return

    print(f"\n📊 Marks for Subject: {subject}")
    for m in found:
        print(f"Student ID: {m['student_id']}, Name: {m['name']}, Date: {m['date']}, Marks: {m['marks']}")

def get_test_marks_by_name(name):
    name = name.strip().lower()

    try:
        with open("marks.json", "r") as f:
            marks_data = json.load(f)
    except FileNotFoundError:
        return []

    return [
        m for m in marks_data
        if name in m.get("name", "").strip().lower()
    ]

if __name__ == "__main__":
    name = input("Enter student name to check test marks: ").strip()
    marks = get_test_marks_by_name(name)
    print(f"\n📊 Test Marks for {name}:")
    if marks:
        for m in marks:
            print(f"Subject: {m['subject']}, Date: {m['date']}, Marks: {m['marks']}")
    else:
        print("No test marks found.")

def get_test_marks_by_name(name):
    name = name.strip().lower()

    try:
        with open("marks.json", "r") as f:
            marks_data = json.load(f)
    except FileNotFoundError:
        return []

    return [
        m for m in marks_data
        if name in m.get("name", "").strip().lower()
    ]