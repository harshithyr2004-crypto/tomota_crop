// -*- coding: utf-8 -*-
/**
 * User Authentication & Session Controller
 * Controls navbar visibility: hidden on login screen, shown when authenticated.
 */

class AuthManager {
    constructor() {
        this.authContainer = document.getElementById('authContainer');
        this.appContainer = document.getElementById('appContainer');
        this.mainNav = document.getElementById('mainNav');
        this.userProfilePill = document.getElementById('userProfilePill');
        this.userNameDisplay = document.getElementById('userNameDisplay');
        this.apiDocsBtn = document.querySelector('.api-docs-btn');
        this.logoutBtn = document.getElementById('logoutBtn');
        
        // Forms & Tabs
        this.loginForm = document.getElementById('loginForm');
        this.signupForm = document.getElementById('signupForm');
        this.tabLoginBtn = document.getElementById('tabLoginBtn');
        this.tabSignupBtn = document.getElementById('tabSignupBtn');
        this.quickDemoBtn = document.getElementById('quickDemoBtn');

        this.init();
    }

    init() {
        this.bindEvents();
        this.checkSession();
    }

    bindEvents() {
        // Tab switching between Login and Signup
        this.tabLoginBtn.addEventListener('click', () => {
            this.tabLoginBtn.classList.add('active');
            this.tabSignupBtn.classList.remove('active');
            this.loginForm.classList.remove('hidden');
            this.signupForm.classList.add('hidden');
        });

        this.tabSignupBtn.addEventListener('click', () => {
            this.tabSignupBtn.classList.add('active');
            this.tabLoginBtn.classList.remove('active');
            this.signupForm.classList.remove('hidden');
            this.loginForm.classList.add('hidden');
        });

        // Form submissions
        this.loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const username = document.getElementById('loginUsername').value.trim();
            const password = document.getElementById('loginPassword').value.trim();
            if (!username || !password) {
                alert('Please enter username and password.');
                return;
            }
            this.setUserSession({ username: username, role: 'Farmer / Agronomist' });
        });

        this.signupForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('signupName').value.trim();
            const username = document.getElementById('signupUsername').value.trim();
            const location = document.getElementById('signupLocation').value.trim() || 'Farm Site';
            if (!name || !username) {
                alert('Please fill required fields.');
                return;
            }
            this.setUserSession({ username: username, fullname: name, role: 'Registered Farmer', location: location });
        });

        // Instant Quick Demo Login Button
        this.quickDemoBtn.addEventListener('click', () => {
            this.setUserSession({ username: 'Ramesh (Farmer)', role: 'Tomato Farmer & Grower' });
        });

        // Logout
        this.logoutBtn.addEventListener('click', () => {
            this.logout();
        });
    }

    checkSession() {
        const stored = localStorage.getItem('tomatoguard_user');
        if (stored) {
            try {
                const user = JSON.parse(stored);
                this.showApp(user);
                return;
            } catch (e) {}
        }
        this.showLogin();
    }

    setUserSession(user) {
        localStorage.setItem('tomatoguard_user', JSON.stringify(user));
        this.showApp(user);
    }

    showApp(user) {
        // Hide login, show app
        this.authContainer.classList.add('hidden');
        this.appContainer.classList.remove('hidden');

        // Show Main Navigation Bar and User Badge
        if (this.mainNav) this.mainNav.classList.remove('hidden');
        if (this.userProfilePill) this.userProfilePill.classList.remove('hidden');
        if (this.apiDocsBtn) this.apiDocsBtn.classList.remove('hidden');
        if (this.userNameDisplay) this.userNameDisplay.textContent = user.username || 'Farmer';
    }

    showLogin() {
        // Hide app, show login
        this.appContainer.classList.add('hidden');
        this.authContainer.classList.remove('hidden');

        // STRICT REQUIREMENT: HIDE navigation bar on login page, ONLY show Language Selector
        if (this.mainNav) this.mainNav.classList.add('hidden');
        if (this.userProfilePill) this.userProfilePill.classList.add('hidden');
        if (this.apiDocsBtn) this.apiDocsBtn.classList.add('hidden');
    }

    logout() {
        localStorage.removeItem('tomatoguard_user');
        this.showLogin();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.authManager = new AuthManager();
});
