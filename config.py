# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
#  ______ _ _                                         
# |  ____| (_)                                        
# | |__  | |_ _   _  __ _ _ __  _ __   ___ _ __   ___ 
# |  __| | | | | | |/ _` | '_ \| '_ \ / _ \ '_ \ / _ \
# | |____| | | |_| | (_| | | | | |_) |  __/ |_) |  __/
# |______|_| |\__,_|\__,_|_| |_| .__/ \___| .__/ \___|
#         _/ |                 | |        | |         
#        |__/                  |_|        |_|         

from typing import List 
from libqtile import bar, layout, widget, qtile, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import os, subprocess

colors = ['#8be9fd', '#282a36',
          '#6272a4', '#50fa7b',
          '#8aaefc', '#ff5555',
          '#ffb86c']

mod = 'mod4'
terminal = 'kitty'
browser = 'qutebrowser'
home = os.path.expanduser('~')


def shutdown_menu():
    qtile.cmd_spawn(home + '/.config/qtile/shutdown.sh')

keys = [
    Key([mod], 
	"h", 
	lazy.layout.left(),
        desc="Move focus to left"),
    Key([mod], 
	"l", 
	lazy.layout.right(),
        desc="Move focus to right"),
    Key([mod], 
	"j",
	lazy.layout.down(),
        desc="Move focus down"),
    Key([mod],
	"k",
	lazy.layout.up(),
        desc="Move focus up"),
    Key([mod],
	"space",
	lazy.layout.next(),
        desc="Move window focus to other window"),
    Key([mod, "shift"],
	"h",
	lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod,
	"shift"],
	"l",
	lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod,
	"shift"],
	"j",
	lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, 
	"shift"], 
	"k", 
	lazy.layout.shuffle_up(), 
	desc="Move window up"),
    Key([mod,
	"control"], 
	"h", 
	lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, 
	"control"], 
	"l", 
	lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, 
	"control"], 
	"j", 
	lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, 
	"control"], 
	"k", 
	lazy.layout.grow_up(),
        desc="Grow window up"),
    Key([mod], 
	"n", 
	lazy.layout.normalize(),
        desc="Reset all window sizes"),
    Key([mod, 
	"shift"], 
	"Return", 
	lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], 
	"Return", 
	lazy.spawn(terminal),
        desc="Launch terminal"),
    Key([mod], 
	"Tab", 
	lazy.next_layout(),
        desc="Toggle between layouts"),
    Key([mod], 
	"w", 
	lazy.window.kill(),
        desc="Kill focused window"),
    Key([mod, 
	"control"], 
	"r", 
	lazy.restart(),
	desc="Restart Qtile"),
    Key([mod], 
	"q", 
	lazy.spawn(home + '/.config/qtile/shutdown.sh'),
	desc="Shutdown Qtile"),
    Key([mod], 
	"r", 
	lazy.spawn('rofi -modi "drun" -theme arc-dracula -show'),
        desc="Spawn a ROFI"),
    Key([mod], 
	"f", 
	lazy.spawn(browser),
        desc="Spawn browser"),
    Key([mod], 
	"v", 
	lazy.spawn('pcmanfm'), 
	desc="Spawn file manager"),
    Key([], 
	"XF86AudioRaiseVolume", 
	lazy.spawn("amixer -c 0 -q set Master 1dB+")),    
    Key([], 
	"XF86AudioLowerVolume", 
	lazy.spawn("amixer -c 0 -q set Master 1dB-")),    
    Key([], 
	"XF86AudioMute", 
	lazy.spawn("amixer -c 0 -q set Master toggle")),
    Key([],
        "Print",
        lazy.spawn("flameshot full -p Downloads/")),
    Key([mod],
	"Print",
	lazy.spawn("flameshot gui"))
]

grops = {
        1: Group("I"),
        2: Group("II"),
        3: Group ("III"),
        4: Group ("IV"),
        5: Group ("V"),
}

groups = [grops[i] for i in grops]

def get_key(name):
    return [k for k, g in grops.items() if g.name == name][0]

for i in groups:
    keys.extend([
        Key([mod], str(get_key(i.name)), lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        Key([mod, "shift"], str(get_key(i.name)), lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
            
        Key([mod, "control"], str(get_key(i.name)), lazy.window.togroup(i.name, switch_group=False),
            desc="move focused window to group {}".format(i.name)),
    ])

layout_theme = {
	"border_width": 3,
	"margin": 4,
	"border_focus": colors[2],
	"border_normal": colors[1]
}

layouts = [
    layout.Columns(
        **layout_theme,
        border_on_single=True,
        fair=True),
    layout.Max(),
    layout.Floating(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Ubuntu',
    fontsize=15,
    padding=3,
)

extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(
					custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")], 
					background=colors[2]),
                widget.GroupBox(this_screen_border=colors[2],
					this_current_screen_border=colors[2],
                    rounded=False,
                    highlight_method='line',
                    font='Ubuntu',
                    disable_drag=True, 
                    foreground='#5294e2',
                    inactive='#797d93',
                    borderwidth=4,
                    highlight_color=['#4b5162', '#4b5162'], 
                    urgent_border=colors[5],
                    ),
                widget.Prompt(),
                widget.Spacer(),
                widget.Chord(
                    chords_colors={
                        'launch': (colors[5], "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Systray(),
                widget.Sep(padding=6),
                widget.NetGraph(graph_color=colors[3],
                    fill_color=colors[3],
                    border_color=colors[2]),
                widget.Sep(padding=6),
                widget.TextBox(text='', 
                    foreground=colors[6]),
                widget.Volume(volume_app='pavucontrol', font='Ubuntu'),
                widget.Sep(),
                widget.Battery(update_interval=15,
                    format='{char}{percent: 2.0%}',
                    charge_char='',
                    discharge_char='',
                    empty_char='',
                    font='Ubuntu Condensed',
                    padding=6,
                    foreground=colors[3]),
                widget.Sep(), 
                widget.Clock(format="  %x |  🕔 %I:%M", 
                    foreground=colors[4],
                    font='Ubuntu Condensed',
                    padding=6),
                widget.Sep(),
                widget.TextBox(font='icons',
                    text='',
                    mouse_callbacks = {'Button1': shutdown_menu},
                    padding=6, 
                    foreground=colors[5]),
            ],
            24, background=colors[1]
        ),
    ),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
], **layout_theme)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

@hook.subscribe.startup_once
def start_once():
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
