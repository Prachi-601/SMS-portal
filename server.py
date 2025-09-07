from flask import Flask, request, jsonify
from auth import login  # reuse your existing login logic
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

if __name__ == '__main__':
    app.run(port=5000)