# 🚀 IndiaHost - Տեղադրում Հրահանգ (Հայերեն)

## ✅ Պահանջների Ցանկ

- [ ] Linux համակարգ KVM աջակցմամբ
- [ ] sudo/root մուտք
- [ ] Python 3.8+
- [ ] Discord սերվեր
- [ ] Discord բոտ token

## 1️⃣ Համակարգի Պատրաստում

### Կախվածությունների Տեղադրում

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

**Fedora/CentOS:**
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

## 2️⃣ Պահեստ Ճյուղավելի

```bash
cd ~
git clone https://github.com/PteroPlays/IndiaHost.git
cd IndiaHost
chmod +x vm-manager.sh
```

## 3️⃣ VM Manager Տեղադրում

```bash
mkdir -p ~/vms
chmod 700 ~/vms
./vm-manager.sh
```

## 4️⃣ Discord Բոտ Տեղադրում

### Discord Բոտ Ստեղծել

1. Գնալ https://discord.com/developers/applications
2. "New Application" ստեղծել
3. "Bot" → "Add Bot"
4. Token-ը պատճենել

### Բոտի Կազմաձեւ

```bash
pip3 install -r requirements.txt

cat > bot_config.json << EOF
{
    "token": "YOUR_DISCORD_BOT_TOKEN_HERE",
    "admin_role": "VM_Admin",
    "vm_dir": "$HOME/vms",
    "allowed_users": []
}
EOF

chmod 600 bot_config.json
python3 discord_bot.py
```

## 🎉 Սկսել Հիմա

```bash
# VM Manager
./vm-manager.sh

# Discord Բոտ
python3 discord_bot.py

# Discord-ում փորձել
!vm list
!help_vm
```

---

**✅ Տեղադրում Ավարտ!**
