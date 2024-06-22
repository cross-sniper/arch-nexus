#!/usr/bin/env python3

import os
import time
import json
import subprocess

print("arch-nexus v1")

print("This is the setup script for arch-nexus.")
print("It will ask you some questions about what you want to install.")
print("If at any point you decide to not go forward with the installation,")
print("you can press <CTRL+C> to cancel it.")
print("Although that will not undo any changes already made, sadly.")

time.sleep(3)

# Assuming there is a 'scripts' directory with installation scripts
if not os.path.exists("scripts"):
    print("The 'scripts' directory does not exist. Exiting.")
    exit(1)

scripts = [f[len('install-'):-3] for f in os.listdir("scripts") if f.startswith('install-') and f.endswith('.sh')]

def get_preferred_install():
    print("Available scripts:")
    for i, script in enumerate(scripts, start=1):
        print(f"{i}. {script}")
    
    choice = input("Select one (by number or name): ")
    try:
        choice = int(choice)
        if 1 <= choice <= len(scripts):
            return scripts[choice - 1]
    except ValueError:
        if choice in scripts:
            return choice

    print("Invalid choice, please try again.")
    return get_preferred_install()

preferred_install = get_preferred_install()

CHAOTIC_AUR_INCLUDE = """
[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist
"""

PRE_RUN = """
pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
pacman-key --lsign-key 3056513887B78AEB
pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst'
pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'
"""

def update_pacman_conf():
    with open("/etc/pacman.conf", "a+", encoding="utf8") as f:
        f.seek(0)
        content = f.read()
        if CHAOTIC_AUR_INCLUDE not in content:
            f.write(CHAOTIC_AUR_INCLUDE)
            print("Added Chaotic AUR to pacman.conf")

def run_pre_commands():
    print("Running pre-commands to set up Chaotic AUR...")
    commands = PRE_RUN.strip().split('\n')
    for cmd in commands:
        subprocess.run(cmd, shell=True, check=True)

def run_install_script(script_name):
    script_path = os.path.join("scripts", f"install-{script_name}.sh")
    if os.path.exists(script_path):
        print(f"Running {script_path}...")
        subprocess.run(f"bash {script_path}", shell=True, check=True)
    else:
        print(f"Script {script_path} not found. Exiting.")
        exit(1)

# Updating pacman.conf to include Chaotic AUR
update_pacman_conf()

# Running pre-commands
run_pre_commands()

# Running the preferred installation script
run_install_script(preferred_install)

print("Setup complete!")
