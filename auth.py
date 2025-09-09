import json

# 🔐 Admin Login
def admin_login(username, password):
    try:
        with open("admins.json", "r") as file:
            admins = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    for admin in admins.get("admins", []):
        if admin["username"] == username and admin["password"] == password:
            return admin
    return None
def update_student_password(username, old_pass, new_pass):
    try:
        with open("students.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    for student in data.get("students", []):
        if student["username"] == username and student["password"] == old_pass:
            student["password"] = new_pass
            with open("students.json", "w") as f:
                json.dump(data, f, indent=4)
            return True
    return False
# 👨‍🏫 Teacher Login
def teacher_login(username, password):
    try:
        with open("teachers.json", "r") as file:
            raw = json.load(file)
            teachers = raw if isinstance(raw, dict) else {"teachers": raw}
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    for teacher in teachers.get("teachers", []):
        if teacher["username"] == username and teacher["password"] == password:
            return teacher
    return None

# 🎓 Student Login
def student_login(username, password):
    try:
        with open("students.json", "r") as file:
            students = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    for student in students.get("students", []):
        if student["username"] == username and student["password"] == password:
            return student
    return None

# 🔍 Get teacher by username
def get_teacher_by_username(username):
    try:
        with open("teachers.json", "r") as f:
            data = json.load(f)
            for teacher in data.get("teachers", []):
                if teacher["username"] == username:
                    return teacher
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    return None

# 🆕 Teacher Signup (HOD only)
def teacher_signup(hod_verified=True, username=None, password=None, name=None, subjects=None):
    if not hod_verified or not username or not password or not name or not subjects:
        return {"success": False, "message": "Missing or unauthorized signup data."}

    if len(password) < 6:
        return {"success": False, "message": "Password too short."}

    new_teacher = {
        "username": username,
        "password": password,
        "name": name,
        "subjects": [s.strip() for s in subjects.split(",")]
    }

    try:
        with open("teachers.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"teachers": []}

    for teacher in data["teachers"]:
        if teacher["username"] == username:
            return {"success": False, "message": "Username already exists."}

    data["teachers"].append(new_teacher)

    with open("teachers.json", "w") as file:
        json.dump(data, file, indent=4)

    return {"success": True, "message": f"Teacher account for {name} created successfully."}

# 🔄 Unified Login Dispatcher
def login(role, username, password):
    if role == "admin":
        return admin_login(username, password)
    elif role == "teacher":
        return teacher_login(username, password)
    elif role == "student":
        return student_login(username, password)
    else:
        return None
