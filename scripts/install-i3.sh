#!/usr/bin/env sh
set -e
echo "please read every message this gives you, before pressing enter"
sleep 1
sudo pacman -Syyu paru
paru -Syyu
paru -S i3 bluez blueman networkmanager-applet \
	picom dunst alacritty kitty emacs tint2 \
	nitrogen thorium sweet-themes beautyline \
	alacritty-themes git
