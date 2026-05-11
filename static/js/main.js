/**
 * Main JavaScript file for Job Portal
 * Handles authentication, navigation, and API calls
 */

// API Configuration
const API_BASE_URL = '/api';

// Check if user is authenticated and update UI
function checkAuthStatus() {
    const token = localStorage.getItem('access_token');
    const authLinks = document.getElementById('auth-links');
    const userMenu = document.getElementById('user-menu');

    if (token) {
        // User is authenticated
        if (authLinks) authLinks.classList.add('hidden');
        if (userMenu) {
            userMenu.classList.remove('hidden');
            loadUserInfo();
        }
    } else {
        // User is not authenticated
        if (authLinks) authLinks.classList.remove('hidden');
        if (userMenu) userMenu.classList.add('hidden');
    }
}

// Load user information
async function loadUserInfo() {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/user/`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });

        if (response.ok) {
            const user = await response.json();
            const usernameEl = document.getElementById('username');
            if (usernameEl) {
                usernameEl.textContent = `${user.first_name || user.username}`;
            }
        } else if (response.status === 401) {
            // Token expired, try to refresh
            await refreshToken();
        }
    } catch (error) {
        console.error('Error loading user info:', error);
    }
}

// Refresh JWT token
async function refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
        logout();
        return false;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/auth/token/refresh/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh: refreshToken })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access);
            return true;
        } else {
            logout();
            return false;
        }
    } catch (error) {
        console.error('Error refreshing token:', error);
        logout();
        return false;
    }
}

// Logout function
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login';
}

// Fetch with token injection
async function apiCall(endpoint, options = {}) {
    const token = localStorage.getItem('access_token');
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
    });

    // Handle token expiration
    if (response.status === 401) {
        const refreshed = await refreshToken();
        if (refreshed) {
            return apiCall(endpoint, options);
        }
    }

    return response;
}

// Format currency
function formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency,
    }).format(amount);
}

// Format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// Format time ago
function timeAgo(dateString) {
    const seconds = Math.floor((new Date() - new Date(dateString)) / 1000);

    let interval = seconds / 31536000;
    if (interval > 1) return Math.floor(interval) + ' years ago';

    interval = seconds / 2592000;
    if (interval > 1) return Math.floor(interval) + ' months ago';

    interval = seconds / 86400;
    if (interval > 1) return Math.floor(interval) + ' days ago';

    interval = seconds / 3600;
    if (interval > 1) return Math.floor(interval) + ' hours ago';

    interval = seconds / 60;
    if (interval > 1) return Math.floor(interval) + ' minutes ago';

    return Math.floor(seconds) + ' seconds ago';
}

// Show notification
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.textContent = message;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '10000';
    notification.style.maxWidth = '500px';

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, duration);
}

// Validate email
function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

// Validate password strength
function validatePassword(password) {
    const requirements = {
        minLength: password.length >= 8,
        hasUppercase: /[A-Z]/.test(password),
        hasLowercase: /[a-z]/.test(password),
        hasNumbers: /\d/.test(password),
        hasSpecialChar: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password),
    };

    return requirements;
}

// Get password strength
function getPasswordStrength(password) {
    const requirements = validatePassword(password);
    const met = Object.values(requirements).filter(Boolean).length;
    
    if (met <= 2) return 'weak';
    if (met <= 3) return 'fair';
    if (met <= 4) return 'good';
    return 'strong';
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    checkAuthStatus();
    setupGlobalErrorHandling();
});

// Global error handling
function setupGlobalErrorHandling() {
    window.addEventListener('unhandledrejection', event => {
        console.error('Unhandled promise rejection:', event.reason);
        showNotification('An unexpected error occurred. Please try again.', 'danger');
    });

    window.addEventListener('error', event => {
        console.error('Global error:', event.error);
        showNotification('An unexpected error occurred. Please try again.', 'danger');
    });
}

// Export functions for use in templates
window.logout = logout;
window.showNotification = showNotification;
window.apiCall = apiCall;
window.formatCurrency = formatCurrency;
window.formatDate = formatDate;
window.timeAgo = timeAgo;
window.validateEmail = validateEmail;
window.validatePassword = validatePassword;
window.getPasswordStrength = getPasswordStrength;
