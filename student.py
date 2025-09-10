import json
from assignment_views import view_assignments, view_submissions_by_id, show_pending_assignments
from schedule import view_timetable_for_class
from test import view_marks_by_student

def add_student():
    try:
        with open("students.json", "r") as f:
            raw = json.load(f)
            data = raw if isinstance(raw, dict) else {"students": raw}
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"students": []}

    try:
        student_id = int(input("Enter student ID: ").strip())
    except ValueError:
        print("❌ Invalid ID format.")
        return

    name = input("Enter student name: ").strip()
    student_class = input("Enter class: ").strip()
    username = input("Create username: ").strip()
    password = input("Create password: ").strip()
    email = input("Enter student email: ").strip().lower()

    if "@" not in email or "." not in email:
        print("❌ Invalid email format.")
        return

    for student in data["students"]:
        if student["id"] == student_id:
            print("⚠️ Student ID already exists.")
            return
        if student["username"].lower() == username.lower():
            print("⚠️ Username already taken.")
            return

    new_student = {
        "id": student_id,
        "name": name,
        "class": student_class,
        "username": username,
        "password": password,
        "email": email
    }

    data["students"].append(new_student)

    with open("students.json", "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Student added successfully!")

def view_students():
    class_filter = input("Enter class to filter (or press Enter to view all): ").strip()
    
    try:
        with open("students.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ No student data found.")
        return

    students = data.get("students", [])
    if class_filter:
        students = [s for s in students if s.get("class", "").lower() == class_filter.lower()]

    if not students:
        print("ℹ️ No student records available.")
        return

    print("\n📚 Student Records:")
    for student in students:
        print(f"ID: {student['id']}, Name: {student['name']}, Class: {student['class']}, Email: {student.get('email', 'Not available')}")
    print(f"Total students: {len(students)}")

def search_student():
    try:
        student_id = int(input("Enter student ID to search: "))
    except ValueError:
        print("❌ Invalid ID format.")
        return

    try:
        with open("students.json", "r") as f:
            students = json.load(f).get("students", [])
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ Student records file not found.")
        return

    for student in students:
        if student["id"] == student_id:
            print(f"\n🎓 Student Found:\nID: {student['id']}\nName: {student['name']}\nClass: {student['class']}\nEmail: {student.get('email', 'Not available')}")
            return

    print("❌ Student not found.")

def search_student_by_name():
    name_input = input("Enter student name to search: ").strip().lower()

    try:
        with open("students.json", "r") as f:
            students = json.load(f).get("students", [])
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ Student records file not found.")
        return

    matched = [s for s in students if name_input in s["name"].strip().lower()]
    if matched:
        for student in matched:
            print(f"\n🎓 Match Found:\nID: {student['id']}, Name: {student['name']}, Class: {student['class']}, Email: {student.get('email', 'Not available')}")
    else:
        print("❌ No matching student found.")

def edit_student():
    try:
        student_id = int(input("Enter student ID to edit: "))
    except ValueError:
        print("❌ Invalid ID format.")
        return

    try:
        with open("students.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ Student records file not found.")
        return

    students = data.get("students", [])
    for student in students:
        if student["id"] == student_id:
            print(f"\n🎓 Current Record:\nID: {student['id']}\nName: {student['name']}\nClass: {student['class']}\nEmail: {student.get('email', 'Not available')}")
            choice = input("Edit (1) Name, (2) Class, or (3) Email: ").strip()

            if choice == "1":
                student["name"] = input("Enter new name: ").strip()
            elif choice == "2":
                student["class"] = input("Enter new class: ").strip()
            elif choice == "3":
                new_email = input("Enter new email: ").strip().lower()
                if "@" not in new_email or "." not in new_email:
                    print("❌ Invalid email format.")
                    return
                student["email"] = new_email
            else:
                print("❌ Invalid choice.")
                return
            with open("students.json", "w") as f:
                json.dump(data, f, indent=4)
            print("✅ Student record updated.")
            return
    print("❌ Student not found.")

def edit_student_by_name():
    name_input = input("Enter student name to edit: ").strip().lower()

    try:
        with open("students.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ Student records file not found.")
        return

    students = data.get("students", [])
    matched = [s for s in students if name_input in s["name"].strip().lower()]
    if not matched:
        print("❌ No matching student found.")
        return

    for student in matched:
        print(f"\n🎓 Match Found:\nID: {student['id']}, Name: {student['name']}, Class: {student['class']}, Email: {student.get('email', 'Not available')}")
        confirm = input("Edit this student? (y/n): ").strip().lower()
        if confirm == "y":
            choice = input("Edit (1) Name, (2) Class, or (3) Email: ").strip()
            if choice == "1":
                student["name"] = input("Enter new name: ").strip()
            elif choice == "2":
                student["class"] = input("Enter new class: ").strip()
            elif choice == "3":
                new_email = input("Enter new email: ").strip().lower()
                if "@" not in new_email or "." not in new_email:
                    print("❌ Invalid email format.")
                    return
                student["email"] = new_email
            else:
                print("❌ Invalid choice.")
                return

            with open("students.json", "w") as f:
                json.dump(data, f, indent=4)
            print("✅ Student record updated.")
            return

def delete_specific_student_by_name():
    name_input = input("Enter student name to delete: ").strip().lower()

    try:
        with open("students.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ Student records file not found.")
        return

    students = data.get("students", [])
    matched = [s for s in students if name_input in s["name"].strip().lower()]
    if not matched:
        print("❌ No student found.")
        return

    for student in matched:
        print(f"\n👁 Found Student:\nID: {student['id']}, Name: {student['name']}, Class: {student['class']}")
        confirm = input("Delete this student? (y/n): ").strip().lower()
        if confirm == "y":
            students.remove(student)
            with open("students.json", "w") as f:
                json.dump({"students": students}, f, indent=4)
            print("✅ Student deleted.")
            return

def get_student_by_id(student_id):
    try:
        with open("students.json", "r") as f:
            data = json.load(f)
            for student in data.get("students", []):
                if student.get("id") == student_id:
                    return student
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    return None

def student_menu(student):
    while True:
        print(f"\n🎓 Welcome, {student['name']}!")
        print("1. View Assignments")
        print("2. View Submissions")
        print("3. View Pending Assignments")
        print("4. View Timetable")
        print("5. View Test Marks")
        print("6. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_assignments(student)
        elif choice == "2":
            submissions = view_submissions_by_id(student["id"])
            if submissions:
                print("\n📤 Your Submissions:")
                for sub in submissions:
                    print(f"- Class: {sub.get('class', 'Unknown')}, Subject: {sub['subject']}, Date: {sub.get('date', sub.get('submitted_on', 'Unknown'))}")
            else:
                print("📭 No submissions found.")
        elif choice == "3":
            show_pending_assignments(student["id"])
        elif choice == "4":
            view_timetable_for_class(student["class"])
        elif choice == "5":
            view_marks_by_student(student["id"])
        elif choice == "6":
            print("👋 Logging out...")
            break
        else:
            print("❌ Invalid choice.")