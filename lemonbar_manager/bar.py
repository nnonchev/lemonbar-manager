import os
import asyncio
from random import choice
from functools import reduce
from typing import Optional, Dict, List

import pywal


class Wallpaper:
    def __init__(self, *,
                 dir: Optional[str] = os.path.join(
                     os.path.expanduser("~"), "wallpapers"),
                 img: Optional[str] = None,
                 alpha: Optional[str] = "FF",
                 ):
        self.dir = dir
        self.img = (
            img
            if img is not None else
            choice(os.listdir(dir))
        )
        self.alpha = alpha

    def set_dir(self, dir):
        self.dir = dir

    def get_dir(self):
        return self.dir

    def set_img(self, img):
        self.img = img

    def get_img(self):
        return self.img

    def set_alpha(self, alpha):
        self.alpha = alpha

    def get_alpha(self):
        return self.alpha

    def set_random_img(self):
        self.img = choice(os.listdir(self.dir))

    def config_wallpaper(self):
        img_path = os.path.join(self.dir, self.img)

        if os.path.isfile(img_path):
            pywal.wallpaper.change(img_path)

    def get_colors(self):
        img_path = os.path.join(self.dir, self.img)
        return pywal.colors.get(img_path)

    def replace_colors(self, string):
        colors = self.get_colors()
        colors = {
            "foreground": colors["special"]["foreground"],
            "background": colors["special"]["background"],
            "color0": colors["colors"]["color0"],
            "color1": colors["colors"]["color1"],
            "color2": colors["colors"]["color2"],
            "color3": colors["colors"]["color3"],
            "color4": colors["colors"]["color4"],
            "color5": colors["colors"]["color5"],
            "color6": colors["colors"]["color6"],
            "color7": colors["colors"]["color7"],
            "color8": colors["colors"]["color8"],
            "color9": colors["colors"]["color9"],
            "color10": colors["colors"]["color10"],
            "color11": colors["colors"]["color11"],
            "color12": colors["colors"]["color12"],
            "color13": colors["colors"]["color13"],
            "color14": colors["colors"]["color14"],
            "color15": colors["colors"]["color15"],
        }

        # Insert alpha
        for key in colors.keys():
            colors[key] = colors[key][0] + self.alpha + colors[key][1:]

        # replace colors
        string = (
            string
            .replace("${foreground}", colors["foreground"])
            .replace("${background}", colors["background"])
            .replace("${color0}", colors["color0"])
            .replace("${color1}", colors["color1"])
            .replace("${color2}", colors["color2"])
            .replace("${color3}", colors["color3"])
            .replace("${color4}", colors["color4"])
            .replace("${color5}", colors["color5"])
            .replace("${color6}", colors["color6"])
            .replace("${color7}", colors["color7"])
            .replace("${color8}", colors["color8"])
            .replace("${color9}", colors["color9"])
            .replace("${color10}", colors["color10"])
            .replace("${color11}", colors["color11"])
            .replace("${color12}", colors["color12"])
            .replace("${color13}", colors["color13"])
            .replace("${color14}", colors["color14"])
            .replace("${color15}", colors["color15"])
        )

        return string


