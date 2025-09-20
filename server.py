from flask import Flask, request, jsonify
from auth import login
from flask_cors import CORS
import json
import random
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import time
from datetime import datetime
from student import add_student
from assignment import add_assignment, submit_assignment, edit_assignment_by_fields, delete_assignment_by_fields
from assignment_views import view_submissions_by_id
from utils import get_student_by_class

load_dotenv()
app = Flask(__name__)
CORS(app)

# 🔐 Login Route
@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()
        role = data.get('role')
        username = data.get('username')
        password = data.get('password')

        user = login(role, username, password)
        if user:
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'admin_id': user.get('admin_id'),
                'name': user.get('name'),
                'role': role
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    except Exception as e:
        print("🔥 Error in /api/login:", e)
        return jsonify({'success': False, 'message': 'Server error'}), 500

# 📘 Get Student Info
@app.route('/api/student/<username>', methods=['GET'])
def get_student(username):
    admin_id = request.args.get("admin_id")
    try:
        with open("students.json", "r") as file:
            students = json.load(file)
            for student in students.get("students", []):
                if student["username"] == username and student.get("admin_id") == admin_id:
                    return jsonify(student)
        return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        print("🔥 Error in /api/student:", e)
        return jsonify({"error": "Server error"}), 500

# 🔄 Update Password
@app.route('/api/update-password', methods=['POST'])
def update_password():
    try:
        data = request.get_json()
        username = data.get("username")
        new_password = data.get("new_password")
        admin_id = data.get("admin_id")

        with open("students.json", "r") as f:
            students = json.load(f)

        updated = False
        for student in students["students"]:
            if student["username"] == username and student.get("admin_id") == admin_id:
                student["password"] = new_password
                updated = True
                break

        if updated:
            with open("students.json", "w") as f:
                json.dump(students, f, indent=4)
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "User not found"}), 404
    except Exception as e:
        print("🔥 Error in /api/update-password:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

# 🔐 OTP Store
otp_store = {}

# 📧 Email Sender
def send_email(to_email, otp):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")
    subject = "🔐 Your OTP Code"
    body = f"Hello,\n\nYour OTP code is: {otp}\nUse this to reset your password."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"🔥 Email sending failed: {e}")
        raise e

