def show_menu():
    role = input("Login as (student/teacher): ").strip().lower()

    if role == "student":
        from student import student_menu
        student_menu()
    elif role == "teacher":
        from teacher import teacher_menu
        teacher_menu()
    else:
        print("❌ Invalid role. Please choose 'student' or 'teacher'.")