class Bar:
    def __init__(self, *,
                 geometry: Optional[str] = "1920x30+0+0",
                 bg_color: Optional[str] = "#000000",
                 fg_color: Optional[str] = "#FFFFFF",
                 offset: Optional[str] = "0",
                 u_color: Optional[str] = "#000000",
                 u_pixels: Optional[str] = "0",
                 font_size: Optional[str] = "13",
                 fonts: Optional[List[str]] = [],
                 on_bottom: Optional[bool] = True,
                 modules: Optional[Dict[str, Dict[str, str]]] = {
                     "left": {}, "center": {}, "right": {}},
                 dir: Optional[str] = os.path.join(
                     os.path.expanduser("~"), "wallpapers"),
                 img: Optional[str] = None,
                 alpha: Optional[str] = "FF",
                 ):

        self.wallpaper = Wallpaper(dir=dir, img=img, alpha=alpha)
        self.wallpaper.config_wallpaper()

        self.options = {
            "-g": geometry,
            "-B": bg_color,
            "-F": fg_color,
            "-o": offset,
            "-U": u_color,
            "-u": u_pixels,
        }

        self.font_size = font_size
        self.fonts = fonts

        self.on_bottom = on_bottom

        self.modules = modules

        self.cmd = ["lemonbar"]
        self.ps = None

    def set_opt(self, key, val):
        if key in self.options.keys():
            self.options[key] = val

    def get_opt(self, key):
        return self.options.get(key)

    def add_font(self, font):
        if font not in self.fonts:
            self.fonts.append(font)

    def remove_font(self, font):
        if font in self.fonts:
            self.fonts.remove(font)

    def get_fonts(self):
        return "\n".join(self.fonts)

    def clear_fonts(self):
        self.fonts.clear()

    def set_font_size(self, new_size):
        self.font_size = new_size

    def get_font_size(self):
        return self.font_size

    def set_wallpaper(self, img_path):
        self.wallpaper.set_img(img_path)
        self.wallpaper.config_wallpaper()

    def set_random_wallpaper(self):
        self.wallpaper.set_random_img()
        self.wallpaper.config_wallpaper()

    def get_wallpaper(self):
        return self.wallpaper.get_img()

    def get_theme_colors(self):
        return self.wallpaper.get_colors()

    def update_mod(self, mod_id, mod_val):
        if mod_id in self.modules.get("before_left", {}).keys():
            self.modules["before_left"][mod_id] = mod_val
        elif mod_id in self.modules.get("left", {}).keys():
            self.modules["left"][mod_id] = mod_val
        elif mod_id in self.modules.get("center", {}).keys():
            self.modules["center"][mod_id] = mod_val
        elif mod_id in self.modules.get("right", {}).keys():
            self.modules["right"][mod_id] = mod_val

    async def parse(self, obj):
        cmd = obj.get("cmd")
        key = obj.get("key")
        val = obj.get("val")

        # Assume no reply
        rep = None

        api_mutators = {

            # Sets lemonbar's global option
            "set_opt": lambda: self.set_opt(key, val),

            # Add a font
            "add_font": lambda: self.add_font(val),

            # Remove a font
            "remove_font": lambda: self.remove_font(val),

            # Clear all fonts
            "clear_fonts": self.clear_fonts,

            # Set font size
            "set_font_size": lambda: self.set_font_size(val),

            # Set wallpaper
            "set_wallpaper": lambda: self.set_wallpaper(val),

            # Set random wallpaper
            "set_random_wallpaper": self.set_random_wallpaper,

            # Set alpha
            "set_alpha": lambda: self.wallpaper.set_alpha(val),

        }

        api_accessors = {

            # Get lemonbar's global option
            "get_opt": lambda: self.get_opt(key),

            # Get all fonts
            "get_fonts": self.get_fonts,

            # Get font size
            "get_font_size": self.get_font_size,

            # Get wallpaper
            "get_wallpaper": self.get_wallpaper,

            # Get theme colors
            "get_colors": self.get_theme_colors,

            # Get alpha
            "get_alpha": self.wallpaper.get_alpha,

        }

        if cmd in api_mutators.keys():
            api_mutators[cmd]()
            await self.reload_bar()
        elif cmd in api_accessors.keys():
            rep = api_accessors[cmd]()
            # In case it's a color
            rep = self.wallpaper.replace_colors(rep)
        elif cmd == "update_mod":
            self.update_mod(key, val)
            self.flush_mods()
        else:
            # Unknown cmd
            rep = {"error": f"Unknown command: { cmd }"}

        return rep or {}

    def build_cmd(self):
        options = []

        for key, val in self.options.items():
            options.append(key)

            if key in ("-F", "-B", "-U"):
                val = self.wallpaper.replace_colors(val)
            options.append(val)

        if self.on_bottom:
            options.append("-b")

        fonts = [
            f"-f {font}:size={self.font_size}"
            for font in self.fonts
        ]

        return [*self.cmd, *options, *fonts]

    def build_modules(self):
        before_left = "".join(self.modules.get("before_left", {}).values())
        left = "".join(self.modules.get("left", {}).values())
        center = "".join(self.modules.get("center", {}).values())
        right = "".join(self.modules.get("right", {}).values())

        complete = f"{before_left}%{{l}}{left}%{{c}}{center}%{{r}}{right}"
        complete = self.wallpaper.replace_colors(complete)

        return complete

    def flush_mods(self):
        if self.ps is not None:import os
