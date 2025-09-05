import json
from student import view_students, get_student_by_id
from attendance import mark_attendance
from assignment import add_assignment, submit_assignment, view_submissions_by_id
from test import schedule_test, add_marks, view_marks_by_student, view_marks_by_subject
from schedule import create_timetable_for_class, view_timetable_for_class

def teacher_login():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    try:
        with open("teachers.json", "r") as f:
            data = json.load(f)
            teachers = data.get("teachers", [])

        for teacher in teachers:
            if teacher["username"] == username and teacher["password"] == password:
                print(f"✅ Welcome, {teacher['name']}!")
                return teacher

        print("❌ Invalid credentials.")
        return None

    except FileNotFoundError:
        print("⚠️ Teachers file not found.")
        return None

def add_teacher():
    try:
        with open("teachers.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"teachers": []}

    username = input("Enter username for login: ").strip()
    password = input("Enter password for login: ").strip()
    name = input("Enter teacher name: ").strip()
    department = input("Enter department: ").strip()
    post = input("Enter post (e.g., Assistant Professor, HOD): ").strip()
    subject = input("Enter subject taught: ").strip()

    for teacher in data["teachers"]:
        if teacher.get("username", "").lower() == username.lower():
            print("Username already exists.")
            return

    new_teacher = {
        "username": username,
        "password": password,
        "name": name,
        "department": department,
        "post": post,
        "subject": subject
    }

    data["teachers"].append(new_teacher)

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

def teacher_menu(teacher):
    while True:
        print("\n📚 Teacher Menu:")
        print("1. Mark Attendance")
        print("2. View Students")
        print("3. View Teachers")
        print("4. Logout")
        print("5. Add Assignment")
        print("6. Submit Assignment")
        print("7. View Submissions")
        print("8. Schedule Test")
        print("9. Add Marks")
        print("10. View Marks by Student")
        print("11. View Marks by Subject")
        print("12. Create Timetable for Class")
        print("13. View Timetable for Class")

        choice = input("Choose an option: ")

        if choice == "1":
            mark_attendance(teacher)
        elif choice == "2":
            view_students()
        elif choice == "3":
            view_teachers()
        elif choice == "4":
            print("👋 Logging out...")
            break
        elif choice == "5":
            class_name = input("Enter class (e.g. TYCS): ").strip()
            subject = input("Enter subject: ").strip()
            deadline = input("Enter deadline (YYYY-MM-DD): ").strip()
            confirm = input("Confirm assignment creation? (y/n): ").lower()
            if confirm == "y":
                add_assignment(class_name, subject, deadline)
        elif choice == "6":
            student_id = input("Enter student ID: ").strip()
            try:
                student_id = int(student_id)
            except ValueError:
                print("❌ Invalid ID format.")
                return
            student = get_student_by_id(student_id)
            if not student:
                print("❌ Student ID not found.")
                return
            subject = input("Enter subject: ")
            confirm = input("Confirm submission? (y/n): ").lower()
            if confirm != "y":
                print("❌ Cancelled.")
                return
            submit_assignment(student_id, subject)
        elif choice == "7":
            student_id = input("Enter student ID to view submissions: ").strip()
            try:
                student_id = int(student_id)
                student = get_student_by_id(student_id)
                subject_filter = input("Filter by subject (press Enter to skip): ").strip()
                date_filter = input("Filter by date (YYYY-MM-DD, press Enter to skip): ").strip()

                submissions = view_submissions_by_id(student_id, subject_filter, date_filter)

                if student:
                    print(f"\n📤 Submitted Assignments for {student['name']} (ID {student_id}):")
                else:
                    print(f"\n📤 Submitted Assignments for Student ID {student_id}:")

                if not submissions:
                    print("No submissions found.")
                else:
                    for sub in submissions:
                        print(f"- Class: {sub['class']}, Subject: {sub['subject']}, Submitted on: {sub['date']}")
                    print(f"\n🧾 Total submissions: {len(submissions)}")

            except ValueError:
                print("❌ Invalid student ID format.")
        elif choice == "8":
            schedule_test()
        elif choice == "9":
            add_marks()
        elif choice == "10":
            view_marks_by_student()
        elif choice == "11":
            view_marks_by_subject()
        elif choice == "12":
            class_name = input("Enter class name: ").strip()
            date = input("Enter date (DD-MM-YYYY): ").strip()
            create_timetable_for_class(date, class_name)
        elif choice == "13":
            class_name = input("Enter class name: ").strip()
            date = input("Enter date (DD-MM-YYYY) or press Enter for today: ").strip()
            if not date:
                from datetime import datetime
                date = datetime.today().strftime("%d-%m-%Y")
            view_timetable_for_class(class_name, date)
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    teacher = teacher_login()
    if teacher:
        teacher_menu(teacher)
