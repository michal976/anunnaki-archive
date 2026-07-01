/**
 * Membership Gating System for Anunnaki Archive
 * 
 * Simple localStorage-based gating for static MkDocs site.
 * After Stripe checkout success → redirect to /members/welcome
 * → sets membership flag → all premium content is accessible.
 */

const MEMBER_KEY = 'anunnaki_member';
const MEMBER_EXPIRY = 'anunnaki_member_expiry';

/**
 * Check if current user is an active member
 */
function isMember() {
  const expiry = localStorage.getItem(MEMBER_EXPIRY);
  if (!expiry) return false;
  
  // Check if membership hasn't expired (365 days from signup)
  if (Date.now() > parseInt(expiry)) {
    localStorage.removeItem(MEMBER_KEY);
    localStorage.removeItem(MEMBER_EXPIRY);
    return false;
  }
  return localStorage.getItem(MEMBER_KEY) === 'true';
}

/**
 * Mark user as member (called from welcome page after Stripe redirect)
 * @param {number} days - membership duration in days
 */
function setMember(days = 365) {
  localStorage.setItem(MEMBER_KEY, 'true');
  localStorage.setItem(MEMBER_EXPIRY, String(Date.now() + (days * 24 * 60 * 60 * 1000)));
}

/**
 * Gate a page — show content to members, show upgrade prompt to non-members
 * @param {string} gateId - DOM element ID containing premium content
 * @param {string} promptId - DOM element ID containing the upgrade prompt
 */
function gateContent(gateId, promptId) {
  const gate = document.getElementById(gateId);
  const prompt = document.getElementById(promptId);
  
  if (!gate) return;
  
  if (isMember()) {
    if (gate) gate.style.display = 'block';
    if (prompt) prompt.style.display = 'none';
  } else {
    if (gate) gate.style.display = 'none';
    if (prompt) prompt.style.display = 'block';
  }
}

/**
 * Open Stripe checkout
 */
async function openCheckout(priceId) {
  const successUrl = window.location.origin + '/members/welcome';
  const cancelUrl = window.location.origin + '/premium';
  
  try {
    const res = await fetch('/api/checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ priceId, successUrl, cancelUrl })
    });
    const data = await res.json();
    if (data.url) {
      window.location.href = data.url;
    } else {
      alert('Error: ' + (data.error || 'Unknown error'));
    }
  } catch (err) {
    alert('Error connecting to payment system: ' + err.message);
  }
}

// Run on page load for gated content
document.addEventListener('DOMContentLoaded', function() {
  // Gate all premium sections
  document.querySelectorAll('[data-premium]').forEach(el => {
    gateContent(el.id, el.id + '-prompt');
  });
});

// Expose to global scope for HTML inline onclick
window.isMember = isMember;
window.setMember = setMember;
window.openCheckout = openCheckout;
window.gateContent = gateContent;