import asyncio
from random import choice
from functools import reduce
from typing import Optional, Dict, List

import pywal


class Wallpaper:
    def __init__(self, *,
                 dir: Optional[str] = os.path.join(
                     os.path.expanduser("~"), "wallpapers"),
                 img: Optional[str] = None,
                 alpha: Optional[str] = "FF",
                 ):
        self.dir = dir
        self.img = (
            img
            if img is not None else
            choice(os.listdir(dir))
        )
        self.alpha = alpha

    def set_dir(self, dir):
        self.dir = dir

    def get_dir(self):
        return self.dir

    def set_img(self, img):
        self.img = img

    def get_img(self):
        return self.img

    def set_alpha(self, alpha):
        self.alpha = alpha

    def get_alpha(self):
        return self.alpha

    def set_random_img(self):
        self.img = choice(os.listdir(self.dir))

    def config_wallpaper(self):
        img_path = os.path.join(self.dir, self.img)

        if os.path.isfile(img_path):
            pywal.wallpaper.change(img_path)

    def get_colors(self):
        img_path = os.path.join(self.dir, self.img)
        return pywal.colors.get(img_path)

    def replace_colors(self, string):
        colors = self.get_colors()
        colors = {
            "foreground": colors["special"]["foreground"],
            "background": colors["special"]["background"],
            "color0": colors["colors"]["color0"],
            "color1": colors["colors"]["color1"],
            "color2": colors["colors"]["color2"],
            "color3": colors["colors"]["color3"],
            "color4": colors["colors"]["color4"],
            "color5": colors["colors"]["color5"],
            "color6": colors["colors"]["color6"],
            "color7": colors["colors"]["color7"],
            "color8": colors["colors"]["color8"],
            "color9": colors["colors"]["color9"],
            "color10": colors["colors"]["color10"],
            "color11": colors["colors"]["color11"],
            "color12": colors["colors"]["color12"],
            "color13": colors["colors"]["color13"],
            "color14": colors["colors"]["color14"],
            "color15": colors["colors"]["color15"],
        }

        # Insert alpha
        for key in colors.keys():
            colors[key] = colors[key][0] + self.alpha + colors[key][1:]

        # replace colors
        string = (
            string
            .replace("${foreground}", colors["foreground"])
            .replace("${background}", colors["background"])
            .replace("${color0}", colors["color0"])
            .replace("${color1}", colors["color1"])
            .replace("${color2}", colors["color2"])
            .replace("${color3}", colors["color3"])
            .replace("${color4}", colors["color4"])
            .replace("${color5}", colors["color5"])
            .replace("${color6}", colors["color6"])
            .replace("${color7}", colors["color7"])
            .replace("${color8}", colors["color8"])
            .replace("${color9}", colors["color9"])
            .replace("${color10}", colors["color10"])
            .replace("${color11}", colors["color11"])
            .replace("${color12}", colors["color12"])
            .replace("${color13}", colors["color13"])
            .replace("${color14}", colors["color14"])
            .replace("${color15}", colors["color15"])
        )

        return string


