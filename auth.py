import json

# 🔐 Admin Login
def admin_login(username, password):
    print(f"🔐 Checking admin credentials for {username}")
    try:
        with open("admins.json", "r") as file:
            admins = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    for admin in admins.get("admins", []):
        if admin["username"] == username and admin["password"] == password:
            return admin  # ✅ Includes admin_id
    return None

# 🔄 Student Password Update (Scoped by admin)
def update_student_password(username, old_pass, new_pass, admin_id):
    try:
        with open("students.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    for student in data.get("students", []):
        if (
            student["username"] == username and
            student["password"] == old_pass and
            student.get("admin_id") == admin_id
        ):
            student["password"] = new_pass
            with open("students.json", "w") as f:
                json.dump(data, f, indent=4)
            return True
    return False

# 👨‍🏫 Teacher Login (Scoped by admin)
def teacher_login(username, password, admin_id):
    try:
        with open("teachers.json", "r") as file:
            raw = json.load(file)
            teachers = raw if isinstance(raw, dict) else {"teachers": raw}
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    for teacher in teachers.get("teachers", []):
        if (
            teacher["username"] == username and
            teacher["password"] == password and
            teacher.get("admin_id") == admin_id
        ):
            return teacher
    return None

# 🎓 Student Login (Scoped by admin)
def student_login(username, password, admin_id):
    try:
        with open("students.json", "r") as file:
            students = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    for student in students.get("students", []):
        if (
            student["username"] == username and
            student["password"] == password and
            student.get("admin_id") == admin_id
        ):
            return student
    return None

# 🔍 Get teacher by username (Scoped by admin)
def get_teacher_by_username(username, admin_id):
    try:
        with open("teachers.json", "r") as f:
            data = json.load(f)
            for teacher in data.get("teachers", []):
                if teacher["username"] == username and teacher.get("admin_id") == admin_id:
                    return teacher
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    return None

# 🆕 Teacher Signup (HOD only, tagged with admin_id)
def teacher_signup(admin_id, hod_verified=True, username=None, password=None, name=None, subjects=None):
    if not hod_verified or not username or not password or not name or not subjects:
        return {"success": False, "message": "Missing or unauthorized signup data."}

    if len(password) < 6:
        return {"success": False, "message": "Password too short."}

    new_teacher = {
        "username": username,
        "password": password,
        "name": name,
        "subjects": [s.strip() for s in subjects.split(",")],
        "admin_id": admin_id  # ✅ Tag teacher with admin_id
    }

    try:
        with open("teachers.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"teachers": []}

    for teacher in data["teachers"]:
        if teacher["username"] == username and teacher.get("admin_id") == admin_id:
            return {"success": False, "message": "Username already exists."}

    data["teachers"].append(new_teacher)

    with open("teachers.json", "w") as file:
        json.dump(data, file, indent=4)

    return {"success": True, "message": f"Teacher account for {name} created successfully."}

def login(role, username, password, admin_id=None):
    print(f"🔍 Login attempt → role: {role}, username: {username}, password: {password}, admin_id: {admin_id}")

    if role == "admin":
        return admin_login(username, password)

    elif role == "teacher":
        try:
            with open("teachers.json", "r") as file:
                data = json.load(file)
                for teacher in data.get("teachers", []):
                    if teacher["username"] == username and teacher["password"] == password:
                        return teacher  # ✅ Found teacher, admin_id included
        except (FileNotFoundError, json.JSONDecodeError):
            return None
        return None

    elif role == "student":
        try:
            with open("students.json", "r") as file:
                data = json.load(file)
                for student in data.get("students", []):
                    if student["username"] == username and student["password"] == password:
                        return student  # ✅ Found student, admin_id included
        except (FileNotFoundError, json.JSONDecodeError):
            return None
        return None

    return None