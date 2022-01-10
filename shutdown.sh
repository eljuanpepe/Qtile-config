#!/bin/bash

#original code: https://github.com/dvogeldev/amber-dracula

rofi_command="rofi -theme powermenu"

#### Options ###
shutdown=""
reboot=""
suspend=""
logout=""

options="$shutdown\n$reboot\n$suspend\n$logout"

chosen="$(echo -e "$options" | $rofi_command -dmenu -selected-row 0)"
case $chosen in   
    $shutdown)
        systemctl poweroff
        ;;
    $reboot)
        systemctl reboot
        ;;
    $suspend)
	    systemctl suspend
        ;;
    $logout)
        qtile cmd-obj -o cmd -f shutdown	
	;;
esac

