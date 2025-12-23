// API Configuration
const API_URL = 'http://localhost:5000';

// Login form handler
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        if (!response.ok) {
            throw new Error('Invalid username or password');
        }
        
        const data = await response.json();
        localStorage.setItem('currentUser', username);
        
        showSuccessMessage('Login successful! Redirecting...');
        setTimeout(() => window.location.href = 'access.html', 1500);
    } catch (error) {
        showAuthError('Login failed: ' + error.message);
    }
});

function showAuthError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'auth-error';
    errorDiv.textContent = message;
    errorDiv.style.cssText = 'color: red; padding: 10px; margin-bottom: 15px; border: 1px solid red; border-radius: 5px;';
    document.querySelector('form').parentElement.appendChild(errorDiv);
    setTimeout(() => errorDiv.remove(), 5000);
}

function showSuccessMessage(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'auth-success';
    successDiv.textContent = message;
    successDiv.style.cssText = 'color: green; padding: 10px; margin-bottom: 15px; border: 1px solid green; border-radius: 5px;';
    document.querySelector('form').parentElement.insertBefore(successDiv, document.querySelector('form'));
}
