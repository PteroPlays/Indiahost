#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IndiaHost Discord Բոտ
Virtual Machine Management համակարգի համար
"""

import discord
from discord.ext import commands
import subprocess
import os
import json
import asyncio
import logging

logging.basicConfig(level=logging.INFO, encoding='utf-8')
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

CONFIG_FILE = "bot_config.json"
VM_DIR = os.path.expanduser("~/vms")

def load_config():
    """Բերել կազմաձեւ"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return get_default_config()
    return get_default_config()

def get_default_config():
    """Հիմնական կազմաձեւ"""
    return {
        "token": "YOUR_DISCORD_BOT_TOKEN",
        "admin_role": "VM_Admin",
        "vm_dir": os.path.expanduser("~/vms"),
        "allowed_users": []
    }

def is_admin(ctx):
    """Ստուգել թե օգտատերը վարիչ է"""
    config = load_config()
    admin_role = config.get("admin_role", "VM_Admin")
    return any(role.name == admin_role for role in ctx.author.roles)

def get_vm_list():
    """Բոլոր VM-ների ցանկ"""
    try:
        config = load_config()
        vm_dir = config.get("vm_dir", VM_DIR)
        if not os.path.exists(vm_dir):
            return []
        vms = [f[:-5] for f in os.listdir(vm_dir) if f.endswith('.conf')]
        return sorted(vms)
    except:
        return []

def is_vm_running(vm_name):
    """Ստուգել թե VM-ը գործարկված է"""
    try:
        result = subprocess.run(
            f"pgrep -f 'qemu-system.*{vm_name}' >/dev/null 2>&1",
            shell=True
        )
        return result.returncode == 0
    except:
        return False

def run_vm_command(command, vm_name=None):
    """VM հրաման գործարկել"""
    try:
        config = load_config()
        vm_dir = config.get("vm_dir", VM_DIR)
        
        if vm_name:
            cmd = f"bash vm-manager.sh {command} {vm_name} 2>&1"
        else:
            cmd = f"bash vm-manager.sh {command} 2>&1"
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout + result.stderr
        success = result.returncode == 0
        
        return success, output[:1500]
    except subprocess.TimeoutExpired:
        return False, "❌ Հրամանը ժամանակ շատ էր (30վ)"
    except Exception as e:
        return False, f"❌ Սխալ: {str(e)}"

@bot.event
async def on_ready():
    """Բոտ պատրաստ"""
    logger.info(f'✅ IndiaHost Բոտ միացել է {bot.user}')
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="VM-ներ 🖥️"
        )
    )

