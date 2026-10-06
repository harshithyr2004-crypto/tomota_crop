// -*- coding: utf-8 -*-
/**
 * User Authentication & Session Controller
 * Only users who registered via the Sign Up form can log in.
 * Controls navbar visibility: hidden on login screen, shown when authenticated.
 */

class AuthManager {
    constructor() {
        this.authContainer   = document.getElementById('authContainer');
        this.appContainer    = document.getElementById('appContainer');
        this.mainNav         = document.getElementById('mainNav');
        this.userProfilePill = document.getElementById('userProfilePill');
        this.userNameDisplay = document.getElementById('userNameDisplay');
        this.apiDocsBtn      = document.querySelector('.api-docs-btn');
        this.logoutBtn       = document.getElementById('logoutBtn');

        // Forms & Tabs
        this.loginForm    = document.getElementById('loginForm');
        this.signupForm   = document.getElementById('signupForm');
        this.tabLoginBtn  = document.getElementById('tabLoginBtn');
        this.tabSignupBtn = document.getElementById('tabSignupBtn');

        this.init();
    }

    // -- Registered-user helpers ----------------------------------------------

    getRegisteredUsers() {
        try {
            return JSON.parse(localStorage.getItem('tomatoguard_registered_users') || '[]');
        } catch {
            return [];
        }
    }

    saveRegisteredUsers(users) {
        localStorage.setItem('tomatoguard_registered_users', JSON.stringify(users));
    }

    validateCredentials(username, password) {
        const registered = this.getRegisteredUsers().find(
            u => u.username === username && u.password === password
        );
        return registered || null;
    }

    // -- Inline error/success helpers -----------------------------------------

    showLoginError(msg) {
        let el = document.getElementById('loginErrorMsg');
        if (!el) {
            el = document.createElement('p');
            el.id = 'loginErrorMsg';
            el.style.cssText = 'color:#ff6b6b;font-size:0.875rem;margin-top:0.5rem;text-align:center;font-weight:500;';
            this.loginForm.appendChild(el);
        }
        el.textContent = msg;
    }

    clearLoginError() {
        const el = document.getElementById('loginErrorMsg');
        if (el) el.textContent = '';
    }

    showSignupMessage(msg, isSuccess) {
        let el = document.getElementById('signupErrorMsg');
        if (!el) {
            el = document.createElement('p');
            el.id = 'signupErrorMsg';
            el.style.cssText = 'font-size:0.875rem;margin-top:0.5rem;text-align:center;font-weight:500;';
            this.signupForm.appendChild(el);
        }
        el.style.color = isSuccess ? '#51cf66' : '#ff6b6b';
        el.textContent = msg;
    }

    clearSignupMessage() {
        const el = document.getElementById('signupErrorMsg');
        if (el) el.textContent = '';
    }

    // -- Lifecycle ------------------------------------------------------------

    init() {
        this.bindEvents();
        this.checkSession();
    }

    bindEvents() {
        // Tab switching
        this.tabLoginBtn.addEventListener('click', () => {
            this.tabLoginBtn.classList.add('active');
            this.tabSignupBtn.classList.remove('active');
            this.loginForm.classList.remove('hidden');
            this.signupForm.classList.add('hidden');
            this.clearLoginError();
        });

        this.tabSignupBtn.addEventListener('click', () => {
            this.tabSignupBtn.classList.add('active');
            this.tabLoginBtn.classList.remove('active');
            this.signupForm.classList.remove('hidden');
            this.loginForm.classList.add('hidden');
            this.clearSignupMessage();
        });

        // LOGIN FORM
        this.loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.clearLoginError();

            const username = document.getElementById('loginUsername').value.trim();
            const password = document.getElementById('loginPassword').value.trim();

            if (!username || !password) {
                this.showLoginError('Please enter both username and password.');
                return;
            }

            const user = this.validateCredentials(username, password);
            if (!user) {
                this.showLoginError('Username not found or wrong password. Please register first.');
                return;
            }

            this.setUserSession({
                username: user.username,
                fullname: user.fullname,
                role:     user.role,
                location: user.location || 'Farm Site'
            });
        });

        // SIGNUP FORM
        this.signupForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.clearSignupMessage();

            const name     = document.getElementById('signupName').value.trim();
            const username = document.getElementById('signupUsername').value.trim();
            const location = document.getElementById('signupLocation').value.trim() || 'Farm Site';
            const password = document.getElementById('signupPassword').value.trim();

            if (!name || !username || !password) {
                this.showSignupMessage('Name, Username, and Password are required.', false);
                return;
            }

            if (password.length < 4) {
                this.showSignupMessage('Password must be at least 4 characters.', false);
                return;
            }

            const registeredUsers = this.getRegisteredUsers();
            if (registeredUsers.some(u => u.username === username)) {
                this.showSignupMessage('Username "' + username + '" is already taken.', false);
                return;
            }

            registeredUsers.push({ username, password, fullname: name, location, role: 'Registered Farmer' });
            this.saveRegisteredUsers(registeredUsers);

            this.showSignupMessage('Account created! Please sign in.', true);

            setTimeout(() => {
                this.tabLoginBtn.click();
                document.getElementById('loginUsername').value = username;
                document.getElementById('loginPassword').focus();
            }, 1200);
        });

        // LOGOUT
        this.logoutBtn.addEventListener('click', () => {
            this.logout();
        });
    }

    checkSession() {
        const stored = localStorage.getItem('tomatoguard_user');
        if (stored) {
            try {
                const user = JSON.parse(stored);
                const stillValid = this.getRegisteredUsers().some(u => u.username === user.username);
                if (stillValid) {
                    this.showApp(user);
                    return;
                }
            } catch (e) {}
        }
        localStorage.removeItem('tomatoguard_user');
        this.showLogin();
    }

    setUserSession(user) {
        localStorage.setItem('tomatoguard_user', JSON.stringify(user));
        this.showApp(user);
    }

    showApp(user) {
        this.authContainer.classList.add('hidden');
        this.appContainer.classList.remove('hidden');

        if (this.mainNav)         this.mainNav.classList.remove('hidden');
        if (this.userProfilePill) this.userProfilePill.classList.remove('hidden');
        if (this.apiDocsBtn)      this.apiDocsBtn.classList.remove('hidden');
        if (this.userNameDisplay) this.userNameDisplay.textContent = user.username || 'Farmer';
    }

    showLogin() {
        this.appContainer.classList.add('hidden');
        this.authContainer.classList.remove('hidden');

        if (this.mainNav)         this.mainNav.classList.add('hidden');
        if (this.userProfilePill) this.userProfilePill.classList.add('hidden');
        if (this.apiDocsBtn)      this.apiDocsBtn.classList.add('hidden');
    }

    logout() {
        localStorage.removeItem('tomatoguard_user');
        this.showLogin();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.authManager = new AuthManager();
});
