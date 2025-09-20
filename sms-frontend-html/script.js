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
      localStorage.setItem("username", username);
      if (role === 'admin' && data.admin_id) {
        localStorage.setItem("admin_id", data.admin_id); // ✅ Store admin_id
      }

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

function populateClassDropdown(dropdownId) {
  const admin_id = localStorage.getItem("admin_id"); // ✅ Inject admin_id

  fetch(`http://localhost:5000/api/classes?admin_id=${encodeURIComponent(admin_id)}`)
    .then(res => res.json())
    .then(data => {
      const dropdown = document.getElementById(dropdownId);
      dropdown.innerHTML = "";
      data.classes.forEach(cls => {
        const opt = document.createElement("option");
        opt.value = cls;
        opt.textContent = cls;
        dropdown.appendChild(opt);
      });
    })
    .catch(error => {
      console.error("❌ Failed to load classes:", error);
    });
}