import json
from datetime import datetime
from utils import get_student_by_id

def schedule_test():
    class_name = input("Enter class name: ").strip()
    subject = input("Enter subject: ").strip()
    test_date = input("Enter test date (DD-MM-YYYY): ").strip()

    try:
        datetime.strptime(test_date, "%d-%m-%Y")  # ✅ Validate DD-MM-YYYY
    except ValueError:
        print("❌ Invalid date format.")
        return

    try:
        max_marks = int(input("Enter maximum marks: ").strip())
        if max_marks <= 0:
            print("❌ Max marks must be positive.")
            return
    except ValueError:
        print("❌ Invalid marks input.")
        return

    test = {
        "class": class_name,
        "subject": subject,
        "date": test_date,
        "max_marks": max_marks
    }

    try:
        with open("tests.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    for t in data:
        if t["class"] == class_name and t["subject"] == subject and t["date"] == test_date:
            print("⚠️ Test already scheduled.")
            return

    data.append(test)

    with open("tests.json", "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Test scheduled successfully.")

def add_marks():
    subject = input("Enter subject: ").strip()
    test_date = input("Enter test date (DD-MM-YYYY): ").strip()

    try:
        datetime.strptime(test_date, "%d-%m-%Y")
    except ValueError:
        print("❌ Invalid date format.")
        return

    try:
        with open("students.json", "r") as f:
            students = json.load(f).get("students", [])
    except:
        print("⚠️ No student data found.")
        return

    try:
        with open("tests.json", "r") as f:
            tests = json.load(f)
    except:
        print("⚠️ No test schedule found.")
        return

    test_class = None
    max_marks = None
    for test in tests:
        if test["subject"] == subject and test["date"] == test_date:
            test_class = test["class"]
            max_marks = test.get("max_marks")
            break

    if not test_class or max_marks is None:
        print("❌ No matching test found.")
        return

    filtered_students = [s for s in students if s["class"] == test_class]

    try:
        with open("marks.json", "r") as f:
            existing = json.load(f)
    except:
        existing = []

    existing_keys = {(m["student_id"], m["subject"], m["date"]) for m in existing}
    marks_data = []

    for student in filtered_students:
        key = (student["id"], subject, test_date)
        if key in existing_keys:
            print(f"⚠️ Marks already recorded for {student['name']} (ID: {student['id']}). Skipping.")
            continue

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
            "marks": marks,
            "max_marks": max_marks
        })

    existing.extend(marks_data)

    with open("marks.json", "w") as f:
        json.dump(existing, f, indent=4)

    print("✅ Marks recorded successfully.")

def view_marks_by_student(student_id=None):
    if student_id is None:
        student_id = input("Enter student ID: ").strip()

    start_date = input("Enter start date (DD-MM-YYYY) or press Enter to skip: ").strip()
    end_date = input("Enter end date (DD-MM-YYYY) or press Enter to skip: ").strip()

    try:
        with open("marks.json", "r") as f:
            data = json.load(f)
    except:
        print("⚠️ No marks data found.")
        return

    try:
        start_dt = datetime.strptime(start_date, "%d-%m-%Y") if start_date else None
        end_dt = datetime.strptime(end_date, "%d-%m-%Y") if end_date else None
    except ValueError:
        print("❌ Invalid date format.")
        return

    filtered = []
    for m in data:
        if str(m["student_id"]) != str(student_id):
            continue
        try:
            mark_date = datetime.strptime(m["date"], "%d-%m-%Y")
        except:
            continue
        if start_dt and mark_date < start_dt:
            continue
        if end_dt and mark_date > end_dt:
            continue
        filtered.append(m)

    if not filtered:
        print("❌ No marks found for this student in the given range.")
        return

    print(f"\n📊 Marks for Student ID {student_id}:")
    for m in filtered:
        print(f"- Subject: {m['subject']}, Date: {m['date']}, Marks: {m['marks']}/{m.get('max_marks', 'N/A')}")

def view_marks_by_subject():
    subject = input("Enter subject: ").strip()
    test_date = input("Enter test date (DD-MM-YYYY): ").strip()

    try:
        datetime.strptime(test_date, "%d-%m-%Y")
    except ValueError:
        print("❌ Invalid date format.")
        return

    try:
        with open("marks.json", "r") as f:
            data = json.load(f)
    except:
        print("⚠️ No marks data found.")
        return

    found = [m for m in data if m["subject"].lower() == subject.lower() and m["date"] == test_date]

    if not found:
        print("❌ No marks found for this subject and date.")
        return

    print(f"\n📊 Marks for Subject: {subject} on {test_date}")
    total = 0
    highest = float("-inf")
    lowest = float("inf")

    for m in found:
        marks = m["marks"]
        print(f"Student ID: {m['student_id']}, Name: {m['name']}, Marks: {marks}/{m.get('max_marks', 'N/A')}")
        total += marks
        highest = max(highest, marks)
        lowest = min(lowest, marks)

    average = round(total / len(found), 2)
    print(f"\n📈 Class Analytics:")
    print(f"- Average Marks: {average}")
    print(f"- Highest Marks: {highest}")
    print(f"- Lowest Marks: {lowest}")

def get_test_marks_by_name(name):
    name = name.strip().lower()
    try:
        with open("marks.json", "r") as f:
            marks_data = json.load(f)
    except:
        return []

    return [m for m in marks_data if name in m.get("name", "").strip().lower()]

def get_tests_by_class(class_name):
    try:
        with open("tests.json", "r") as f:
            tests = json.load(f)
    except:
        return []

    return [t for t in tests if t.get("class", "").strip().lower() == class_name.strip().lower()]

def view_all_tests():
    try:
        with open("tests.json", "r") as f:
            tests = json.load(f)
    except:
        print("⚠️ No tests found.")
        return

    print("\n🗓️ Scheduled Tests:")
    for t in tests:
        print(f"- Class: {t['class']}, Subject: {t['subject']}, Date: {t['date']}")

# ✅ CLI block
if __name__ == "__main__":
    print("📘 Test Module")
    print("1. Schedule Test")
    print("2. Add Marks")
    print("3. View All Tests")
    choice = input("Choose: ").strip()

    if choice == "1":
        schedule_test()
    elif choice == "2":
        add_marks()
    elif choice == "3":
        view_all_tests()