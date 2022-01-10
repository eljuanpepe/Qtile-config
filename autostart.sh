#!/bin/sh
setxkbmap latam
picom --experimental-backend --vsync &
nitrogen --restore
numlockx on
xinput set-prop "Elan Touchpad" "libinput Natural Scrolling Enabled" 1
xinput set-prop "Elan Touchpad" "libinput Tapping Enabled" 1
amixer set 'Master' 100%
