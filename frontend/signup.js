// API Configuration
const API_URL = 'http://localhost:5000';

// Sign up form handler
document.getElementById('signupForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const full_name = document.getElementById('signup-fullname').value;
    const username = document.getElementById('signup-username').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const confirm_password = document.getElementById('signup-confirm-password').value;
    
    if (password !== confirm_password) {
        showAuthError('Passwords do not match');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password, email, full_name })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Sign up failed');
        }
        
        const data = await response.json();
        
        // Display success message only
        showSuccessMessage('✅ Account Created Successfully!');
        
        // Display token in a separate message
        if (data.access_token) {
            console.log('Token:', data.access_token);
            const tokenMsg = document.createElement('div');
            tokenMsg.style.cssText = 'color: #3498db; padding: 10px; margin-bottom: 15px; border: 1px solid #3498db; border-radius: 5px; word-break: break-all; font-size: 12px;';
            tokenMsg.textContent = 'Token: ' + data.access_token;
            document.querySelector('form').parentElement.insertBefore(tokenMsg, document.querySelector('form'));
        }
        
        // Redirect immediately - no wait
        window.location.href = 'login.html';
    } catch (error) {
        showAuthError('Sign up failed: ' + error.message);
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
