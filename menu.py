from auth import login
from admin import admin_menu
from teacher import teacher_menu
from student import student_menu

def show_menu():
    print("\n🔐 Login as:\n1. Admin\n2. Teacher\n3. Student")
    role_map = {"1": "admin", "2": "teacher", "3": "student"}
    choice = input("Enter choice (1/2/3): ").strip()
    role = role_map.get(choice)

    if not role:
        print("❌ Invalid choice. Please select 1, 2, or 3.")
        return

    if role == "admin":
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        user = login(role, username, password, None)
        if user:
            admin_menu(user)
        else:
            print("❌ Login failed.")
    else:
        admin_id = input("Enter your admin ID: ").strip()
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        user = login(role, username, password, admin_id)
        if not user:
            print("❌ Login failed.")
            return

        if role == "teacher":
            teacher_menu(user, admin_id)
        elif role == "student":
            student_menu(user, admin_id)

# ✅ CLI block
if __name__ == "__main__":
    show_menu()