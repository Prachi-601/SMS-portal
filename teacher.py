import json
from student import view_students
from attendance import mark_attendance
from student import get_student_by_id
from assignment import add_assignment, submit_assignment, view_submissions


def add_teacher():
    # Load existing data
    try:
        with open("teachers.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"teachers": []}

    # Input teacher details
    name = input("Enter teacher name: ").strip()
    department = input("Enter department: ").strip()
    post = input("Enter post (e.g., Assistant Professor, HOD): ").strip()
    subject = input("Enter subject taught: ").strip()

    # Optional duplicate check
    for teacher in data["teachers"]:
        if (teacher["name"].lower() == name.lower() and 
            teacher["department"].lower() == department.lower() and 
            teacher["post"].lower() == post.lower() and
            teacher["subject"].lower() == subject.lower()):
            print("Teacher already exists.")
            return

    # Add new teacher
    new_teacher = {
        "name": name,
        "department": department,
        "post": post,
        "subject": subject
    }
    data["teachers"].append(new_teacher)

    # Save to JSON
    with open("teachers.json", "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Teacher added successfully!")

def view_teachers():
    try:
        with open("teachers.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No teacher data found.")
        return

    teachers = data.get("teachers", [])
    if not teachers:
        print("No teacher records available.")
        return

    print("\n🎓 Teacher Records:")
    print("-" * 40)
    for teacher in teachers:
        print(f"Name: {teacher['name']}")
        print(f"Department: {teacher['department']}")
        print(f"Post: {teacher['post']}")
        print(f"Subject: {teacher['subject']}")
        print("-" * 40)
    print(f"Total teachers: {len(teachers)}\n")

def teacher_menu():
    while True:
        print("\n📚 Teacher Menu:")
        print("1. Mark Attendance")
        print("2. View Students")
        print("3. View Teachers")
        print("4. Logout")
        print("5. Add Assignment")
        print("6. Submit Assignment")
        print("7. View Submissions")


        choice = input("Choose an option: ")

        if choice == "1":
            mark_attendance()
        elif choice == "2":
            view_students()
        elif choice == "3":
            view_teachers()
        elif choice == "4":
            print("👋 Logging out...")
            break
        elif choice == "5":
            subject = input("Enter subject: ")
            topic = input("Enter topic: ")
            deadline = input("Enter deadline (YYYY-MM-DD): ")
            confirm = input("Confirm assignment creation? (y/n): ").lower()
            if confirm != "y":
                print("❌ Cancelled.")
                return
            add_assignment(subject, topic, deadline)


        elif choice == "6":
            student_id = input("Enter student ID: ")
            student = get_student_by_id(student_id)
            if not student:
                print("❌ Student ID not found.")
                return

            subject = input("Enter subject: ")
            topic = input("Enter topic: ")
            confirm = input("Confirm submission? (y/n): ").lower()
            if confirm != "y":
                print("❌ Cancelled.")
                return

            submit_assignment(student_id, subject, topic)
        elif choice == "7":
            view_submissions()
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    teacher_menu()
