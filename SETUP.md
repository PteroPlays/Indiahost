# 🔧 Installation & Setup Guide

Complete guide to get IndiaHost up and running.

## Prerequisites Checklist

- [ ] Linux system with KVM support
- [ ] sudo/root access for dependencies
- [ ] Python 3.8+
- [ ] Discord server where you can manage roles
- [ ] Discord application/bot token

## Step 1: System Preparation

### Enable KVM Virtualization

Check if KVM is available:
```bash
kvm-ok
```

If not installed:
```bash
# Ubuntu/Debian
sudo apt install cpu-checker

# Then check
kvm-ok
```

### Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y \
    qemu-system-x86-64 \
    cloud-image-utils \
    wget \
    lsof \
    openssl \
    python3 \
    python3-pip
```

**Fedora/CentOS/RHEL:**
```bash
sudo dnf install -y \
    qemu-system-x86 \
    cloud-utils-growpart \
    wget \
    lsof \
    openssl \
    python3 \
    python3-pip
```

**Arch:**
```bash
sudo pacman -Sy qemu wget lsof openssl python python-pip
```

## Step 2: Clone Repository

```bash
cd ~
git clone https://github.com/PteroPlays/IndiaHost.git
cd IndiaHost
chmod +x vm-manager.sh
```

## Step 3: VM Manager Setup

### Create VM Storage Directory

```bash
mkdir -p ~/vms
chmod 700 ~/vms
```

### Test VM Manager

```bash
./vm-manager.sh
```

You should see the main menu. Press `0` to exit.

## Step 4: Discord Bot Setup

### Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Name it "IndiaHost" (or your preference)
4. Go to "Bot" section → Click "Add Bot"
5. Copy the token

### Configure Bot Permissions

In Discord Developer Portal:

1. Go to "OAuth2" → "URL Generator"
2. Select scopes: `bot`
3. Select permissions:
   - Send Messages
   - Embed Links
   - Add Reactions
   - Manage Messages (optional)
4. Copy generated URL
5. Paste in browser to invite bot to your server

### Create Admin Role

In your Discord server:

1. Go to Server Settings → Roles
2. Create new role: `VM_Admin`
3. Assign to trusted users only

### Create Bot Configuration

```bash
cd ~/IndiaHost

# Create config file with your token
cat > bot_config.json << EOF
{
    "token": "YOUR_BOT_TOKEN_HERE",
    "admin_role": "VM_Admin",
    "vm_dir": "$HOME/vms",
    "allowed_users": []
}
EOF

# Secure the config file
chmod 600 bot_config.json
```

Replace `YOUR_BOT_TOKEN_HERE` with your actual bot token.

### Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

Or manually:
```bash
pip3 install discord.py==2.3.2
```

### Test Discord Bot

```bash
python3 discord_bot.py
```

You should see:
```
✅ Bot logged in as IndiaHost#1234
```

Press `Ctrl+C` to stop.

## Step 5: Running the Services

### Option A: Run Separately (Development)

**Terminal 1 - VM Manager:**
```bash
cd ~/IndiaHost
./vm-manager.sh
```

**Terminal 2 - Discord Bot:**
```bash
cd ~/IndiaHost
python3 discord_bot.py
```

### Option B: Background Services (Production)

#### Using systemd (Recommended)

Create service for Discord bot:

```bash
sudo tee /etc/systemd/system/indiahost-bot.service > /dev/null << EOF
[Unit]
Description=IndiaHost Discord Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/IndiaHost
ExecStart=/usr/bin/python3 $HOME/IndiaHost/discord_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable indiahost-bot
sudo systemctl start indiahost-bot

# Check status
sudo systemctl status indiahost-bot
```

#### Using nohup

```bash
# Start bot in background
nohup python3 ~/IndiaHost/discord_bot.py > ~/indiahost-bot.log 2>&1 &

# Check if running
ps aux | grep discord_bot.py

# View logs
tail -f ~/indiahost-bot.log
```

#### Using screen

```bash
# Install screen
sudo apt install screen

# Start bot in screen session
screen -S indiahost-bot
cd ~/IndiaHost
python3 discord_bot.py

# Detach: Ctrl+A then D
# Reattach: screen -r indiahost-bot
```

## Step 6: Verify Everything Works

### Test VM Manager

```bash
cd ~/IndiaHost
./vm-manager.sh
# Select option 1: Create a new VM (or just exit with 0)
```

### Test Discord Bot

In your Discord server:

```
!help_vms
```

You should see a list of available commands.

### Create a Test VM

In Discord:
```
!vm list
```

Should show "No VMs found" or list existing VMs.

## Step 7: Security Hardening

### Secure File Permissions

```bash
# Make scripts secure
chmod 700 ~/IndiaHost/vm-manager.sh
chmod 700 ~/IndiaHost/discord_bot.py
chmod 600 ~/IndiaHost/bot_config.json

# Secure VM directory
chmod 700 ~/vms
```

### Rotate Bot Token (If Compromised)

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click on your application
3. Go to "Bot" section
4. Click "Regenerate" next to token
5. Update `bot_config.json` with new token
6. Restart bot

### Limit User Access

Edit `bot_config.json` to add allowed users:

```json
{
    "token": "YOUR_BOT_TOKEN",
    "admin_role": "VM_Admin",
    "vm_dir": "/home/user/vms",
    "allowed_users": [123456789, 987654321]
}
```

Replace numbers with actual Discord user IDs.

## Troubleshooting

### KVM Not Available

```bash
# Check processor support
grep -o 'vmx\|svm' /proc/cpuinfo

# If empty, virtualization not enabled in BIOS
# Reboot and enter BIOS/UEFI to enable virtualization
```

### Dependencies Missing

```bash
# Re-run dependency installation
# Ubuntu
sudo apt install -y qemu-system cloud-image-utils wget lsof

# Or check what's missing
which qemu-system-x86_64
which cloud-localds
which wget
which lsof
```

### Bot Won't Connect

1. Check token is correct: `cat bot_config.json`
2. Check bot is in server
3. Check bot has permissions
4. Check Discord status: https://status.discord.com

### VM Manager Permission Denied

```bash
# Make executable
chmod +x vm-manager.sh

# Or run with bash
bash vm-manager.sh
```

### SSH Can't Connect

```bash
# Check SSH port (default 2222)
ssh -p 2222 ubuntu@localhost

# If connection refused, check VM is running
ps aux | grep qemu
```

## Next Steps

1. ✅ Create your first VM: `!vm list` → Create in menu
2. ✅ Start a VM: `!vm start <name>`
3. ✅ SSH into VM: `ssh -p <port> user@localhost`
4. ✅ Stop VM: `!vm stop <name>`
5. ✅ Monitor performance: `!vm performance <name>`

## Getting Help

- **VM Manager Questions**: Run `./vm-manager.sh` and explore menus
- **Discord Bot Help**: Type `!help_vms` in Discord
- **Issues**: Check troubleshooting section
- **GitHub Issues**: Open an issue on the repository

---

**Setup complete! You're ready to manage VMs with IndiaHost! 🚀**
