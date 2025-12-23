// API Configuration
const API_URL = 'http://localhost:5000';

// Get current user from localStorage
const currentUser = localStorage.getItem('currentUser');

// Redirect to login if not authenticated
if (!currentUser) {
    window.location.href = 'login.html';
}

// Display user information
document.getElementById('userDisplayHistory').textContent = `👤 Logged in as: ${currentUser}`;

// Load history on page load
document.addEventListener('DOMContentLoaded', loadHistory);

// Load history function
async function loadHistory() {
    const historyContainer = document.getElementById('historyContainer');
    
    try {
        const response = await fetch(`${API_URL}/history/${currentUser}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to load history');
        }
        
        const data = await response.json();
        
        if (!data.records || data.records.length === 0) {
            historyContainer.innerHTML = '<p class="no-history">No predictions yet. Make your first prediction!</p>';
            return;
        }
        
        let html = '';
        data.records.forEach((record) => {
            // Parse the timestamp and convert to Bangladesh timezone (GMT+6)
            const date = new Date(record.timestamp);
            
            // Get Bangladesh time by adding 6 hours offset
            const bdTime = new Date(date.getTime() + (6 * 60 * 60 * 1000));
            
            // Format with options
            const weekday = bdTime.toLocaleDateString('en-US', { weekday: 'long' });
            const month = bdTime.toLocaleDateString('en-US', { month: 'long' });
            const day = bdTime.getDate();
            const year = bdTime.getFullYear();
            const hours = String(bdTime.getHours()).padStart(2, '0');
            const minutes = String(bdTime.getMinutes()).padStart(2, '0');
            const seconds = String(bdTime.getSeconds()).padStart(2, '0');
            const ampm = bdTime.getHours() >= 12 ? 'PM' : 'AM';
            const hours12 = bdTime.getHours() % 12 || 12;
            
            const bdDateTime = `${weekday}, ${month} ${day}, ${year} at ${hours12}:${minutes}:${seconds} ${ampm}`;
            
            const status = record.prediction === 1 ? 'positive' : 'negative';
            const statusText = record.prediction === 1 ? '⚠️ POSITIVE' : '✅ NEGATIVE';
            
            // Parse medical parameters from JSON
            const params = JSON.parse(record.medical_parameters);
            
            html += `
                <div class="history-item ${status}">
                    <div class="history-header">
                        <div class="history-datetime">
                            <span class="history-date">${bdDateTime}</span>
                        </div>
                        <button class="delete-btn" onclick="deletePrediction(${record.id})">🗑️ Delete</button>
                    </div>
                    <div class="history-content">
                        <p><strong>Prediction:</strong> ${statusText}</p>
                        
                        <div class="history-parameters">
                            <h4>Medical Parameters:</h4>
                            <div class="parameters-grid">
                                <div class="param-item"><strong>Age:</strong> ${params.Age} years</div>
                                <div class="param-item"><strong>Gender:</strong> ${params.Gender === 1 ? 'Male' : 'Female'}</div>
                                <div class="param-item"><strong>Total Bilirubin:</strong> ${params.Total_Bilirubin} mg/dL</div>
                                <div class="param-item"><strong>Direct Bilirubin:</strong> ${params.Direct_Bilirubin} mg/dL</div>
                                <div class="param-item"><strong>Alkaline Phosphatase:</strong> ${params.Alkaline_Phosphotase} U/L</div>
                                <div class="param-item"><strong>Alamine Aminotransferase:</strong> ${params.Alamine_Aminotransferase} U/L</div>
                                <div class="param-item"><strong>Aspartate Aminotransferase:</strong> ${params.Aspartate_Aminotransferase} U/L</div>
                                <div class="param-item"><strong>Total Proteins:</strong> ${params.Total_Proteins} g/dL</div>
                                <div class="param-item"><strong>Albumin:</strong> ${params.Albumin} g/dL</div>
                                <div class="param-item"><strong>Albumin-Globulin Ratio:</strong> ${params.Albumin_and_Globulin_Ratio}</div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        
        historyContainer.innerHTML = html;
    } catch (error) {
        historyContainer.innerHTML = `<p class="error">Error loading history: ${error.message}</p>`;
    }
}

// Delete specific prediction
async function deletePrediction(predictionId) {
    if (!confirm('Are you sure you want to delete this prediction?')) return;
    
    try {
        const response = await fetch(`${API_URL}/history/${currentUser}/${predictionId}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete prediction');
        }
        
        loadHistory();
    } catch (error) {
        alert('Error deleting prediction: ' + error.message);
    }
}

// Clear all history
async function clearHistoryData() {
    if (!confirm('Are you sure you want to clear all prediction history? This cannot be undone.')) return;
    
    try {
        const response = await fetch(`${API_URL}/history/${currentUser}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (!response.ok) {
            throw new Error('Failed to clear history');
        }
        
        loadHistory();
    } catch (error) {
        alert('Error clearing history: ' + error.message);
    }
}

// Go back to prediction page
function goBack() {
    window.location.href = 'access.html';
}

// Logout function
function logout() {
    localStorage.removeItem('currentUser');
    window.location.href = 'login.html';
}