# 📩 Request OTP
@app.route('/api/request-otp', methods=['POST'])
def request_otp():
    try:
        data = request.get_json()
        role = data.get("role")
        username = data.get("username")
        email = data.get("email")

        print(f"🔧 Sending OTP to {email} for user {username} ({role})")

        if not role or not username or not email:
            return jsonify({"success": False, "message": "Missing fields"}), 400

        filename = f"{role}s.json"
        with open(filename, "r") as f:
            users = json.load(f).get(f"{role}s", [])

        user = next((u for u in users if u["username"].lower() == username.lower()), None)
        if not user or user.get("email", "").lower() != email.lower():
            return jsonify({"success": False, "message": "User not found or email mismatch"}), 404

        otp = str(random.randint(100000, 999999))
        otp_store[username] = {
            "otp": otp,
            "timestamp": time.time()
        }

        send_email(email, otp)
        return jsonify({"success": True, "message": "OTP sent to email"})
    except Exception as e:
        print("🔥 Error in /api/request-otp:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

# 🔁 Reset Password with OTP
@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        role = data.get("role")
        username = data.get("username")
        otp = data.get("otp")
        new_password = data.get("new_password")

        otp_entry = otp_store.get(username)

        if not otp_entry:
            return jsonify({"success": False, "message": "OTP not found"}), 404

        if time.time() - otp_entry["timestamp"] > 60:
            otp_store.pop(username, None)
            return jsonify({"success": False, "message": "OTP expired"}), 401

        if otp_entry["otp"] != otp:
            return jsonify({"success": False, "message": "Invalid OTP"}), 401

        filename = f"{role}s.json"
        with open(filename, "r") as f:
            users = json.load(f)

        updated = False
        for user in users.get(f"{role}s", []):
            if user["username"].lower() == username.lower():
                user["password"] = new_password
                updated = True
                break

        if updated:
            with open(filename, "w") as f:
                json.dump(users, f, indent=4)
            otp_store.pop(username, None)
            print(f"✅ Password updated for {username}")
            return jsonify({"success": True, "message": "Password updated successfully"})
        else:
            return jsonify({"success": False, "message": "User not found"}), 404
    except Exception as e:
        print("🔥 Error in /api/reset-password:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
@app.route('/api/admin-signup', methods=['POST'])
def admin_signup_api():
    try:
        data = request.get_json()
        username = data.get("username", "").strip().lower()
        password = data.get("password", "").strip()
        email = data.get("email", "").strip().lower()

        if not username or not password or not email:
            return jsonify({"success": False, "message": "All fields are required"}), 400

        if "@" not in email or "." not in email:
            return jsonify({"success": False, "message": "Invalid email format"}), 400

        try:
            with open("admins.json", "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"admins": []}

        admins = data.get("admins", [])
        for admin in admins:
            if admin["username"] == username:
                return jsonify({"success": False, "message": "Admin already exists"}), 409

        admins.append({
            "username": username,
            "password": password,
            "email": email,
            "admin_id": username  # using username as admin_id
        })

        with open("admins.json", "w") as f:
            json.dump({"admins": admins}, f, indent=2)

        print(f"✅ New admin registered: {username}")
        return jsonify({"success": True, "message": "Admin signup successful", "admin_id": username})
    except Exception as e:
        print("🔥 Error in /api/admin-signup:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

@app.route("/api/add-student", methods=["POST"])
def api_add_student():
    try:
        data = request.get_json()
        admin_id = data.get("admin_id")
        with open("students.json", "r") as f:
            students = json.load(f).get("students", [])

        for s in students:
            if s["id"] == data["id"] or s["username"].lower() == data["username"].lower():
                return jsonify({"success": False, "message": "❌ Student already exists."})

        data["admin_id"] = admin_id
        students.append(data)
        with open("students.json", "w") as f:
            json.dump({"students": students}, f, indent=4)

        return jsonify({"success": True, "message": "✅ Student added successfully."})
    except Exception as e:
        print("🔥 Error in /api/add-student:", e)
        return jsonify({"success": False, "message": "❌ Failed to add student."})

@app.route("/api/students/<class_name>", methods=["GET"])
def get_students_by_class(class_name):
    admin_id = request.args.get("admin_id")
    try:
        with open("students.json", "r") as f:
            students = json.load(f).get("students", [])
        filtered = [s for s in students if s["class"].lower() == class_name.lower() and s.get("admin_id") == admin_id]
        return jsonify({"students": filtered})
    except:
        return jsonify({"students": []})

@app.route("/api/search-student", methods=["POST"])
def search_student_api():
    data = request.get_json()
    query = data.get("query", "").strip().lower()
    search_type = data.get("type")
    admin_id = data.get("admin_id")

    try:
        with open("students.json", "r") as f:
            students = json.load(f).get("students", [])
    except:
        return jsonify({"success": False})

    if search_type == "id":
        try:
            query_id = int(query)
            for s in students:
                if s["id"] == query_id and s.get("admin_id") == admin_id:
                    return jsonify({"success": True, "student": s})
        except:
            return jsonify({"success": False})
    elif search_type == "name":
        for s in students:
            if query in s["name"].lower() and s.get("admin_id") == admin_id:
                return jsonify({"success": True, "student": s})

    return jsonify({"success": False})

@app.route("/api/edit-student", methods=["PUT"])
def edit_student_api():
    data = request.get_json()
    student_id = data.get("id")
    admin_id = data.get("admin_id")
    try:
        with open("students.json", "r") as f:
            students = json.load(f).get("students", [])
        for s in students:
            if s["id"] == student_id and s.get("admin_id") == admin_id:
                s["name"] = data.get("name", s["name"])
                s["class"] = data.get("class", s["class"])
                s["email"] = data.get("email", s["email"])
                with open("students.json", "w") as f:
                    json.dump({"students": students}, f, indent=4)
                return jsonify({"success": True, "message": "✅ Student updated."})
    except:
        pass
    return jsonify({"success": False, "message": "❌ Update failed."})
@app.route("/api/delete-student", methods=["DELETE"])
def delete_student_api():
    data = request.get_json()
    student_id = data.get("id")
    admin_id = data.get("admin_id")
    try:
        with open("students.json", "r") as f:
            students = json.load(f).get("students", [])
        students = [s for s in students if not (s["id"] == student_id and s.get("admin_id") == admin_id)]
        with open("students.json", "w") as f:
            json.dump({"students": students}, f, indent=4)
        return jsonify({"success": True, "message": "✅ Student deleted."})
    except:
        return jsonify({"success": False, "message": "❌ Deletion failed."})

@app.route("/api/add-teacher", methods=["POST"])
def add_teacher_api():
    try:
        data = request.get_json()
        admin_id = data.get("admin_id")
        with open("teachers.json", "r") as f:
            teachers = json.load(f).get("teachers", [])

        for t in teachers:
            if t["username"].lower() == data["username"].lower() and t.get("admin_id") == admin_id:
                return jsonify({"success": False, "message": "❌ Teacher already exists."})

        data["admin_id"] = admin_id
        teachers.append(data)
        with open("teachers.json", "w") as f:
            json.dump({"teachers": teachers}, f, indent=4)

        return jsonify({"success": True, "message": "✅ Teacher added successfully."})
    except Exception as e:
        print("🔥 Error in /api/add-teacher:", e)
        return jsonify({"success": False, "message": "❌ Failed to add teacher."})

@app.route("/api/teachers", methods=["GET"])
def get_all_teachers():
    admin_id = request.args.get("admin_id")
    try:
        with open("teachers.json", "r") as f:
            teachers = json.load(f).get("teachers", [])
        filtered = [t for t in teachers if t.get("admin_id") == admin_id]
        return jsonify({"teachers": filtered})
    except:
        return jsonify({"teachers": []})

@app.route("/api/search-teacher", methods=["POST"])
def search_teacher_api():
    data = request.get_json()
    query = data.get("query", "").strip().lower()
    admin_id = data.get("admin_id")

    try:
        with open("teachers.json", "r") as f:
            teachers = json.load(f).get("teachers", [])
    except:
        return jsonify({"success": False})

    for t in teachers:
        if (query in t["name"].lower() or query == t["username"].lower()) and t.get("admin_id") == admin_id:
            return jsonify({"success": True, "teacher": t})

    return jsonify({"success": False})

@app.route("/api/edit-teacher", methods=["PUT"])
def edit_teacher_api():
    data = request.get_json()
    username = data.get("username", "").strip().lower()
    admin_id = data.get("admin_id")

    try:
        with open("teachers.json", "r") as f:
            teachers = json.load(f).get("teachers", [])

        for t in teachers:
            if t["username"].lower() == username and t.get("admin_id") == admin_id:
                t["name"] = data.get("name", t["name"])
                t["email"] = data.get("email", t["email"])
                t["department"] = data.get("department", t["department"])
                t["post"] = data.get("post", t["post"])
                t["subject"] = data.get("subject", t["subject"])
                t["class_list"] = data.get("class_list", t["class_list"])
                break
        else:
            return jsonify({"success": False, "message": "❌ Teacher not found."})

        with open("teachers.json", "w") as f:
            json.dump({"teachers": teachers}, f, indent=4)

        return jsonify({"success": True, "message": "✅ Teacher updated."})
    except:
        return jsonify({"success": False, "message": "❌ Update failed."})

@app.route("/api/delete-teacher", methods=["DELETE"])
def delete_teacher_api():
    data = request.get_json()
    username = data.get("username", "").strip().lower()
    admin_id = data.get("admin_id")

    try:
        with open("teachers.json", "r") as f:
            teachers = json.load(f).get("teachers", [])

        updated_teachers = [t for t in teachers if not (t["username"].lower() == username and t.get("admin_id") == admin_id)]

        if len(updated_teachers) == len(teachers):
            return jsonify({"success": False, "message": "❌ Teacher not found."})

        with open("teachers.json", "w") as f:
            json.dump({"teachers": updated_teachers}, f, indent=4)

        return jsonify({"success": True, "message": "✅ Teacher deleted."})
    except:
        return jsonify({"success": False, "message": "❌ Deletion failed."})

@app.route('/api/add-assignment', methods=['POST'])
def api_add_assignment():
    data = request.get_json()
    add_assignment(data["class"], data["subject"], data["deadline"], data["admin_id"])
    return jsonify({"success": True})

@app.route('/api/submit-assignment', methods=['POST'])
def api_submit_assignment():
    data = request.get_json()
    subject = data["subject"]
    admin_id = data.get("admin_id")
    submitted_ids = []
    skipped_ids = []

    for student_id in data["student_ids"]:
        existing = view_submissions_by_id(student_id, subject_filter=subject, admin_id=admin_id)
        if not existing:
            submit_assignment(student_id, subject, admin_id)
            submitted_ids.append(student_id)
        else:
            skipped_ids.append(student_id)

    return jsonify({
        "success": True,
        "submitted_ids": submitted_ids,
        "skipped_ids": skipped_ids
    })

@app.route('/api/class-assignments', methods=['GET'])
def get_class_assignments():
    class_name = request.args.get("class")
    admin_id = request.args.get("admin_id")
    with open("assignments.json", "r") as f:
        data = json.load(f)
    filtered = [a for a in data if a["class"] == class_name and a.get("admin_id") == admin_id]
    return jsonify(filtered)

@app.route('/api/class-students', methods=['GET'])
def get_class_students():
    class_name = request.args.get("class")
    subject = request.args.get("subject")  # ✅ NEW: subject filter

    with open("students.json", "r") as f:
        students = json.load(f)["students"]

    filtered = [
        s for s in students
        if s.get("class", "").strip().lower() == class_name.strip().lower()
    ]

    result = []
    for student in filtered:
        submitted = False
        if subject:
            subs = view_submissions_by_id(student["id"], subject_filter=subject)
            submitted = bool(subs)
        result.append({
            "id": student["id"],
            "name": student["name"],
            "class": student["class"],
            "submitted": submitted  # ✅ NEW: submission status
        })

    return jsonify(result)

@app.route('/api/view-submissions', methods=['GET'])
def api_view_submissions():
    class_name = request.args.get("class")
    subject = request.args.get("subject")

    with open("students.json", "r") as f:
        students = json.load(f)["students"]

    filtered = [
        s for s in students
        if s["class"].strip().lower() == class_name.strip().lower()
    ]

    result = []
    for student in filtered:
        subs = view_submissions_by_id(student["id"], subject_filter=subject)
        if subs:
            result.append({
                "name": student["name"],
                "id": student["id"],
                "submitted_on": subs[0]["date"]
            })

    return jsonify(result)

@app.route('/api/edit-assignment', methods=['PATCH'])
def api_edit_assignment():
    data = request.get_json()
    print("🛠️ Edit request received:", data)
    success = edit_assignment_by_fields(
        data["class"],
        data["subject"],
        data["deadline"],
        {
            "class": data.get("new_class"),
            "subject": data.get("new_subject"),
            "deadline": data.get("new_deadline")
        }
    )
    return jsonify({"success": success})

@app.route('/api/delete-assignment', methods=['DELETE'])
def api_delete_assignment():
    data = request.get_json()
    print("🗑️ Delete request received:", data)
    success = delete_assignment_by_fields(
        data["class"],
        data["subject"],
        data["deadline"]
    )
    return jsonify({"success": success})
def convert_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").strftime("%d-%m-%Y")
    except ValueError:
        return None

# 🔧 Helper: View test marks by student ID
def view_test_marks_by_id(student_id, subject_filter="", date_filter=""):
    try:
        with open("marks.json", "r") as f:
            marks = json.load(f)
    except:
        return []

    filtered = [m for m in marks if str(m.get("student_id")) == str(student_id)]

    if subject_filter:
        filtered = [m for m in filtered if m.get("subject", "").strip().lower() == subject_filter.strip().lower()]
    if date_filter:
        filtered = [m for m in filtered if m.get("date", "").strip() == date_filter.strip()]

    return filtered

@app.route('/api/schedule-test', methods=['POST'])
def schedule_test_api():
    try:
        data = request.get_json()
        class_name = data.get("class", "").strip()
        subject = data.get("subject", "").strip()
        test_date = data.get("date", "").strip()
        max_marks = data.get("max_marks")

        if not class_name or not subject or not test_date or max_marks is None:
            return jsonify({"success": False, "message": "Missing fields"}), 400

        try:
            datetime.strptime(test_date, "%d-%m-%Y")
        except ValueError:
            return jsonify({"success": False, "message": "Invalid date format"}), 400

        try:
            max_marks = int(max_marks)
            if max_marks <= 0:
                return jsonify({"success": False, "message": "Max marks must be positive"}), 400
        except:
            return jsonify({"success": False, "message": "Invalid marks input"}), 400

        try:
            with open("tests.json", "r", encoding="utf-8") as f:
                tests = json.load(f)
        except:
            tests = []

        for t in tests:
            if t["class"].strip().lower() == class_name.lower() and \
               t["subject"].strip().lower() == subject.lower() and \
               t["date"].strip() == test_date:
                return jsonify({"success": False, "message": "Test already scheduled"}), 409

        tests.append({
            "class": class_name,
            "subject": subject,
            "date": test_date,
            "max_marks": max_marks
        })

        with open("tests.json", "w", encoding="utf-8") as f:
            json.dump(tests, f, indent=4)

        return jsonify({"success": True, "message": "✅ Test scheduled successfully"})
    except Exception as e:
        print("🔥 Error in /api/schedule-test:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
      
@app.route('/api/scheduled-tests', methods=['GET'])
def get_scheduled_tests():
    class_name = request.args.get("class", "").strip()
    admin_id = request.args.get("admin_id")

    if not class_name or not admin_id:
        return jsonify({"success": False, "message": "Missing class name or admin ID"}), 400

    try:
        with open("tests.json", "r", encoding="utf-8") as f:
            tests = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({"success": False, "message": "Could not load test data"}), 500

    filtered = [
        t for t in tests
        if t.get("class", "").strip().lower() == class_name.lower()
        and t.get("admin_id") == admin_id
    ]
    filtered.sort(key=lambda t: datetime.strptime(t["date"], "%d-%m-%Y"))

    return jsonify({"success": True, "tests": filtered})

@app.route('/api/save-marks', methods=['POST'])
def api_save_marks():
    try:
        data = request.get_json()
        subject = data.get("subject", "").strip()
        test_date = data.get("date", "").strip()
        marks_data = data.get("marks_data", [])
        admin_id = data.get("admin_id")

        if not subject or not test_date or not marks_data or not admin_id:
            return jsonify({"success": False, "message": "Missing fields"}), 400

        try:
            datetime.strptime(test_date, "%d-%m-%Y")
        except ValueError:
            return jsonify({"success": False, "message": "Invalid date format"}), 400

        try:
            with open("tests.json", "r", encoding="utf-8") as f:
                tests = json.load(f)
        except:
            tests = []

        test_info = next(
            (t for t in tests if t["subject"].strip().lower() == subject.lower()
             and t["date"].strip() == test_date
             and t.get("admin_id") == admin_id),
            None
        )

        if not test_info:
            return jsonify({"success": False, "message": "Test not found"}), 404

        test_class = test_info["class"]
        max_marks = test_info.get("max_marks")

        try:
            with open("marks.json", "r", encoding="utf-8") as f:
                existing = json.load(f)
        except:
            existing = []

        existing_keys = {(m["student_id"], m["subject"], m["date"], m.get("admin_id")) for m in existing}
        new_entries = []

        for entry in marks_data:
            key = (entry["student_id"], subject, test_date, admin_id)
            if key in existing_keys:
                continue
            try:
                marks = float(entry["marks"])
                if marks < 0 or marks > max_marks:
                    continue
            except:
                continue
            if test_class.strip().lower() != entry.get("class", "").strip().lower():
                print(f"⚠️ Class mismatch for student {entry['student_id']}: {entry.get('class')} vs expected {test_class}")
                continue

            new_entries.append({
                "student_id": entry["student_id"],
                "name": entry["name"],
                "subject": subject,
                "date": test_date,
                "marks": marks,
                "max_marks": max_marks,
                "class": test_class,
                "submitted": True,
                "admin_id": admin_id
            })

        existing.extend(new_entries)

        with open("marks.json", "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=4)

        for test in tests:
            if (
                test["class"].strip().lower() == test_class.strip().lower() and
                test["subject"].strip().lower() == subject.strip().lower() and
                test["date"].strip() == test_date.strip() and
                test.get("admin_id") == admin_id
            ):
                test["submitted"] = True
                break

        with open("tests.json", "w", encoding="utf-8") as f:
            json.dump(tests, f, indent=4)

        return jsonify({
            "success": True,
            "added": len(new_entries),
            "skipped": len(marks_data) - len(new_entries)
        })
    except Exception as e:
        print("🔥 Error in /api/save-marks:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

@app.route('/api/subject-marks', methods=['GET'])
def api_subject_marks():
    class_name = request.args.get("class", "").strip().lower()
    subject = request.args.get("subject", "").strip().lower()
    test_date = request.args.get("date", "").strip()
    admin_id = request.args.get("admin_id")

    if not class_name or not subject or not test_date or not admin_id:
        return jsonify({"success": False, "message": "Missing fields"}), 400

    try:
        datetime.strptime(test_date, "%d-%m-%Y")
    except ValueError:
        return jsonify({"success": False, "message": "Invalid date format"}), 400

    try:
        with open("marks.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        print("🔥 Failed to load marks.json:", e)
        return jsonify({"success": False, "message": "No marks data found"}), 404

    found = [
        m for m in data
        if m.get("class", "").strip().lower() == class_name and
           m.get("subject", "").strip().lower() == subject and
           m.get("date", "").strip() == test_date and
           m.get("admin_id") == admin_id
    ]

    if not found:
        return jsonify({"success": True, "marks": [], "analytics": {}})

    try:
        with open("students.json", "r") as f:
            student_data = json.load(f).get("students", [])
            student_lookup = {
                int(s["id"]): s["name"]
                for s in student_data
                if s.get("admin_id") == admin_id
            }
    except Exception as e:
        print("⚠️ Failed to load student names:", e)
        student_lookup = {}

    try:
        scores = [m.get("marks") for m in found if isinstance(m.get("marks"), (int, float))]
        average = round(sum(scores) / len(scores), 2) if scores else 0
        highest = max(scores) if scores else 0
        lowest = min(scores) if scores else 0

        top_entry = next((m for m in found if m.get("marks") == highest), None)
        top_id = int(top_entry.get("student_id")) if top_entry else None
        top_scorer = {
            "name": student_lookup.get(top_id, "Unknown"),
            "student_id": top_entry.get("student_id")
        } if top_entry else {}
    except Exception as e:
        print("🔥 Error calculating analytics:", e)
        return jsonify({"success": False, "message": "Invalid marks data"}), 500

    return jsonify({
        "success": True,
        "subject": subject,
        "date": test_date,
        "marks": found,
        "analytics": {
            "average": average,
            "highest": highest,
            "top_scorer": top_scorer,
            "lowest": lowest
        }
    })

@app.route('/api/student-marks', methods=['GET'])
def api_student_marks():
    query = request.args.get("query", "").strip().lower()
    subject_filter = request.args.get("subject", "").strip().lower()
    admin_id = request.args.get("admin_id")

    if not query or not admin_id:
        return jsonify({"success": False, "message": "Missing student query or admin ID"}), 400

    # Load students
    try:
        with open("students.json", "r") as f:
            students_data = json.load(f)["students"]
    except:
        return jsonify({"success": False, "message": "Student data not found"}), 500

    # Load marks
    try:
        with open("marks.json", "r") as f:
            marks_data = json.load(f)
    except:
        marks_data = []

    # Load tests
    try:
        with open("tests.json", "r") as f:
            tests_data = json.load(f)
    except:
        tests_data = []

    # Find student (match by ID or name, scoped by admin)
    student = None
    for s in students_data:
        if s.get("admin_id") != admin_id:
            continue
        sid = str(s.get("id", "")).strip().lower()
        name = s.get("name", "").strip().lower()
        if query == sid or query == name:
            student = s
            break

    if not student:
        return jsonify({"success": False, "message": "Student not found in records"}), 404

    student_id = str(student.get("id")).strip().lower()
    student_class = student.get("class", "").strip().lower()

    # Filter marks for this student
    student_marks = []
    for m in marks_data:
        if str(m.get("student_id", "")).strip().lower() != student_id:
            continue
        if m.get("admin_id") != admin_id:
            continue
        if subject_filter and m.get("subject", "").strip().lower() != subject_filter:
            continue

        student_marks.append({
            "subject": m.get("subject", "Unknown"),
            "date": m.get("date", "Unknown"),
            "marks": m.get("marks", 0),
            "max_marks": m.get("max_marks", "N/A")
        })

    if student_marks:
        return jsonify({
            "success": True,
            "student": {
                "id": student.get("id"),
                "name": student.get("name")
            },
            "marks": student_marks
        })

    # Check if test was scheduled for this student’s class
    test_found = False
    for t in tests_data:
        if t.get("admin_id") != admin_id:
            continue
        t_class = t.get("class", "").strip().lower()
        t_subject = t.get("subject", "").strip().lower()
        if t_class == student_class and (not subject_filter or t_subject == subject_filter):
            test_found = True
            break

    if test_found:
        return jsonify({
            "success": False,
            "message": "Test scheduled but not attempted",
            "student": {
                "id": student.get("id"),
                "name": student.get("name")
            }
        }), 404

    return jsonify({
        "success": False,
        "message": "No test scheduled for this student",
        "student": {
            "id": student.get("id"),
            "name": student.get("name")
        }
    }), 404

@app.route('/api/edit-test', methods=['PATCH'])
def edit_test_api():
    try:
        data = request.get_json()
        print("📦 Incoming edit payload:", data)

        admin_id = data.get("admin_id")
        if not admin_id:
            return jsonify({"success": False, "message": "Missing admin ID"}), 400

        # Original values for matching
        original_subject = data.get("original_subject", "").strip().lower()
        original_date = data.get("original_date", "").strip()
        original_class = data.get("original_class", "").strip().lower()

        # New values to update
        new_subject = data.get("subject", "").strip()
        new_date = data.get("date", "").strip()
        new_class = data.get("class", "").strip().lower()
        new_max = data.get("new_max_marks")

        if not original_subject or not original_date or not original_class or \
           not new_subject or not new_date or new_max is None or not new_class:
            return jsonify({"success": False, "message": "Missing fields"}), 400

        try:
            parsed_date = datetime.strptime(new_date, "%d-%m-%Y")
            new_date = parsed_date.strftime("%d-%m-%Y")
        except ValueError:
            return jsonify({"success": False, "message": "Invalid date format"}), 400

        try:
            new_max = int(new_max)
            if new_max <= 0:
                raise ValueError
        except:
            return jsonify({"success": False, "message": "Invalid max marks"}), 400

        # Load and update tests.json
        try:
            with open("tests.json", "r") as f:
                tests = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return jsonify({"success": False, "message": "No test data found"}), 404

        updated = False
        for test in tests:
            test_subject = test.get("subject", "").strip().lower()
            test_date = test.get("date", "").strip()
            test_class = test.get("class", "").strip().lower()

            if test_subject == original_subject and test_date == original_date and \
               test_class == original_class and test.get("admin_id") == admin_id:
                print("✅ Match found in tests.json. Updating...")
                test["subject"] = new_subject
                test["date"] = new_date
                test["class"] = new_class
                test["max_marks"] = new_max
                updated = True
                break

        if not updated:
            print(f"❌ No matching test found for: {original_subject} | {original_date} | {original_class}")
            return jsonify({"success": False, "message": "Test not found"}), 404

        with open("tests.json", "w") as f:
            json.dump(tests, f, indent=4)

        # 🔄 Sync marks.json
        try:
            with open("marks.json", "r") as f:
                marks_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            marks_data = []

        sync_count = 0
        for entry in marks_data:
            entry_subject = entry.get("subject", "").strip().lower()
            entry_date = entry.get("date", "").strip()
            entry_class = entry.get("class", "").strip().lower()

            if entry_subject == original_subject and entry_date == original_date and \
               entry_class == original_class and entry.get("admin_id") == admin_id:
                entry["subject"] = new_subject
                entry["date"] = new_date
                entry["class"] = new_class
                entry["max_marks"] = new_max
                sync_count += 1

        with open("marks.json", "w") as f:
            json.dump(marks_data, f, indent=4)

        print(f"✅ Synced {sync_count} marks entries for test: {new_subject} on {new_date}")

        return jsonify({
            "success": True,
            "message": f"✅ Test updated successfully. Synced {sync_count} mark entries."
        })

    except Exception as e:
        print("🔥 Error in /api/edit-test:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
        
@app.route('/api/delete-test', methods=['DELETE'])
def delete_test_api():
    try:
        data = request.get_json()
        subject = data.get("subject", "").strip()
        date = data.get("date", "").strip()
        class_name = data.get("class", "").strip().lower()
        admin_id = data.get("admin_id")

        if not subject or not date or not class_name or not admin_id:
            return jsonify({"success": False, "message": "Missing subject, date, class or admin ID"}), 400

        try:
            parsed_date = datetime.strptime(date, "%d-%m-%Y")
            date = parsed_date.strftime("%d-%m-%Y")
        except ValueError:
            return jsonify({"success": False, "message": "Invalid date format"}), 400

        try:
            with open("tests.json", "r") as f:
                tests = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return jsonify({"success": False, "message": "No test data found"}), 404

        original_len = len(tests)
        tests = [
            t for t in tests
            if not (
                t["subject"].lower() == subject.lower() and
                t["date"] == date and
                t["class"].strip().lower() == class_name and
                t.get("admin_id") == admin_id
            )
        ]

        if len(tests) == original_len:
            return jsonify({"success": False, "message": "Test not found"}), 404

        with open("tests.json", "w") as f:
            json.dump(tests, f, indent=4)

        return jsonify({"success": True, "message": "🗑️ Test deleted successfully"})
    except Exception as e:
        print("🔥 Error in /api/delete-test:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
@app.route('/api/edit-marks', methods=['PATCH'])
def edit_marks_api():
    try:
        data = request.get_json()
        student_id = str(data.get("student_id", "")).strip()
        subject = data.get("subject", "").strip()
        date = data.get("date", "").strip()
        new_marks = data.get("new_marks")
        admin_id = data.get("admin_id")

        if not student_id or not subject or not date or new_marks is None or not admin_id:
            return jsonify({"success": False, "message": "Missing fields"}), 400

        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d")
            date = parsed_date.strftime("%d-%m-%Y")
        except ValueError:
            return jsonify({"success": False, "message": "Invalid date format"}), 400

        try:
            new_marks = float(new_marks)
            if new_marks < 0:
                raise ValueError
        except:
            return jsonify({"success": False, "message": "Invalid marks"}), 400

        try:
            with open("marks.json", "r") as f:
                marks_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return jsonify({"success": False, "message": "No marks data found"}), 404

        updated = False
        for m in marks_data:
            if str(m["student_id"]) == student_id and \
               m["subject"].lower() == subject.lower() and \
               m["date"] == date and \
               m.get("admin_id") == admin_id:
                m["marks"] = new_marks
                updated = True
                break

        if not updated:
            return jsonify({"success": False, "message": "Marks entry not found"}), 404

        with open("marks.json", "w") as f:
            json.dump(marks_data, f, indent=4)

        return jsonify({"success": True, "message": "✏️ Marks updated successfully"})
    except Exception as e:
        print("🔥 Error in /api/edit-marks:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

@app.route('/api/delete-marks', methods=['POST'])
def delete_marks_api():
    try:
        data = request.get_json(force=True)
        print("📦 Incoming DELETE payload:", data)

        student_id = str(data.get("student_id", "")).strip()
        subject = data.get("subject", "").strip()
        date = data.get("date", "").strip()
        admin_id = data.get("admin_id")

        if not student_id or not subject or not date or not admin_id:
            return jsonify({"success": False, "message": "Missing fields"}), 400

        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d")
            date = parsed_date.strftime("%d-%m-%Y")
        except ValueError:
            return jsonify({"success": False, "message": "Invalid date format"}), 400

        try:
            with open("marks.json", "r") as f:
                marks_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return jsonify({"success": False, "message": "No marks data found"}), 404

        original_len = len(marks_data)
        marks_data = [
            m for m in marks_data
            if not (
                str(m.get("student_id", "")).strip() == student_id and
                m.get("subject", "").strip().lower() == subject.lower() and
                m.get("date", "").strip() == date and
                m.get("admin_id") == admin_id
            )
        ]

        if len(marks_data) == original_len:
            return jsonify({"success": False, "message": "Marks entry not found"}), 404

        with open("marks.json", "w") as f:
            json.dump(marks_data, f, indent=4)

        return jsonify({"success": True, "message": "🗑️ Marks deleted successfully"})

    except Exception as e:
        print("🔥 Error in /api/delete-marks:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
@app.route('/api/class-students', methods=['GET'])
def api_class_students():
    class_name = request.args.get("class", "").strip().lower()
    subject = request.args.get("subject", "").strip().lower()
    test_date = request.args.get("date", "").strip()
    admin_id = request.args.get("admin_id")

    if not class_name or not subject or not test_date or not admin_id:
        return jsonify({"success": False, "message": "Missing parameters"}), 400

    try:
        datetime.strptime(test_date, "%d-%m-%Y")
    except ValueError:
        return jsonify({"success": False, "message": "Invalid date format"}), 400

    try:
        with open("students.json", "r") as f:
            students_data = json.load(f)["students"]
    except:
        return jsonify({"success": False, "message": "Student data not found"}), 500

    try:
        with open("marks.json", "r") as f:
            marks_data = json.load(f)
    except:
        marks_data = []

    filtered_students = [
        s for s in students_data
        if s.get("class", "").strip().lower() == class_name and s.get("admin_id") == admin_id
    ]

    response = []
    for s in filtered_students:
        sid = str(s.get("id")).strip()
        name = s.get("name")

        student_entry = {
            "id": sid,
            "student_id": sid,
            "name": name,
            "submitted": False,
            "marks": None,
            "max_marks": None
        }

        for m in marks_data:
            if (
                str(m.get("student_id")) == sid and
                m.get("subject", "").strip().lower() == subject and
                m.get("date", "").strip() == test_date and
                m.get("class", "").strip().lower() == class_name and
                m.get("admin_id") == admin_id
            ):
                student_entry["submitted"] = m.get("submitted", True)
                try:
                    student_entry["marks"] = int(float(m.get("marks", 0)))
                except:
                    student_entry["marks"] = None
                student_entry["max_marks"] = m.get("max_marks")
                break

        response.append(student_entry)

    return jsonify({"success": True, "students": response})

@app.route('/api/classes', methods=['GET'])
def get_classes():
    admin_id = request.args.get("admin_id")
    if not admin_id:
        return jsonify({"success": False, "message": "Missing admin ID"}), 400

    try:
        with open("students.json", "r") as f:
            students_data = json.load(f)["students"]
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({"success": False, "message": "Student data not found"}), 500

    classes = sorted(set(
        s.get("class", "").strip()
        for s in students_data
        if s.get("class") and s.get("admin_id") == admin_id
    ))

    return jsonify({"success": True, "classes": classes})

# 🚀 Run Server
if __name__ == '__main__':
    app.run(port=5000)
