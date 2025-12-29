// API Configuration
const API_URL = 'http://localhost:5000';

// Get current user from localStorage
const currentUser = localStorage.getItem('currentUser');

// Redirect to login if not authenticated
if (!currentUser) {
    window.location.href = 'login.html';
}

// Display user information
if (document.getElementById('userDisplay')) {
    document.getElementById('userDisplay').textContent = `👤 Logged in as: ${currentUser}`;
}

// Global flag to prevent form reset
let resultIsShowing = false;
let visibilityMonitor = null;  // Track the monitoring interval

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Page loaded - Initializing form');
    
    const form = document.getElementById('predictionForm');
    if (!form) {
        console.error('❌ Form not found!');
        return;
    }
    
    // Attach focus handlers to show suggestions
    const formElements = form.querySelectorAll('input, select');
    formElements.forEach(element => {
        element.addEventListener('focus', showFieldSuggestions);
        element.addEventListener('input', saveFormValues);
        element.addEventListener('change', saveFormValues);
    });
    
    // CRITICAL: Stop form from submitting normally
    form.onsubmit = function(e) {
        e.preventDefault();
        e.stopPropagation();
        return false;
    };
    
    // Attach submit handler
    form.addEventListener('submit', handleFormSubmit, false);
    
    // Save form values whenever user types
    form.addEventListener('input', saveFormValues);
    form.addEventListener('change', saveFormValues);
    
    // Prevent any accidental resets
    form.addEventListener('reset', function(e) {
        if (resultIsShowing) {
            console.log('⚠️  Reset blocked - result is showing');
            e.preventDefault();
            return false;
        }
    });
    
    console.log('✅ Form handlers attached');
});

// Save form values to localStorage
function saveFormValues() {
    const form = document.getElementById('predictionForm');
    if (!form) return;
    
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    localStorage.setItem('liverPredictionFormData', JSON.stringify(data));
    
    // Also save history for each field
    const form_elements = form.querySelectorAll('[name]');
    form_elements.forEach(element => {
        const fieldName = element.name;
        const fieldValue = element.value;
        
        if (fieldValue.trim() !== '') {
            saveFieldHistory(fieldName, fieldValue);
        }
    });
    
    console.log('💾 Form values saved');
}

// Save field history
function saveFieldHistory(fieldName, value) {
    try {
        const historyKey = `fieldHistory_${fieldName}`;
        let history = JSON.parse(localStorage.getItem(historyKey) || '[]');
        
        // Remove if already exists and add to beginning
        history = history.filter(v => v !== value);
        history.unshift(value);
        
        // Keep only last 5 values
        history = history.slice(0, 5);
        
        localStorage.setItem(historyKey, JSON.stringify(history));
    } catch (error) {
        console.error('Error saving field history:', error);
    }
}

// Get field history
function getFieldHistory(fieldName) {
    try {
        const historyKey = `fieldHistory_${fieldName}`;
        return JSON.parse(localStorage.getItem(historyKey) || '[]');
    } catch (error) {
        console.error('Error getting field history:', error);
        return [];
    }
}

// Show field suggestions dropdown
function showFieldSuggestions(e) {
    const field = e.target;
    const fieldName = field.name;
    const history = getFieldHistory(fieldName);
    
    if (history.length === 0) {
        return; // No history to show
    }
    
    // Remove any existing suggestion dropdown
    const existingSuggestions = document.querySelector('.field-suggestions');
    if (existingSuggestions) {
        existingSuggestions.remove();
    }
    
    // Create suggestions dropdown
    const suggestionsDiv = document.createElement('div');
    suggestionsDiv.className = 'field-suggestions';
    
    // Add suggestion items
    history.forEach(value => {
        const suggestionItem = document.createElement('div');
        suggestionItem.textContent = `📌 ${value}`;
        
        suggestionItem.addEventListener('click', function() {
            field.value = value;
            suggestionsDiv.remove();
            field.focus();
            saveFormValues();
        });
        
        suggestionsDiv.appendChild(suggestionItem);
    });
    
    // Add to body to get proper positioning
    document.body.appendChild(suggestionsDiv);
    
    // Calculate position based on field's location
    const fieldRect = field.getBoundingClientRect();
    suggestionsDiv.style.position = 'fixed';
    suggestionsDiv.style.top = (fieldRect.bottom + 5) + 'px';
    suggestionsDiv.style.left = fieldRect.left + 'px';
    suggestionsDiv.style.width = fieldRect.width + 'px';
    suggestionsDiv.style.zIndex = '10000';
    
    // Remove dropdown when clicking outside
    function removeDropdown(e) {
        if (e.target !== field && !suggestionsDiv.contains(e.target)) {
            suggestionsDiv.remove();
            document.removeEventListener('click', removeDropdown);
        }
    }
    
    setTimeout(() => {
        document.addEventListener('click', removeDropdown);
    }, 0);
}

