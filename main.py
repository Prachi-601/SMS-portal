from auth import login
from admin import admin_menu
from teacher import teacher_menu
from dashboard import student_dashboard
from auth import teacher_signup


def main():
    print("🔐 Login as:\n1. Admin\n2. Teacher\n3. Student")
    choice = input("Enter choice: ")

    if choice == "1":
        user = login("admin")
        if user:
            print("🔓 Access granted to admin panel.")
            admin_menu(user)
    elif choice == "2":
        user = login("teacher")
        if user:
            print("👨‍🏫 Welcome to the teacher panel.")
            teacher_menu(user)
    elif choice == "3":
        user = login("student")
        if user:
            print("🎓 Welcome to your dashboard.")
            student_dashboard(name)
    else:
        print("❌ Invalid choice.")



# Inside your HOD menu flow:
teacher_signup(hod_verified=True)

if __name__ == "__main__":
    main()

