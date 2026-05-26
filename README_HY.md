# 🏠 IndiaHost - Վիրտուալ Մեքենաների Կառավարման Համակարգ

IndiaHost-ը հանրային VM կառավարման համակարգ է, որն ապահովում է QEMU/KVM հիման վրա բազմաթիվ օպերացիոն համակարգեր հեշտ կառավարել:

## 🎯 Հատկանիշներ

### VM Manager (vm-manager.sh)
- ✨ **Բազմ OP Հաջողակցություն**: Ubuntu, Debian, Fedora, CentOS, AlmaLinux, Rocky Linux
- 🚀 **Լիակազմ VM Ցիկլ**: Ստեղծել, գործարկել, կանգնեցնել, ջնջել, խմբագրել
- 📊 **Կատարման Մոնիտորում**: Իրական ժամանակ CPU, Հիշողություն, Սկավառակ
- 🔧 **Բարձր Հատկանիշներ**: Սկավառակի վերափոխել, SSH Պորտեր, Պորտ Ուղղորդում, GUI/Console
- 🛡️ **Անվտանգ Կողպեքներ**: Գործընթացի կողպեքներ, հնամաշ կողպեքներ
- 🎨 **Հարուստ Ինտերֆեյս**: Գույնային ելք emoji-ներով

### Discord Բոտ (discord_bot.py)
- 💬 **Discord Հրամաններ**: Discord-ից VM կառավարել
- 🔐 **Դերային Մուտք**: VM_Admin դերի ստուգում
- 📊 **Իրական Կարգավիճակ**: VM կարգավիճակ և կատարում տեսնել
- ⚠️ **Հաստատում Երկխոսություններ**: Անվտանգ ջնջումներ
- 📋 **Մանրամասն Օգնություն**: Ներկառուցված հրամանի փաստաթղթեր

## 📋 Պահանջներ

### Համակարգի Պահանջներ
- Linux (Ubuntu, Debian, Fedora, CentOS և այլն)
- QEMU/KVM Վիրտուալացման Աջակցություն
- KVM Միացված BIOS-ում
- Նվազ 2GB RAM VM-ի համար
- Բավական սկավառակի տեղ VM պատկերների համար

### Կախվածություններ
- `qemu-system-x86_64` - QEMU Համակարգ
- `wget` - Պատկերների Ներբեռնում
- `cloud-localds` - Cloud-init Մշակ
- `qemu-img` - Սկավառակի Պատկերի Գործիքներ
- `lsof` - Գործընթաց/Ֆայլի Կողպեկ Հայտնաբերում

## 🚀 Արագ Մեկնարկ

### 1. VM Manager Տեղադրում

```bash
git clone https://github.com/PteroPlays/IndiaHost.git
cd IndiaHost
chmod +x vm-manager.sh
./vm-manager.sh
```

### 2. Discord Բոտ Տեղադրում

```bash
pip install discord.py
cat > bot_config.json << EOF
{
    "token": "YOUR_DISCORD_BOT_TOKEN",
    "admin_role": "VM_Admin",
    "vm_dir": "$HOME/vms",
    "allowed_users": []
}
EOF
python3 discord_bot.py
```

## 📖 Discord Բոտ Հրամաններ

```
!vm list              - Բոլոր VM-ներ
!vm start <name>      - VM Գործարկել
!vm stop <name>       - VM Կանգնեցնել
!vm info <name>       - VM Տեղեկություն
!vm delete <name>     - VM Ջնջել
!vm performance <name> - VM Կատարում
!vmstatus             - Բոլոր Կարգավիճակ
!help_vm              - Բոլոր Հրամաններ
```

## 🌐 Աջակցվող Օպերացիոն Համակարգեր

| OP | Տարբերակ | Կարգավիճակ |
|---|---|---|
| Ubuntu | 22.04, 24.04 | ✅ |
| Debian | 11, 12, 13 | ✅ |
| Fedora | 40 | ✅ |
| CentOS | Stream 9 | ✅ |
| AlmaLinux | 9 | ✅ |
| Rocky Linux | 9 | ✅ |

---

**Պատրաստ ❤️ Հեշտ VM Կառավարման Համար**
