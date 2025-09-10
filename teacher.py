import json
from student import (
    add_student,
    view_students,
    search_student,
    search_student_by_name,
    edit_student,
    edit_student_by_name,
    delete_specific_student_by_name,
    get_student_by_id
)

from attendance import mark_attendance
from assignment import add_assignment, submit_assignment, view_submissions_by_id
from test import schedule_test, add_marks, view_marks_by_student, view_marks_by_subject
from schedule import (
    create_timetable_for_class,
    view_timetable_for_class,
    enter_subjects_for_class
)
from dashboard import student_dashboard
from attendance import get_monthly_attendance

def teacher_login():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    try:
        with open("teachers.json", "r") as f:
            data = json.load(f)
            teachers = data.get("teachers", [])
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ Teachers file not found or corrupted.")
        return None

    for teacher in teachers:
        if teacher["username"] == username and teacher["password"] == password:
            print(f"✅ Welcome, {teacher['name']}!")
            return teacher

    print("❌ Invalid credentials.")
    return None

def add_teacher():
    try:
        with open("teachers.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"teachers": []}

    username = input("Enter username for login: ").strip()
    password = input("Enter password for login: ").strip()
    name = input("Enter teacher name: ").strip()
    email = input("Enter teacher email: ").strip().lower()
    department = input("Enter department: ").strip()
    post = input("Enter post (e.g., Assistant Professor, HOD): ").strip()
    subject = input("Enter subject taught: ").strip()
    class_list = input("Enter classes assigned (comma-separated): ").strip().split(",")
    class_list = [cls.strip() for cls in class_list if cls.strip()]

    if "@" not in email or "." not in email:
        print("❌ Invalid email format.")
        return

    for teacher in data["teachers"]:
        if teacher.get("username", "").lower() == username.lower():
            print("⚠️ Username already exists.")
            return

    new_teacher = {
        "username": username,
        "password": password,
        "name": name,
        "email": email,
        "department": department,
        "post": post,
        "subject": subject,
        "class_list": class_list
    }

    data["teachers"].append(new_teacher)

    with open("teachers.json", "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Teacher added successfully!")

def view_teachers():
    try:
        with open("teachers.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ No teacher data found.")
        return

    teachers = data.get("teachers", [])
    if not teachers:
        print("ℹ️ No teacher records available.")
        return

    print("\n🎓 Teacher Records:")
    print("-" * 40)
    for teacher in teachers:
        print(f"Name: {teacher['name']}")
        print(f"Email: {teacher.get('email', 'Not available')}")
        print(f"Department: {teacher['department']}")
        print(f"Post: {teacher['post']}")
        print(f"Subject: {teacher['subject']}")
        print(f"Classes Assigned: {', '.join(teacher.get('class_list', []))}")
        print("-" * 40)
    print(f"Total teachers: {len(teachers)}\n")
def teacher_menu(teacher):
    while True:
        print(f"\n📚 Teacher Menu ({teacher['name']}):")
        print("1. View Students")
        print("2. Add Student")
        print("3. Search Student by ID")
        print("4. Search Student by Name")
        print("5. Edit Student by ID")
        print("6. Edit Student by Name")
        print("7. Delete Student by Name")

        print("8. Mark Attendance")
        print("9. View Teachers")

        print("10. Add Assignment")
        print("11. Submit Assignment")
        print("12. View Submissions")

        print("13. Schedule Test")
        print("14. Add Marks")
        print("15. View Marks by Student")
        print("16. View Marks by Subject")

        print("17. Create Timetable for Class")
        print("18. View Timetable for Class")
        print("19. Enter Subjects for Class")

        print("20. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_students()
        elif choice == "2":
            add_student()
        elif choice == "3":
            search_student()
        elif choice == "4":
            search_student_by_name()
        elif choice == "5":
            edit_student()
        elif choice == "6":
            edit_student_by_name()
        elif choice == "7":
            delete_specific_student_by_name()
        elif choice == "8":
            mark_attendance(teacher)
        elif choice == "9":
            view_teachers()
        elif choice == "10":
            subject = input("Enter subject: ")
            deadline = input("Enter deadline (YYYY-MM-DD): ")
            confirm = input("Confirm assignment creation? (y/n): ").lower()
            if confirm == "y":
                add_assignment(teacher["class_list"][0], subject, deadline)
            else:
                print("❌ Cancelled.")

        elif choice == "11":
            try:
                student_id = int(input("Enter student ID: ").strip())
            except ValueError:
                print("❌ Invalid ID format.")
                return
            student = get_student_by_id(student_id)
            if not student:
                print("❌ Student ID not found.")
                return
            subject = input("Enter subject: ")
            confirm = input("Confirm submission? (y/n): ").lower()
            if confirm == "y":
                submit_assignment(student_id, subject)
            else:
                print("❌ Cancelled.")
        elif choice == "12":
            try:
                student_id = int(input("Enter student ID to view submissions: ").strip())
                student = get_student_by_id(student_id)
                subject_filter = input("Filter by subject (press Enter to skip): ").strip()
                date_filter = input("Filter by date (YYYY-MM-DD, press Enter to skip): ").strip()
                submissions = view_submissions_by_id(student_id, subject_filter, date_filter)
                name = student["name"] if student else f"ID {student_id}"
                print(f"\n📤 Submissions for {name}:")
                if submissions:
                    for sub in submissions:
                        print(f"- Class: {sub['class']}, Subject: {sub['subject']}, Date: {sub['date']}")
                    print(f"\n🧾 Total submissions: {len(submissions)}")
                else:
                    print("📭 No submissions found.")
            except ValueError:
                print("❌ Invalid student ID format.")
        elif choice == "13":
            schedule_test()
        elif choice == "14":
            add_marks()
        elif choice == "15":
            view_marks_by_student()
        elif choice == "16":
            view_marks_by_subject()
        elif choice == "17":
            print(f"\n📚 Classes assigned: {', '.join(teacher['class_list'])}")
            class_name = input("Enter class to manage: ").strip()
            if class_name not in teacher["class_list"]:
                print("❌ You are not assigned to this class.")
                return
            date = input("Enter date (DD-MM-YYYY): ")
            create_timetable_for_class(date, class_name)
        elif choice == "18":
            print(f"\n📚 Classes assigned: {', '.join(teacher['class_list'])}")
            class_name = input("Enter class to view: ").strip()
            if class_name not in teacher["class_list"]:
                print("❌ You are not assigned to this class.")
                return
            date = input("Enter date (DD-MM-YYYY) or press Enter for today: ").strip()
            view_timetable_for_class(class_name, date if date else None)
        elif choice == "19":
            enter_subjects_for_class()
        elif choice == "20":
            print("👋 Logging out...")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    teacher = teacher_login()
    if teacher:
        teacher_menu(teacher)