@bot.command(name='vm', help='VM կառավարման հրամաններ')
@commands.check(is_admin)
async def vm_command(ctx, action: str = None, vm_name: str = None):
    """VM հրամաններ"""
    if not action:
        embed = discord.Embed(
            title="❌ Սխալ",
            description="Օգտագործում: `!vm <action> [vm_name]`\n\nՀրամաններ: list, start, stop, info, delete, performance, fix",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    if action == 'list':
        vms = get_vm_list()
        if not vms:
            embed = discord.Embed(
                title="📁 VM ցանկ",
                description="Վիրտուալ մեքենաներ չեն գտնվել",
                color=discord.Color.blue()
            )
        else:
            vm_info = []
            for vm in vms:
                status = "🚀 Գործարկված" if is_vm_running(vm) else "💤 Կանգ"
                vm_info.append(f"`{vm}` - {status}")
            embed = discord.Embed(
                title="📁 VM ցանկ",
                description="\n".join(vm_info),
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Ընդամենը: {len(vms)} VM")
        await ctx.send(embed=embed)

    elif action == 'start':
        if not vm_name:
            await ctx.send("❌ Նշեք VM-ի անունը: `!vm start <vm_name>`")
            return
        async with ctx.typing():
            success, output = run_vm_command('start', vm_name)
            embed = discord.Embed(
                title=f"{'✅' if success else '❌'} VM գործարկել - {vm_name}",
                description=f"```{output[:1024]}```",
                color=discord.Color.green() if success else discord.Color.red()
            )
            await ctx.send(embed=embed)

    elif action == 'stop':
        if not vm_name:
            await ctx.send("❌ Նշեք VM-ի անունը: `!vm stop <vm_name>`")
            return
        async with ctx.typing():
            success, output = run_vm_command('stop', vm_name)
            embed = discord.Embed(
                title=f"{'✅' if success else '❌'} VM կանգնեցնել - {vm_name}",
                description=f"```{output[:1024]}```",
                color=discord.Color.green() if success else discord.Color.red()
            )
            await ctx.send(embed=embed)

    elif action == 'info':
        if not vm_name:
            await ctx.send("❌ Նշեք VM-ի անունը: `!vm info <vm_name>`")
            return
        async with ctx.typing():
            success, output = run_vm_command('info', vm_name)
            embed = discord.Embed(
                title=f"📊 VM տեղեկություն - {vm_name}",
                description=f"```{output[:1024]}```",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)

    elif action == 'delete':
        if not vm_name:
            await ctx.send("❌ Նշեք VM-ի անունը: `!vm delete <vm_name>`")
            return
        
        embed = discord.Embed(
            title="⚠️ VM ջնջել - Հաստատում",
            description=f"Պաղատ ունեք ջնջել `{vm_name}` VM-ը?\nԱյս գործողությունը անվերականգ է!",
            color=discord.Color.red()
        )
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['✅', '❌']
        
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
            if str(reaction.emoji) == '✅':
                async with ctx.typing():
                    success, output = run_vm_command('delete', vm_name)
                    embed = discord.Embed(
                        title=f"{'✅' if success else '❌'} VM ջնջվել - {vm_name}",
                        description=f"```{output[:1024]}```",
                        color=discord.Color.green() if success else discord.Color.red()
                    )
                    await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Ջնջումը չեղարկվեց")
        except asyncio.TimeoutError:
            await ctx.send("⏱️ Հաստատումը ժամանականց եղավ")

    elif action == 'performance':
        if not vm_name:
            await ctx.send("❌ Նշեք VM-ի անունը: `!vm performance <vm_name>`")
            return
        async with ctx.typing():
            success, output = run_vm_command('performance', vm_name)
            embed = discord.Embed(
                title=f"📈 VM կատարումը - {vm_name}",
                description=f"```{output[:1024]}```",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)

    elif action == 'fix':
        if not vm_name:
            await ctx.send("❌ Նշեք VM-ի անունը: `!vm fix <vm_name>`")
            return
        async with ctx.typing():
            success, output = run_vm_command('fix', vm_name)
            embed = discord.Embed(
                title=f"🔧 VM շտկել - {vm_name}",
                description=f"```{output[:1024]}```",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="❌ Անհայտ գործողություն",
            description="Գործողությունները: list, start, stop, info, delete, performance, fix",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.command(name='vmstatus', help='Բոլոր VM-ների կարգավիճակ')
async def vmstatus(ctx):
    """VM-ների կարգավիճակ"""
    vms = get_vm_list()
    if not vms:
        embed = discord.Embed(
            title="📊 VM կարգավիճակ",
            description="Վիրտուալ մեքենաներ չեն գտնվել",
            color=discord.Color.blue()
        )
    else:
        status_info = []
        running = 0
        stopped = 0
        
        for vm in vms:
            is_running = is_vm_running(vm)
            if is_running:
                status_info.append(f"🚀 `{vm}` - Գործարկված")
                running += 1
            else:
                status_info.append(f"💤 `{vm}` - Կանգ")
                stopped += 1
        
        embed = discord.Embed(
            title="📊 VM կարգավիճակ",
            description="\n".join(status_info),
            color=discord.Color.blue()
        )
        embed.add_field(name="🚀 Գործարկված", value=str(running), inline=True)
        embed.add_field(name="💤 Կանգ", value=str(stopped), inline=True)
        embed.add_field(name="📁 Ընդամենը", value=str(len(vms)), inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='help_vm', help='VM հրամանների օգնություն')
async def help_vm(ctx):
    """VM հրամանների օգնություն"""
    embed = discord.Embed(
        title="🔧 IndiaHost VM Հրամաններ",
        color=discord.Color.blue()
    )
    
    commands_info = [
        ("**!vm list**", "Բոլոր VM-ների ցանկ տեսնել"),
        ("**!vm start <name>**", "VM գործարկել"),
        ("**!vm stop <name>**", "VM կանգնեցնել"),
        ("**!vm info <name>**", "VM տեղեկություն"),
        ("**!vm delete <name>**", "VM ջնջել (հաստատում)"),
        ("**!vm performance <name>**", "VM կատարում"),
        ("**!vm fix <name>**", "VM շտկել"),
        ("**!vmstatus**", "Բոլոր VM-ների կարգավիճակ"),
    ]
    
    for cmd, desc in commands_info:
        embed.add_field(name=cmd, value=desc, inline=False)
    
    embed.set_footer(text="Միայն VM_Admin դերի օգտատերները կարող են հրամաններ գործարկել")
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    """Սխալների մշակում"""
    if isinstance(error, commands.MissingRole):
        embed = discord.Embed(
            title="❌ Մուտք մերժված",
            description="Դուք չունեք թույլտվություն այս հրամանը գործարկել",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.NotOwner):
        embed = discord.Embed(
            title="❌ Միայն տեր",
            description="Միայն բոտի տերը կարող է գործարկել այս հրամանը",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        logger.error(f"Սխալ: {error}")

def main():
    """Բոտ գործարկել"""
    config = load_config()
    token = config.get("token")
    
    if token == "YOUR_DISCORD_BOT_TOKEN":
        logger.error("❌ խնդրում ենք սահմանել Discord բոտի token-ը bot_config.json ֆայլում")
        return
    
    try:
        bot.run(token)
    except Exception as e:
        logger.error(f"❌ Բոտ գործարկել չկարողացա: {e}")

if __name__ == "__main__":
    main()
