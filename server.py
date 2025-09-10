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
from student import add_student  
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
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    except Exception as e:
        print("🔥 Error in /api/login:", e)
        return jsonify({'success': False, 'message': 'Server error'}), 500

# 📘 Get Student Info
@app.route('/api/student/<username>', methods=['GET'])
def get_student(username):
    try:
        with open("students.json", "r") as file:
            students = json.load(file)
            for student in students.get("students", []):
                if student["username"] == username:
                    return jsonify(student)
        return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        print("🔥 Error in /api/student:", e)
        return jsonify({"error": "Server error"}), 500

# 🔄 Update Password (Direct)
@app.route('/api/update-password', methods=['POST'])
def update_password():
    try:
        data = request.get_json()
        username = data.get("username")
        new_password = data.get("new_password")

        with open("students.json", "r") as f:
            students = json.load(f)

        updated = False
        for student in students["students"]:
            if student["username"] == username:
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
otp_store = {}  # Format: { "username": { "otp": "123456", "timestamp": 1694350000 } }

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
            "timestamp": time.time()  # current time in seconds
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

        # ⏳ Check if OTP is expired (1 minute = 60 seconds)
        if time.time() - otp_entry["timestamp"] > 60:
            otp_store.pop(username, None)  # Clean up expired OTP
            return jsonify({"success": False, "message": "OTP expired"}), 401

        # 🔐 Check if OTP matches
        if otp_entry["otp"] != otp:
            return jsonify({"success": False, "message": "Invalid OTP"}), 401

        # ✅ Proceed with password update
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
            otp_store.pop(username, None)  # Clean up after success
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

        # Load or initialize admins.json
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
            "email": email
        })

        with open("admins.json", "w") as f:
            json.dump({"admins": admins}, f, indent=2)

        print(f"✅ New admin registered: {username}")
        return jsonify({"success": True, "message": "Admin signup successful"})
    except Exception as e:
        print("🔥 Error in /api/admin-signup:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    
@app.route("/api/add-student", methods=["POST"])
def api_add_student():
    try:
        data = request.get_json()
        with open("students.json", "r") as f:
            students = json.load(f).get("students", [])

        # Check for duplicate ID or username
        for s in students:
            if s["id"] == data["id"] or s["username"].lower() == data["username"].lower():
                return jsonify({"success": False, "message": "❌ Student already exists."})

        students.append(data)
        with open("students.json", "w") as f:
            json.dump({"students": students}, f, indent=4)

        return jsonify({"success": True, "message": "✅ Student added successfully."})
    except Exception as e:
        print("🔥 Error in /api/add-student:", e)
        return jsonify({"success": False, "message": "❌ Failed to add student."})

@app.route("/api/classes", methods=["GET"])
def get_classes():
    try:
        with open("students.json", "r") as f:
            students = json.load(f).get("students", [])
        classes = sorted(set(s["class"] for s in students))
        return jsonify({"classes": classes})
    except:
        return jsonify({"classes": []})

@app.route("/api/students/<class_name>", methods=["GET"])
def get_students_by_class(class_name):
    try:
        with open("students.json", "r") as f:
            students = json.load(f).get("students", [])
        filtered = [s for s in students if s["class"].lower() == class_name.lower()]
        return jsonify({"students": filtered})
    except:
        return jsonify({"students": []})

@app.route("/api/search-student", methods=["POST"])
def search_student_api():
    data = request.get_json()
    query = data.get("query", "").strip().lower()
    search_type = data.get("type")

    try:
        with open("students.json", "r") as f:
            students = json.load(f).get("students", [])
    except:
        return jsonify({"success": False})

    if search_type == "id":
        try:
            query_id = int(query)
            for s in students:
                if s["id"] == query_id:
                    return jsonify({"success": True, "student": s})
        except:
            return jsonify({"success": False})
    elif search_type == "name":
        for s in students:
            if query in s["name"].lower():
                return jsonify({"success": True, "student": s})

    return jsonify({"success": False})
@app.route("/api/edit-student", methods=["PUT"])
def edit_student_api():
    data = request.get_json()
    student_id = data.get("id")
    try:
        with open("students.json", "r") as f:
            students = json.load(f).get("students", [])
        for s in students:
            if s["id"] == student_id:
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
    try:
        with open("students.json", "r") as f:
            students = json.load(f).get("students", [])
        students = [s for s in students if s["id"] != student_id]
        with open("students.json", "w") as f:
            json.dump({"students": students}, f, indent=4)
        return jsonify({"success": True, "message": "✅ Student deleted."})
    except:
        return jsonify({"success": False, "message": "❌ Deletion failed."})
# 🚀 Run Server
if __name__ == '__main__':
    app.run(port=5000)