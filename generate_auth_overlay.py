import re

with open("trueprofit_original.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find the script block
script_start = html.find('<script>')
script_end = html.find('</script>', script_start) + 9

# Strip out the logic
html_without_logic = html[:script_start] + html[script_end:]

auth_overlay = """
<style>
/* Secure Auth Overlay Styles */
#tp-auth-overlay {
    position: fixed; inset: 0; background: rgba(32, 42, 36, 0.95);
    display: flex; align-items: center; justify-content: center; z-index: 999999;
    padding: 20px; font-family: system-ui, -apple-system, sans-serif;
    backdrop-filter: blur(5px);
}
#tp-auth-overlay .tp-auth-card {
    background: #fff; border-radius: 20px; padding: 30px; max-width: 400px; width: 100%;
    text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.5); color: #202a24;
}
#tp-auth-overlay h2 { margin: 10px 0; font-size: 22px; color: #202a24; }
#tp-auth-overlay p { font-size: 14px; color: #68716b; line-height: 1.5; margin-bottom: 20px; }
#tp-auth-overlay .tp-btn {
    display: inline-flex; align-items: center; justify-content: center; width: 100%; background: #b08d2c; color: #fff;
    padding: 14px 20px; border-radius: 12px; font-weight: 700; text-decoration: none;
    border: none; cursor: pointer; font-size: 16px; margin-bottom: 20px; gap: 8px;
}
#tp-auth-overlay .tp-btn:hover { background: #9d7d26; }
#tp-auth-overlay .tp-divider { border-top: 1px solid #e2e5e0; padding-top: 20px; text-align: left; }
#tp-auth-overlay .tp-divider p { margin-bottom: 10px; font-size: 13px; font-weight: 600; color: #202a24; text-align: left; }
#tp-auth-overlay .tp-auth-row { display: flex; gap: 8px; }
#tp-auth-overlay .tp-btn-small {
    background: #202a24; color: #fff; padding: 12px 16px; border-radius: 10px; font-weight: 700; border: none; cursor: pointer; width: 100%;
}
.tp-loader {
    border: 3px solid #f3f3f3; border-top: 3px solid #b08d2c; border-radius: 50%;
    width: 20px; height: 20px; animation: spin 1s linear infinite; display: none; margin: 0 auto;
}
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
</style>
<div id="tp-auth-overlay">
  <div class="tp-auth-card">
    <div style="font-size: 40px; margin-bottom: 10px;">🔒</div>
    <h2>TRUEPROFIT™ Access</h2>
    <p>TRUEPROFIT™ is a premium commercial tool. Log in to verify your paid access.</p>
    
    <div id="auth-ui">
      <!-- Firebase Auth requires configuration. See backend/README_SECRETS.md -->
      <button class="tp-btn-small" onclick="loginWithGoogle()" id="login-btn">Log In / Verify Access</button>
      <div class="tp-loader" id="auth-loader"></div>
      <p id="tp-auth-error" style="color: #b42318; font-size: 13px; margin-top: 15px; display: none; font-weight: 600;"></p>
    </div>

    <div class="tp-divider" style="margin-top: 25px;">
      <p style="text-align: center; color: #68716b;">Don't have access yet?</p>
      <a href="https://selar.com/28o4b14m9g" target="_blank" class="tp-btn" style="background: #202a24; font-size: 14px;">Purchase on Selar</a>
    </div>
  </div>
</div>

<!-- Firebase SDKs -->
<script type="module">
  // IMPORT FIREBASE MODULES
  import { initializeApp } from "https://www.gstatic.com/firebasejs/10.3.1/firebase-app.js";
  import { getAuth, signInWithRedirect, GoogleAuthProvider, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.3.1/firebase-auth.js";

  // TODO: Add your actual Firebase configuration here once the project is provisioned.
  // DO NOT COMMIT REAL CREDENTIALS TO GITHUB. USE ENVIRONMENT VARIABLES IN PRODUCTION.
  const firebaseConfig = {
    apiKey: "AIzaSyDRnx8GnLYWk0lAZVFm_OSQ0nRsdO3BRqM",
    authDomain: "trueprofit-app-38918.firebaseapp.com",
    projectId: "trueprofit-app-38918",
    storageBucket: "trueprofit-app-38918.firebasestorage.app",
    messagingSenderId: "436391906446",
    appId: "1:436391906446:web:03ea779ac9b155ecf14ddf"
  };

  let app, auth, provider;
  try {
      app = initializeApp(firebaseConfig);
      auth = getAuth(app);
      provider = new GoogleAuthProvider();
  } catch (e) {
      console.warn("Firebase not configured. Using isolated integration mode.");
  }

  const errorEl = document.getElementById('tp-auth-error');
  const loginBtn = document.getElementById('login-btn');
  const loader = document.getElementById('auth-loader');

  function showError(msg) {
      errorEl.textContent = msg;
      errorEl.style.display = 'block';
      loader.style.display = 'none';
      loginBtn.style.display = 'block';
  }

  window.loginWithGoogle = async () => {
      if (!auth) {
          showError("System configuration incomplete. Firebase credentials required.");
          return;
      }
      try {
          loginBtn.style.display = 'none';
          loader.style.display = 'block';
          errorEl.style.display = 'none';
          await signInWithRedirect(auth, provider);
      } catch (error) {
          showError("Authentication failed: " + error.message);
      }
  };

  async function fetchEngine(user) {
      try {
          loginBtn.style.display = 'none';
          loader.style.display = 'block';
          errorEl.style.display = 'none';

          const token = await user.getIdToken();
          
          // Call our secure backend to verify entitlement and fetch the proprietary logic.
          // Note: In production, change the URL to your deployed backend URL.
          const BACKEND_URL = "/api/engine.js";
          
          const response = await fetch(BACKEND_URL, {
              headers: {
                  'Authorization': 'Bearer ' + token
              }
          });

          const code = await response.text();

          if (!response.ok) {
              // Access denied or error (e.g. 403 Forbidden)
              auth.signOut();
              showError("Access Denied: " + code.replace('/* ', '').replace(' */', ''));
              return;
          }

          // Access Granted: Execute the proprietary engine
          const script = document.createElement('script');
          script.textContent = code;
          document.body.appendChild(script);

          // Hide overlay
          document.getElementById('tp-auth-overlay').style.display = 'none';
          
      } catch (error) {
          showError("Failed to connect to authorization server.");
      }
  }

// Monitor auth state
  if (auth) {
      // CATCHER: Resolves the mobile redirect
      getRedirectResult(auth).catch((error) => {
          showError("Authentication failed: " + error.message);
      });

      // LISTENER: Handles user state
      onAuthStateChanged(auth, (user) => {
          if (user) {
              fetchEngine(user);
          } else {
              loginBtn.style.display = 'block';
              loader.style.display = 'none';
          }
      });
  }
</script>
"""

final_html = html_without_logic.replace("</body>", auth_overlay + "\n</body>")

with open("trueprofit-app.html", "w", encoding="utf-8") as f:
    f.write(final_html)
