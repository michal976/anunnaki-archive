/**
 * Waitlist API — captures email and optionally sends notification.
 * 
 * Stores to a JSON file in /tmp (ephemeral on Vercel).
 * For production: connect to Mailchimp, ConvertKit, or SendGrid.
 */

const NOTIFICATION_EMAIL = 'michal@placek.one';
const LIST_FILE = '/tmp/waitlist.json';

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { email, source } = req.body;

  if (!email || !email.includes('@')) {
    return res.status(400).json({ error: 'Valid email required' });
  }

  try {
    // Store to file (ephemeral — for production use a real service)
    const fs = require('fs');
    let entries = [];
    try {
      entries = JSON.parse(fs.readFileSync(LIST_FILE, 'utf8'));
    } catch (e) {
      // File doesn't exist yet, starting fresh
    }
    
    entries.push({
      email,
      source: source || 'unknown',
      timestamp: new Date().toISOString()
    });
    
    fs.writeFileSync(LIST_FILE, JSON.stringify(entries, null, 2));
    
    console.log(`📧 Waitlist signup: ${email} from ${source || 'unknown'}`);
    
    res.json({ 
      success: true, 
      message: 'You\'re on the list!',
      total: entries.length 
    });
  } catch (err) {
    console.error('Waitlist error:', err);
    res.status(500).json({ error: err.message });
  }
};
