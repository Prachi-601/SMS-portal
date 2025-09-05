from auth import login
from admin import admin_menu
from teacher import teacher_menu
from student import student_menu

def main():
    print("\n🔐 Login as:\n1. Admin\n2. Teacher\n3. Student")
    choice = input("Enter choice (1/2/3): ").strip()

    if choice == "1":
        user = login("admin")
        if user:
            print("🔓 Access granted to admin panel.")
            admin_menu(user)
        else:
            print("❌ Login failed.")

    elif choice == "2":
        user = login("teacher")
        if user:
            print("👨‍🏫 Welcome to the teacher panel.")
            teacher_menu(user)
        else:
            print("❌ Login failed.")

    elif choice == "3":
        user = login("student")
        if user:
            print("🎓 Welcome to your dashboard.")
            student_menu(user)
        else:
            print("❌ Login failed.")

    else:
        print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
