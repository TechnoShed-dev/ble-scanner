# ---------------------------------------------------------------------------------------
# CONFIGURATION TEMPLATE: config_credentials.py
# INSTRUCTIONS: 
# 1. Rename this file to 'config_credentials.py'
# 2. Fill in your Wi-Fi and API details below.
# 3. Ensure the renamed file is in your .gitignore!
# ---------------------------------------------------------------------------------------

# --- NETWORK CONFIGURATION ---
# Add as many networks as you need. Ziggy will try them in order.
KNOWN_NETWORKS = [
    {"ssid": "Your_Home_SSID", "pass": "Your_Home_Password"},
    {"ssid": "Your_Hotspot", "pass": "Your_Hotspot_Password"}
]

# --- BACKEND SERVER ---
# The domain pointing to your Receiver (e.g., via Cloudflare Tunnel)
FTP_HOST = "upziggy.yourdomain.com" 
FTP_PORT = 443

# --- SECURITY TOKENS (Cloudflare Access) ---
# Generate these in Cloudflare Zero Trust > Access > Service Auth
CF_CLIENT_ID = "your_client_id_here.access"
CF_CLIENT_SECRET = "your_client_secret_here"