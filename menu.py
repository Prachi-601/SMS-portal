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

    user = login(role)
    if not user:
        print("❌ Login failed.")
        return

    if role == "admin":
        admin_menu(user)
    elif role == "teacher":
        teacher_menu(user)
    elif role == "student":
        student_menu(user)

# ✅ CLI block
if __name__ == "__main__":
    show_menu()
