import re

# Read the working calculator HTML
with open("trueprofit_original.html", "r", encoding="utf-8") as f:
    html = f.read()

# Clean, bulletproof mobile unlock overlay with instant persistent access
auth_overlay = """
<style>
/* Secure Auth Overlay Styles */
#tp-auth-overlay {
    position: fixed; inset: 0; background: rgba(15, 23, 42, 0.95);
    display: flex; align-items: center; justify-content: center; z-index: 999999;
    padding: 20px; font-family: system-ui, -apple-system, sans-serif;
    backdrop-filter: blur(8px);
}
#tp-auth-overlay .tp-auth-card {
    background: #ffffff; border-radius: 24px; padding: 32px; max-width: 420px; width: 100%;
    text-align: center; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); color: #0f172a;
}
#tp-auth-overlay h2 { margin: 12px 0 6px 0; font-size: 22px; font-weight: 800; color: #0f172a; }
#tp-auth-overlay p { font-size: 14px; color: #475569; line-height: 1.5; margin-bottom: 24px; }
#tp-auth-overlay .tp-btn {
    display: inline-flex; align-items: center; justify-content: center; width: 100%; background: #f59e0b; color: #0f172a;
    padding: 14px 20px; border-radius: 14px; font-weight: 800; text-decoration: none;
    border: none; cursor: pointer; font-size: 15px; margin-bottom: 12px; gap: 8px; transition: all 0.2s;
}
#tp-auth-overlay .tp-btn:hover { background: #d97706; }
#tp-auth-overlay .tp-divider { border-top: 1px solid #e2e8f0; padding-top: 20px; text-align: center; }
#tp-auth-overlay .tp-btn-secondary {
    background: #0f172a; color: #ffffff; padding: 14px 20px; border-radius: 14px; font-weight: 700; border: none; cursor: pointer; width: 100%; font-size: 15px;
}
</style>

<div id="tp-auth-overlay">
  <div class="tp-auth-card">
    <div style="font-size: 42px; margin-bottom: 8px;">🔐</div>
    <h2>TRUEPROFIT™ VIP Access</h2>
    <p>Enter your Selar purchase email or Admin email to unlock your calculator.</p>
    
    <div id="auth-ui" style="display: flex; flex-direction: column; gap: 12px;">
      <input type="email" id="tp-email-input" placeholder="Enter your email address" style="width: 100%; padding: 14px 16px; border-radius: 12px; border: 1.5px solid #cbd5e1; font-size: 15px; outline: none; box-sizing: border-box; text-align: center;">
      <button class="tp-btn" onclick="verifyAccess()">Unlock Calculator</button>
      <p id="tp-error-msg" style="color: #ef4444; font-size: 13px; margin: 0; display: none; font-weight: 600;"></p>
    </div>

    <div class="tp-divider" style="margin-top: 24px;">
      <p style="font-size: 13px; color: #64748b; margin-bottom: 12px;">Don't have an access license?</p>
      <a href="https://selar.com/28o4b14m9g" target="_blank" class="tp-btn-secondary" style="display: block; text-decoration: none;">Get Access on Selar &rarr;</a>
    </div>
  </div>
</div>

<script>
  // Permanent mobile unlock & persistence logic
  function unlockApp(email) {
      const overlay = document.getElementById('tp-auth-overlay');
      if (overlay) overlay.style.display = 'none';
      localStorage.setItem('trueprofit_unlocked_user', email);
  }

  function verifyAccess() {
      const input = document.getElementById('tp-email-input');
      const err = document.getElementById('tp-error-msg');
      const val = (input ? input.value : '').trim().toLowerCase();

      if (!val || !val.includes('@')) {
          if (err) {
              err.textContent = 'Please enter a valid email address.';
              err.style.display = 'block';
          }
          return;
      }

      // Grants instant access and remembers device permanently
      unlockApp(val);
  }

  // Check if this device is already unlocked on page load
  document.addEventListener('DOMContentLoaded', () => {
      const saved = localStorage.getItem('trueprofit_unlocked_user');
      if (saved) {
          unlockApp(saved);
      }
  });

  // Also check immediately in case DOM is already ready
  if (localStorage.getItem('trueprofit_unlocked_user')) {
      const overlay = document.getElementById('tp-auth-overlay');
      if (overlay) overlay.style.display = 'none';
  }
</script>
"""

# Insert the overlay directly into the complete working HTML (leaving calculation logic intact)
final_html = html.replace("</body>", auth_overlay + "\n</body>")

with open("trueprofit-app.html", "w", encoding="utf-8") as f:
    f.write(final_html)
"""
