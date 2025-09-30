#!/usr/bin/env bash
set -euo pipefail

# === CONFIG ===
DOMAIN="remote.genxfx.org"
DUCKDNS_DOMAIN="your-duckdns-subdomain.duckdns.org"
DEVICE_IP="10.62.78.114"
BUILD_NUMBER="15.1.1.109SP06(OP001PF001AZ)"
HASHED_ID=$(echo -n "$BUILD_NUMBER" | openssl dgst -sha256 | awk '{print $2}')
FIREBASE_PROJECT="genxfx"
PRIVACY_EMAIL="189807f4de4d86bd181553d72ab3f.protect@withheldforprivacy.com"

# === STEP 1: Reverse Proxy Setup ===
reverse_proxy() {
  echo "[*] Setting up reverse proxy for $DOMAIN -> $DEVICE_IP"
  cat > remote.conf <<EOF
<VirtualHost *:80>
  ServerName $DOMAIN
  ProxyPass / http://$DEVICE_IP:8000/
  ProxyPassReverse / http://$DEVICE_IP:8000/
</VirtualHost>
EOF

  scp remote.conf user@server354.web-hosting.com:/etc/apache2/sites-available/
  ssh user@server354.web-hosting.com "a2ensite remote && systemctl reload apache2"
}

# === STEP 2: Device Identity Hashing ===
device_identity() {
  echo "[*] Device hash: $HASHED_ID"
  curl -H "X-Device-ID: $HASHED_ID" https://genxfx.org/api/agent-status || true
}

# === STEP 3: Firebase Session Schema ===
firebase_session() {
  echo "[*] Pushing session schema to Firebase"
  cat > session.json <<EOF
{
  "deviceid": "$HASHED_ID",
  "session_token": "$(uuidgen)",
  "timestamp": "$(date -Iseconds)",
  "notes_synced": true
}
EOF
  firebase deploy --only firestore:rules
}

# === STEP 4: GitHub OAuth + Device Verification ===
github_oauth_check() {
  echo "[*] Reminder: Add this snippet to your OAuth callback"
  cat <<'JS'
if (req.headers['x-device-id'] !== expectedHash) {
  return res.status(403).send("Unauthorized device");
}
JS
}

# === STEP 5: LiteWriter Note Sync ===
note_sync() {
  echo "[*] Mounting LiteWriter WebDAV and syncing tasks"
  mkdir -p /mnt/litewriter
  mount -t davfs http://$DOMAIN /mnt/litewriter || true
  grep -r "\[ \]" /mnt/litewriter | awk '{print $2}' > tasks.txt
  while read -r task; do
    gh issue create --title "New Task" --body "$task"
  done < tasks.txt
}

# === STEP 6: VS Code Extension Hook ===
vscode_hook() {
  echo "[*] VS Code extension should poll Firebase at:"
  echo "https://firebase.genxfx.org/session-status"
}

# === STEP 7: Privacy Email Alerts ===
send_alert() {
  echo "[*] Sending fallback alert to $PRIVACY_EMAIL"
  echo "Agent offline" | msmtp -a default "$PRIVACY_EMAIL"
}

# === DDNS Auto-Update (Free Tier) ===
ddns_update() {
  echo "[*] Updating DuckDNS record for $DUCKDNS_DOMAIN"
  curl -s "https://www.duckdns.org/update?domains=$DUCKDNS_DOMAIN&token=<yourtoken>&ip="
}

# === COMMAND DISPATCH ===
case "${1:-}" in
  reverse-proxy) reverse_proxy ;;
  device-id) device_identity ;;
  firebase) firebase_session ;;
  github-oauth) github_oauth_check ;;
  note-sync) note_sync ;;
  vscode) vscode_hook ;;
  alert) send_alert ;;
  ddns) ddns_update ;;
  all)
    reverse_proxy
    device_identity
    firebase_session
    note_sync
    ;;
  *)
    echo "Usage: $0 {reverse-proxy|device-id|firebase|github-oauth|note-sync|vscode|alert|ddns|all}"
    ;;
esac