class Bar:
    def __init__(self, *,
                 geometry: Optional[str] = "1920x30+0+0",
                 bg_color: Optional[str] = "#000000",
                 fg_color: Optional[str] = "#FFFFFF",
                 offset: Optional[str] = "0",
                 u_color: Optional[str] = "#000000",
                 u_pixels: Optional[str] = "0",
                 font_size: Optional[str] = "13",
                 fonts: Optional[List[str]] = [],
                 on_bottom: Optional[bool] = True,
                 modules: Optional[Dict[str, Dict[str, str]]] = {
                     "left": {}, "center": {}, "right": {}},
                 dir: Optional[str] = os.path.join(
                     os.path.expanduser("~"), "wallpapers"),
                 img: Optional[str] = None,
                 alpha: Optional[str] = "FF",
                 ):

        self.wallpaper = Wallpaper(dir=dir, img=img, alpha=alpha)
        self.wallpaper.config_wallpaper()

        self.options = {
            "-g": geometry,
            "-B": bg_color,
            "-F": fg_color,
            "-o": offset,
            "-U": u_color,
            "-u": u_pixels,
        }

        self.font_size = font_size
        self.fonts = fonts

        self.on_bottom = on_bottom

        self.modules = modules

        self.cmd = ["lemonbar"]
        self.ps = None

    def set_opt(self, key, val):
        if key in self.options.keys():
            self.options[key] = val

    def get_opt(self, key):
        return self.options.get(key)

    def add_font(self, font):
        if font not in self.fonts:
            self.fonts.append(font)

    def remove_font(self, font):
        if font in self.fonts:
            self.fonts.remove(font)

    def get_fonts(self):
        return "\n".join(self.fonts)

    def clear_fonts(self):
        self.fonts.clear()

    def set_font_size(self, new_size):
        self.font_size = new_size

    def get_font_size(self):
        return self.font_size

    def set_wallpaper(self, img_path):
        self.wallpaper.set_img(img_path)
        self.wallpaper.config_wallpaper()

    def set_random_wallpaper(self):
        self.wallpaper.set_random_img()
        self.wallpaper.config_wallpaper()

    def get_wallpaper(self):
        return self.wallpaper.get_img()

    def get_theme_colors(self):
        return self.wallpaper.get_colors()

    def update_mod(self, mod_id, mod_val):
        if mod_id in self.modules.get("before_left", {}).keys():
            self.modules["before_left"][mod_id] = mod_val
        elif mod_id in self.modules.get("left", {}).keys():
            self.modules["left"][mod_id] = mod_val
        elif mod_id in self.modules.get("center", {}).keys():
            self.modules["center"][mod_id] = mod_val
        elif mod_id in self.modules.get("right", {}).keys():
            self.modules["right"][mod_id] = mod_val

    async def parse(self, obj):
        cmd = obj.get("cmd")
        key = obj.get("key")
        val = obj.get("val")

        # Assume no reply
        rep = None

        api_mutators = {

            # Sets lemonbar's global option
            "set_opt": lambda: self.set_opt(key, val),

            # Add a font
            "add_font": lambda: self.add_font(val),

            # Remove a font
            "remove_font": lambda: self.remove_font(val),

            # Clear all fonts
            "clear_fonts": self.clear_fonts,

            # Set font size
            "set_font_size": lambda: self.set_font_size(val),

            # Set wallpaper
            "set_wallpaper": lambda: self.set_wallpaper(val),

            # Set random wallpaper
            "set_random_wallpaper": self.set_random_wallpaper,

            # Set alpha
            "set_alpha": lambda: self.wallpaper.set_alpha(val),

        }

        api_accessors = {

            # Get lemonbar's global option
            "get_opt": lambda: self.get_opt(key),

            # Get all fonts
            "get_fonts": self.get_fonts,

            # Get font size
            "get_font_size": self.get_font_size,

            # Get wallpaper
            "get_wallpaper": self.get_wallpaper,

            # Get theme colors
            "get_colors": self.get_theme_colors,

            # Get alpha
            "get_alpha": self.wallpaper.get_alpha,

        }

        if cmd in api_mutators.keys():
            api_mutators[cmd]()
            await self.reload_bar()
        elif cmd in api_accessors.keys():
            rep = api_accessors[cmd]()
            # In case it's a color
            rep = self.wallpaper.replace_colors(rep)
        elif cmd == "update_mod":
            self.update_mod(key, val)
            self.flush_mods()
        else:
            # Unknown cmd
            rep = {"error": f"Unknown command: { cmd }"}

        return rep or {}

    def build_cmd(self):
        options = []

        for key, val in self.options.items():
            options.append(key)

            if key in ("-F", "-B", "-U"):
                val = self.wallpaper.replace_colors(val)
            options.append(val)

        if self.on_bottom:
            options.append("-b")

        fonts = [
            f"-f {font}:size={self.font_size}"
            for font in self.fonts
        ]

        return [*self.cmd, *options, *fonts]

    def build_modules(self):
        before_left = "".join(self.modules.get("before_left", {}).values())
        left = "".join(self.modules.get("left", {}).values())
        center = "".join(self.modules.get("center", {}).values())
        right = "".join(self.modules.get("right", {}).values())

        complete = f"{before_left}%{{l}}{left}%{{c}}{center}%{{r}}{right}"
        complete = self.wallpaper.replace_colors(complete)

        return complete

    def flush_mods(self):
        if self.ps is not None:
            mods = self.build_modules()
            mods = mods.encode()

            self.ps.stdin.write(mods)

    async def reload_bar(self):
        tmp = self.ps

        cmd = self.build_cmd()

        self.ps = await asyncio.create_subprocess_exec(*cmd, stdin=asyncio.subprocess.PIPE)

        self.flush_mods()

        if tmp is not None:
            # Needed for smoother transition
            await asyncio.sleep(.5)

            tmp.stdin.close()
            await tmp.wait()

        # Needed so lemonbar goes behind full-screen programs
        await self.fix_lemonbar()

    async def fix_lemonbar(self):
        await asyncio.sleep(1)
        _ps1 = await asyncio.create_subprocess_exec("xdo", "id", "-n", "root",
                                                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        out1, err1 = await _ps1.communicate()
        if _ps1.returncode != 0:
            raise Exception(err1.decode())

        _ps2 = await asyncio.create_subprocess_exec("xdo", "id", "-n", "lemonbar",
                                                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        out2, err2 = await _ps2.communicate()
        if _ps2.returncode != 0:
            raise Exception("Error: ", err2.decode())

        out1 = out1.decode().strip()
        out2 = out2.decode().strip()

        _ps3 = await asyncio.create_subprocess_exec("xdo", "above", "-t", out1, out2,
                                                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        _, err3 = await _ps3.communicate()
        if _ps3.returncode != 0:
            raise Exception(err3.decode())

    async def __aenter__(self):
        await self.reload_bar()
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        self.ps.stdin.close()
        await self.ps.wait()

    async def reload_bar(self):
        tmp = self.ps

        cmd = self.build_cmd()

        self.ps = await asyncio.create_subprocess_exec(*cmd, stdin=asyncio.subprocess.PIPE)

        self.flush_mods()

        if tmp is not None:
            # Needed for smoother transition
            await asyncio.sleep(.5)

            tmp.stdin.close()
            await tmp.wait()

        # Needed so lemonbar goes behind full-screen programs
        await self.fix_lemonbar()

    async def fix_lemonbar(self):
        await asyncio.sleep(1)
        _ps1 = await asyncio.create_subprocess_exec("xdo", "id", "-n", "root",
                                                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        out1, err1 = await _ps1.communicate()
        if _ps1.returncode != 0:
            raise Exception(err1.decode())

        _ps2 = await asyncio.create_subprocess_exec("xdo", "id", "-n", "lemonbar",
                                                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        out2, err2 = await _ps2.communicate()
        if _ps2.returncode != 0:
            raise Exception("Error: ", err2.decode())

        out1 = out1.decode().strip()
        out2 = out2.decode().strip()

        _ps3 = await asyncio.create_subprocess_exec("xdo", "above", "-t", out1, out2,
                                                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        _, err3 = await _ps3.communicate()
        if _ps3.returncode != 0:
            raise Exception(err3.decode())

    async def __aenter__(self):
        await self.reload_bar()
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        self.ps.stdin.close()
        await self.ps.wait()
