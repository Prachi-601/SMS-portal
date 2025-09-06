function login() {
  const role = document.getElementById('role').value;
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const errorMsg = document.getElementById('error-message');

  // Clear previous error
  errorMsg.textContent = '';

  // Send login request to backend
  fetch('http://localhost:5000/api/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ role, username, password })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Redirect based on role
      if (role === 'student') window.location.href = 'student.html';
      else if (role === 'teacher') window.location.href = 'teacher.html';
      else if (role === 'admin') window.location.href = 'admin.html';
    } else {
      errorMsg.textContent = data.message || 'Invalid credentials';
    }
  })
  .catch(error => {
    console.error('Error:', error);
    errorMsg.textContent = 'Server error. Please try again later.';
  });
}
