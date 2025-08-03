import json

def add_student():
    # Load existing data
    try:
        with open("students.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"students": []}

    # Input student details
    try:
        student_id = int(input("Enter student ID: ").strip())
    except ValueError:
        print("❌ Invalid ID format. Please enter digits only.")
        return

    name = input("Enter student name: ").strip()
    student_class = input("Enter class: ").strip()

    # Check for duplicate ID
    for student in data["students"]:
        if student["id"] == student_id:
            print("⚠️ Student ID already exists. Try another.")
            return

    # Add new student
    new_student = {
        "id": student_id,
        "name": name,
        "class": student_class
    }
    data["students"].append(new_student)

    # Save to JSON
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
        full_name = student["name"].strip().lower()
        if name_input in full_name:
            matched_students.append(student)

    if matched_students:
        for student in matched_students:
            print("\n🎓 Student Found:")
            print(f"ID: {student['id']}")
            print(f"Name: {student['name']}")
            print(f"Class: {student['class']}")
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
        students = data["students"]  # 👈 access the actual list

    for student in students:
        if student["id"] == student_id:  # 👈 use lowercase 'id'
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
                new_name = input("Enter new name: ")
                student["name"] = new_name
            elif choice == "2":
                new_class = input("Enter new class: ")
                student["class"] = new_class
            else:
                print("❌ Invalid choice.")
                return

            # Save updates
            with open("students.json", "w") as f:
                json.dump(data, f, indent=4)

            print("✅ Student record updated successfully.")
            return  # Stop after first confirmed edit

    print("ℹ️ No edits made.")


# Optional direct testing
if __name__ == "__main__":
    add_student()
