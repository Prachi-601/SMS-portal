import json
from assignment_views import view_assignments, view_submissions_by_id, show_pending_assignments
from schedule import view_timetable_for_class
from test import view_marks_by_student
def add_student():
    try:
        with open("students.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"students": []}

    try:
        student_id = int(input("Enter student ID: ").strip())
    except ValueError:
        print("❌ Invalid ID format. Please enter digits only.")
        return

    name = input("Enter student name: ").strip()
    student_class = input("Enter class: ").strip()

    for student in data["students"]:
        if student["id"] == student_id:
            print("⚠️ Student ID already exists. Try another.")
            return

    new_student = {
        "id": student_id,
        "name": name,
        "class": student_class
    }
    data["students"].append(new_student)

    with open("students.json", "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Student added successfully!")

def view_students():
    try:
        with open("students.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("⚠️ No student data found.")
        return

    students = data.get("students", [])
    if not students:
        print("ℹ️ No student records available.")
        return

    print("\n📚 Student Records:")
    print("-" * 30)
    for student in students:
        print(f"ID: {student['id']}, Name: {student['name']}, Class: {student['class']}")
    print("-" * 30)
    print(f"Total students: {len(students)}\n")

def search_student():
    try:
        student_id = int(input("Enter student ID to search: "))
    except ValueError:
        print("❌ Invalid ID format.")
        return

    try:
        with open("students.json", "r") as f:
            students = json.load(f)

        for student in students.get("students", []):
            if student["id"] == student_id:
                print("\n🎓 Student Found:")
                print(f"ID: {student['id']}")
                print(f"Name: {student['name']}")
                print(f"Class: {student['class']}")
                return

        print("❌ Student not found.")

    except FileNotFoundError:
        print("⚠️ Student records file not found.")

def get_student_by_id(student_id):
    try:
        with open("students.json", "r") as f:
            data = json.load(f)
            for student in data.get("students", []):
                if student.get("id") == student_id:
                    return student
    except FileNotFoundError:
        return None
    return None

def search_student_by_name():
    name_input = input("Enter student name to search: ").strip().lower()

    try:
        with open("students.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("⚠️ Student records file not found.")
        return

    matched_students = []
    for student in data.get("students", []):
        if name_input in student["name"].strip().lower():
            matched_students.append(student)

    if matched_students:
        for student in matched_students:
            print("\n🎓 Student Found:")
            print(f"ID: {student['id']}, Name: {student['name']}, Class: {student['class']}")
    else:
        print("❌ No matching student found.")

def edit_student():
    student_id = input("Enter student ID to edit: ")
    
    try:
        student_id = int(student_id)
    except ValueError:
        print("❌ Invalid ID. Please enter a numeric value.")
        return

    with open("students.json", "r") as f:
        data = json.load(f)
        students = data["students"]

    for student in students:
        if student["id"] == student_id:
            print(f"\n🎓 Current Record:\nID: {student['id']}\nName: {student['name']}\nClass: {student['class']}")
            choice = input("\nWhat would you like to edit?\n1. Name\n2. Class\nChoose (1/2): ")

            if choice == "1":
                new_name = input("Enter new name: ")
                student["name"] = new_name
            elif choice == "2":
                new_class = input("Enter new class: ")
                student["class"] = new_class
            else:
                print("❌ Invalid choice.")
                return

            with open("students.json", "w") as f:
                json.dump(data, f, indent=4)

            print("✅ Student record updated successfully.")
            return

    print("❌ Student not found.")

def edit_student_by_name():
    name_input = input("Enter student name to edit: ").strip().lower()

    try:
        with open("students.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("⚠️ Student records file not found.")
        return

    students = data.get("students", [])
    matched_students = [
        student for student in students
        if name_input in student["name"].strip().lower()
    ]

    if not matched_students:
        print("❌ No matching student found.")
        return

    for student in matched_students:
        print(f"\n🎓 Match Found:\nID: {student['id']}, Name: {student['name']}, Class: {student['class']}")
        confirm = input("Do you want to edit this student? (Y/N): ").strip().lower()
        if confirm == "y":
            choice = input("\nWhat would you like to edit?\n1. Name\n2. Class\nChoose (1/2): ")
            if choice == "1":
                student["name"] = input("Enter new name: ")
            elif choice == "2":
                student["class"] = input("Enter new class: ")
            else:
                print("❌ Invalid choice.")
                return

            with open("students.json", "w") as f:
                json.dump(data, f, indent=4)

            print("✅ Student record updated successfully.")
            return

    print("ℹ️ No edits made.")

def delete_specific_student_by_name():
    name_input = input("Enter the student name to delete: ").strip().lower()

    try:
        with open("students.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("⚠️ Student records file not found.")
        return

    students = data.get("students", [])
    matched_students = [
        student for student in students
        if name_input in student["name"].strip().lower()
    ]

    if not matched_students:
        print("❌ No student found with that name.")
        return

    for student in matched_students:
        print("\n👁 Found Student:")
        print(f"ID: {student['id']}, Name: {student['name']}, Class: {student['class']}")

        confirm = input("\n⚠️ Do you want to delete this student? (Y/N): ").strip().lower()
        if confirm == "y":
            students.remove(student)
            with open("students.json", "w") as f:
                json.dump({"students": students}, f, indent=4)
            print("✅ Student deleted successfully.")
            return
        else:
            print("ℹ️ Deletion cancelled.")
            return

def sort_students_by_course():
    try:
        with open("students.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("⚠️ Student records file not found.")
        return

    students = data.get("students", [])
    sorted_students = sorted(students, key=lambda x: x["class"])

    print("\n📊 Students Sorted by Class:")
    for student in sorted_students:
        print(f"ID: {student['id']}, Name: {student['name']}, Class: {student['class']}")


# Direct testing
if __name__ == "__main__":
    add_student()
