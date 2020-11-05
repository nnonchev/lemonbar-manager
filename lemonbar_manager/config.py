_modules = {
    "left": {
        "desktops": "%{O10}...%{O10}",
    },
    "center": {
        "node": "%{O10}...%{O10}",
    },
    "right": {
        "battery": "%{O10}...%{O10}",
        "date_time": "%{O10}...%{O10}",
    },
}

bar_config = {
    "geometry": "1920x36+0+0",
    "fg_color": "${foreground}",
    "bg_color": "${background}",
    "u_color": "${background}",
    "font_size": "13",
    "u_pixels": "3",
    "fonts": [
        "Hack Nerd Font Mono:style=Bold Italic",
    ],
    "modules": _modules,
    "alpha": "D0",
}


to_update = [
    (1, ["lemonc", "date-time"]),
    (5, ["lemonc", "battery"]),
]


to_subscribe = [
    (["bspc", "subscribe", "desktop_focus"], ["lemonc", "bspwm-desktops"]),
    (["bspc", "subscribe", "node_focus"], ["lemonc", "bspwm-desktops"]),
    (["bspc", "subscribe", "node_transfer"], ["lemonc", "bspwm-desktops"]),
    (["bspc", "subscribe", "node_focus"], ["lemonc", "bspwm-node"]),
]
