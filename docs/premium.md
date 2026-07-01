---
tags: [premium, membership, anunnaki, english]
---

# 💎 Premium Membership

Unlock the complete Anunnaki Archive — every article, every detail, every connection.

## What's Included

- ✅ **Full access** to all 150+ articles
- ✅ **Cross-referenced content** with related topics
- ✅ **Full-text search** across the entire archive
- ✅ **PDF exports** of any article
- ✅ **Ad-free experience**
- ✅ **Early access** to new content
- ✅ **Member community** discussions

## Pricing

| Tier | Price | What You Get |
|------|-------|-------------|
| 🗓️ Monthly | **$9/month** | Full access, cancel anytime |
| 📅 Annual | **$79/year** | Full access, 2 months free |
| 🏆 Lifetime | **$199** | Forever access + supporter badge |

## Choose Your Plan

<div style="display:flex;flex-wrap:wrap;gap:20px;margin:30px 0;">
  <div style="flex:1;min-width:250px;border:2px solid #7c3aed;border-radius:12px;padding:24px;text-align:center;">
    <h3>🗓️ Monthly</h3>
    <p style="font-size:2em;font-weight:bold;color:#7c3aed;">$9</p>
    <p style="color:#666;">per month</p>
    <button onclick="checkout('price_1To255JwU8rLBPSf3X36D6mi')" style="background:#7c3aed;color:white;border:none;padding:12px 32px;border-radius:8px;font-size:1.1em;cursor:pointer;width:100%;">
      Subscribe Monthly
    </button>
  </div>
  <div style="flex:1;min-width:250px;border:2px solid #f59e0b;border-radius:12px;padding:24px;text-align:center;">
    <div style="background:#f59e0b;color:white;padding:4px 12px;border-radius:12px;display:inline-block;font-size:0.8em;margin-bottom:8px;">BEST VALUE</div>
    <h3>📅 Annual</h3>
    <p style="font-size:2em;font-weight:bold;color:#f59e0b;">$79</p>
    <p style="color:#666;">$6.58/month — save 27%</p>
    <button onclick="checkout('price_1To256JwU8rLBPSfV3HNlU2G')" style="background:#f59e0b;color:white;border:none;padding:12px 32px;border-radius:8px;font-size:1.1em;cursor:pointer;width:100%;">
      Subscribe Annual
    </button>
  </div>
  <div style="flex:1;min-width:250px;border:2px solid #10b981;border-radius:12px;padding:24px;text-align:center;">
    <h3>🏆 Lifetime</h3>
    <p style="font-size:2em;font-weight:bold;color:#10b981;">$199</p>
    <p style="color:#666;">one-time payment</p>
    <a href="mailto:a32675117@gmail.com?subject=Lifetime%20Membership" style="background:#10b981;color:white;text-decoration:none;padding:12px 32px;border-radius:8px;font-size:1.1em;display:inline-block;width:100%;box-sizing:border-box;">
      Contact for Access
    </a>
  </div>
</div>

<div id="checkout-message" style="display:none;background:#d1fae5;border:1px solid #10b981;border-radius:8px;padding:16px;margin:20px 0;">
  ✅ Redirecting to secure checkout...
</div>

---

### 🔒 Secure Payment

All payments are processed securely via **Stripe**. Your card details never touch our servers. Cancel anytime.

_Questions? Email [a32675117@gmail.com](mailto:a32675117@gmail.com)_

<script>
async function checkout(priceId) {
  const msg = document.getElementById('checkout-message');
  msg.style.display = 'block';
  msg.textContent = '⏳ Opening secure checkout...';
  
  try {
    const res = await fetch('/api/checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        priceId,
        successUrl: window.location.origin + '/members/welcome',
        cancelUrl: window.location.origin + '/premium'
      })
    });
    const data = await res.json();
    if (data.url) {
      window.location.href = data.url;
    } else {
      msg.textContent = '❌ Error: ' + (data.error || 'Unknown error');
      msg.style.background = '#fee2e2';
      msg.style.borderColor = '#ef4444';
    }
  } catch (err) {
    msg.textContent = '❌ Error: ' + err.message;
    msg.style.background = '#fee2e2';
    msg.style.borderColor = '#ef4444';
  }
}
</script>
