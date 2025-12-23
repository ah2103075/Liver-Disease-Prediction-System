// API Configuration
const API_URL = 'http://localhost:5000';

// Get current user from localStorage
const currentUser = localStorage.getItem('currentUser');

// Redirect to login if not authenticated
if (!currentUser) {
    window.location.href = 'login.html';
}

// Display user information
document.getElementById('userDisplay').textContent = `👤 Logged in as: ${currentUser}`;

// Prediction form handler
document.getElementById('predictionForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    // Get form data FIRST before anything else
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);
    
    // Convert string values to numbers
    Object.keys(data).forEach(key => {
        data[key] = parseFloat(data[key]);
    });
    
    try {
        // Show loading state
        const submitBtn = e.target.querySelector('.submit-btn');
        const originalText = submitBtn.textContent;
        submitBtn.disabled = true;
        submitBtn.textContent = '⏳ Processing...';
        
        // Make API request
        const response = await fetch(`${API_URL}/predict/${currentUser}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to make prediction');
        }
        
        const result = await response.json();
        
        // Display the result - STAYS VISIBLE UNTIL RESET
        displayResult(result);
        
        // Restore button - DO NOT RESET FORM
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
        
    } catch (error) {
        displayError(error.message);
        
        // Restore button
        const submitBtn = e.target.querySelector('.submit-btn');
        submitBtn.disabled = false;
        submitBtn.textContent = '🔍 Get Prediction';
    }
}, false);

// Display result function - RESULT STAYS VISIBLE UNTIL RESET
function displayResult(result) {
    const resultSection = document.getElementById('resultSection');
    const resultStatus = document.getElementById('resultStatus');
    const predictionValue = document.getElementById('predictionValue');
    const predictionStatus = document.getElementById('predictionStatus');
    const confidence = document.getElementById('confidence');
    
    // Determine if positive or negative prediction
    const isPredicted = result.prediction === 1;
    const predictionText = isPredicted ? '⚠️ POSITIVE - Disease Detected' : '✅ NEGATIVE - No Disease';
    const statusClass = isPredicted ? 'positive' : 'negative';
    
    // Update all content
    resultStatus.className = 'result-status ' + statusClass;
    resultStatus.innerHTML = `<h3>${predictionText}</h3>`;
    
    predictionValue.textContent = isPredicted ? 'Disease Present (1)' : 'Disease Absent (0)';
    predictionStatus.textContent = predictionText;
    confidence.textContent = result.confidence.toFixed(2) + '%';
    
    // Show the result section
    resultSection.style.display = 'block';
    
    // Scroll to result
    setTimeout(() => {
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

// Display error function - auto hides after 5 seconds
function displayError(message) {
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');
    
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    
    // Auto-hide error after 5 seconds
    setTimeout(() => {
        errorSection.style.display = 'none';
    }, 5000);
}

// Reset form and clear result
function resetFormAndClear() {
    // Clear form
    document.getElementById('predictionForm').reset();
    
    // Clear result section
    document.getElementById('resultSection').style.display = 'none';
    
    // Clear error section
    document.getElementById('errorSection').style.display = 'none';
}

// Close error function
function closeError() {
    document.getElementById('errorSection').style.display = 'none';
}

// Navigate to history page
function goToHistory() {
    window.location.href = 'history.html';
}

// Logout function
function logout() {
    localStorage.removeItem('currentUser');
    window.location.href = 'login.html';
}