// Load previous form values from localStorage
function loadPreviousFormValues() {
    try {
        const savedData = localStorage.getItem('liverPredictionFormData');
        if (!savedData) {
            console.log('ℹ️  No previous form data found');
            return;
        }
        
        const data = JSON.parse(savedData);
        const form = document.getElementById('predictionForm');
        
        if (!form) return;
        
        // Restore each field
        Object.keys(data).forEach(key => {
            const field = form.querySelector(`[name="${key}"]`);
            if (field) {
                field.value = data[key];
            }
        });
        
        console.log('✅ Previous form values restored');
    } catch (error) {
        console.error('❌ Error loading previous values:', error);
    }
}

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    e.stopPropagation();
    e.stopImmediatePropagation();

    console.log('📝 Form submitted');
    
    const form = e.target;
    const submitBtn = form.querySelector('.submit-btn');
    const originalBtnText = submitBtn.textContent;
    
    // Get form data
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = parseFloat(value);
    }
    
    try {
        // Show loading
        submitBtn.disabled = true;
        submitBtn.textContent = '⏳ Processing...';
        
        console.log('📤 Sending prediction request...');
        
        // Make API call
        const response = await fetch(`${API_URL}/predict/${currentUser}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Prediction failed');
        }
        
        const result = await response.json();
        console.log('✅ Prediction received:', result);
        
        // Show result
        showResult(result);
        
        // Restore button
        submitBtn.disabled = false;
        submitBtn.textContent = originalBtnText;
        
    } catch (error) {
        console.error('❌ Error:', error);
        showError(error.message);
        
        // Restore button
        submitBtn.disabled = false;
        submitBtn.textContent = originalBtnText;
    }
    
    return false;
}

// Show prediction result
function showResult(result) {
    console.log('📊 Displaying result...');
    
    const resultDisplay = document.getElementById('resultDisplay');
    const resultMainStatus = document.getElementById('resultMainStatus');
    const resultDisplayValue = document.getElementById('resultDisplayValue');
    const resultDisplayStatus = document.getElementById('resultDisplayStatus');
    const resultDisplayConfidence = document.getElementById('resultDisplayConfidence');
    const resultDisplayTime = document.getElementById('resultDisplayTime');
    const resultStatusBox = document.getElementById('resultStatusBox');
    
    if (!resultDisplay) {
        console.error('❌ Result display not found');
        return;
    }
    
    // Set flag
    resultIsShowing = true;
    
    // Get timestamp
    const now = new Date();
    const dateStr = now.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
    const timeStr = now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit' 
    });
    
    // Determine result type
    const isPositive = result.prediction === 1;
    const statusText = isPositive ? '⚠️ POSITIVE - Disease Detected' : '✅ NEGATIVE - No Disease';
    const statusClass = isPositive ? 'positive' : 'negative';
    
    // Update content
    resultMainStatus.textContent = statusText;
    resultStatusBox.className = 'result-status-box ' + statusClass;
    resultDisplayValue.textContent = isPositive ? 'Disease Present (1)' : 'Disease Absent (0)';
    resultDisplayStatus.textContent = statusText;
    resultDisplayConfidence.textContent = result.confidence.toFixed(2) + '%';
    resultDisplayTime.textContent = `📅 ${dateStr} at ${timeStr}`;
    
    // FORCE DISPLAY
    resultDisplay.style.cssText = 'display: block !important; visibility: visible !important; opacity: 1 !important;';
    resultDisplay.removeAttribute('hidden');
    resultDisplay.classList.remove('hidden');
    
    console.log('✅ Result is now visible');
    console.log('   Display:', resultDisplay.style.display);
    console.log('   Visibility:', resultDisplay.style.visibility);
    
    // Scroll to result
    setTimeout(() => {
        resultDisplay.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 150);
    
    // Keep monitoring visibility for 30 seconds
    let checkCount = 0;
    visibilityMonitor = setInterval(() => {
        checkCount++;
        
        // Stop after 30 seconds (150 checks * 200ms)
        if (checkCount > 150) {
            clearInterval(visibilityMonitor);
            visibilityMonitor = null;
            console.log('✅ Visibility monitoring ended (30 seconds)');
            return;
        }
        
        // Check if still visible
        const computedStyle = window.getComputedStyle(resultDisplay);
        if (computedStyle.display === 'none' || computedStyle.visibility === 'hidden') {
            console.warn('⚠️  Result was hidden! Restoring...');
            resultDisplay.style.cssText = 'display: block !important; visibility: visible !important; opacity: 1 !important;';
        }
    }, 200);
    
    console.log('🎉 Result will stay visible until you click Reset Form');
}

// Show error message
function showError(message) {
    console.log('❌ Showing error:', message);
    
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');
    
    if (errorSection && errorMessage) {
        errorMessage.textContent = message;
        errorSection.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            errorSection.style.display = 'none';
        }, 5000);
    }
}

// Reset form and clear result
function resetFormAndClear() {
    console.log('🔄 Reset button clicked');
    
    // STOP the visibility monitoring
    if (visibilityMonitor) {
        clearInterval(visibilityMonitor);
        visibilityMonitor = null;
        console.log('✅ Visibility monitor stopped');
    }
    
    // Clear flag
    resultIsShowing = false;
    
    // Reset form
    const form = document.getElementById('predictionForm');
    if (form) {
        form.reset();
        console.log('✅ Form cleared');
    }
    
    // Hide result - multiple methods to ensure it's hidden
    const resultDisplay = document.getElementById('resultDisplay');
    if (resultDisplay) {
        resultDisplay.style.display = 'none';
        resultDisplay.style.visibility = 'hidden';
        resultDisplay.style.pointerEvents = 'none';
        resultDisplay.style.height = '0';
        resultDisplay.style.overflow = 'hidden';
        console.log('✅ Result hidden');
    }
    
    // Hide error
    const errorSection = document.getElementById('errorSection');
    if (errorSection) {
        errorSection.style.display = 'none';
        errorSection.style.visibility = 'hidden';
        errorSection.style.pointerEvents = 'none';
        console.log('✅ Error hidden');
    }
    
    console.log('✅ Reset complete');
}

// Close error
function closeError() {
    const errorSection = document.getElementById('errorSection');
    if (errorSection) {
        errorSection.style.display = 'none';
    }
}

// Navigate to history
function goToHistory() {
    window.location.href = 'history.html';
}

// Logout
function logout() {
    localStorage.removeItem('currentUser');
    window.location.href = 'login.html';
}
