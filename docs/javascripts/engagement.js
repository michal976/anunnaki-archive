/**
 * Email capture & social sharing for Anunnaki Archive
 */

// ============================================================
// EMAIL CAPTURE
// ============================================================

/**
 * Submit email to the waitlist/serverless function
 */
async function submitEmail(email) {
  try {
    const res = await fetch('/api/waitlist', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, source: window.location.pathname })
    });
    return await res.json();
  } catch (err) {
    // Fallback to mailto if API is not available
    window.location.href = `mailto:michal@placek.one?subject=Waitlist%20Signup&body=Email:%20${encodeURIComponent(email)}%0A%0APlease%20add%20me%20to%20the%20Anunnaki%20Archive%20waitlist.`;
    return { success: true, fallback: true };
  }
}

/**
 * Render email capture form into a container
 */
function renderEmailForm(containerId, context) {
  const el = document.getElementById(containerId);
  if (!el) return;
  
  el.innerHTML = `
    <div style="background:linear-gradient(135deg,#1e1b4b,#312e81);border:1px solid #7c3aed;border-radius:12px;padding:24px;margin:20px 0;text-align:center;">
      <h3 style="color:#a78bfa;margin:0 0 8px;">🔔 Never Miss New Evidence</h3>
      <p style="color:#c4b5fd;margin:0 0 16px;font-size:0.9em;">
        Get notified when we publish new deep dives — free, no spam, unsubscribe anytime.
      </p>
      <div style="display:flex;gap:8px;max-width:400px;margin:0 auto;flex-wrap:wrap;">
        <input type="email" id="email-input-${containerId}" placeholder="your@email.com" 
          style="flex:1;min-width:200px;padding:10px 16px;border-radius:8px;border:1px solid #4c1d95;background:#1e1b4b;color:white;font-size:0.95em;">
        <button onclick="submitEmail(document.getElementById('email-input-${containerId}').value)" 
          style="background:#7c3aed;color:white;border:none;padding:10px 24px;border-radius:8px;cursor:pointer;font-size:0.95em;white-space:nowrap;">
          Notify Me
        </button>
      </div>
      <div id="email-msg-${containerId}" style="margin-top:8px;font-size:0.85em;"></div>
    </div>
  `;
  
  // Override submitEmail for this specific form
  window['submitEmail_' + containerId] = async function() {
    const input = document.getElementById('email-input-' + containerId);
    const msg = document.getElementById('email-msg-' + containerId);
    const email = input.value.trim();
    
    if (!email || !email.includes('@')) {
      msg.textContent = '❌ Please enter a valid email address.';
      msg.style.color = '#fca5a5';
      return;
    }
    
    msg.textContent = '⏳ Submitting...';
    msg.style.color = '#a78bfa';
    
    const result = await submitEmail(email);
    if (result.success) {
      msg.textContent = '✅ You\'re on the list! We\'ll notify you when new evidence drops.';
      msg.style.color = '#86efac';
      input.value = '';
    } else {
      msg.textContent = '❌ Error: ' + (result.error || 'Please try again.');
      msg.style.color = '#fca5a5';
    }
  };
}

// ============================================================
// SOCIAL SHARING
// ============================================================

/**
 * Share current page on social platforms
 */
function sharePlatform(platform) {
  const url = encodeURIComponent(window.location.href);
  const title = encodeURIComponent(document.title);
  
  const shareUrls = {
    twitter: `https://twitter.com/intent/tweet?text=${title}&url=${url}`,
    facebook: `https://www.facebook.com/sharer/sharer.php?u=${url}`,
    telegram: `https://t.me/share/url?url=${url}&text=${title}`,
    copy: null
  };
  
  if (platform === 'copy') {
    navigator.clipboard.writeText(window.location.href).then(() => {
      const btn = document.querySelector('[data-share="copy"]');
      if (btn) {
        btn.textContent = '✓ Copied!';
        setTimeout(() => { btn.textContent = '🔗 Copy Link'; }, 2000);
      }
    });
    return;
  }
  
  window.open(shareUrls[platform], '_blank', 'width=600,height=400');
}

/**
 * Render share buttons into a container
 */
function renderShareButtons(containerId) {
  const el = document.getElementById(containerId);
  if (!el) return;
  
  el.innerHTML = `
    <div style="margin:20px 0;">
      <p style="color:#a78bfa;font-size:0.85em;margin:0 0 8px;text-transform:uppercase;letter-spacing:1px;">
        📤 Share This Evidence
      </p>
      <div style="display:flex;gap:8px;flex-wrap:wrap;">
        <button onclick="sharePlatform('twitter')" 
          style="background:#1DA1F2;color:white;border:none;padding:8px 16px;border-radius:8px;cursor:pointer;font-size:0.9em;">
          𝕏 Twitter
        </button>
        <button onclick="sharePlatform('facebook')" 
          style="background:#4267B2;color:white;border:none;padding:8px 16px;border-radius:8px;cursor:pointer;font-size:0.9em;">
          f Facebook
        </button>
        <button onclick="sharePlatform('telegram')" 
          style="background:#0088cc;color:white;border:none;padding:8px 16px;border-radius:8px;cursor:pointer;font-size:0.9em;">
          ✈️ Telegram
        </button>
        <button data-share="copy" onclick="sharePlatform('copy')" 
          style="background:#4c1d95;color:white;border:none;padding:8px 16px;border-radius:8px;cursor:pointer;font-size:0.9em;">
          🔗 Copy Link
        </button>
      </div>
    </div>
  `;
}

// Auto-render on page load for evidence articles
document.addEventListener('DOMContentLoaded', function() {
  // Render email form in containers
  document.querySelectorAll('[data-email-form]').forEach(el => {
    renderEmailForm(el.id, el.dataset.emailContext || 'default');
  });
  
  // Render share buttons
  document.querySelectorAll('[data-share-buttons]').forEach(el => {
    renderShareButtons(el.id);
  });
});
