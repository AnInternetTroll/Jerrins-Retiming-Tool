# Jerrin Shirks
import webbrowser

# native imports
from PyQt5.QtWidgets import QStyleFactory
import platform

# custom imports
from support import *
import subprocess
import os



class Settings:
    def __init__(self, version="1.0.0"):
        self.os_index = 0
        self.documentFolder: str = ""
        self.templateFolder: str = ""
        self.iconFolder: str = ""
        self.prepareOS()

        self.filename_settings = self.documentFolder + "settings.json"
        self.filename_pages = self.documentFolder + "pages.json"
        self.data: dict = read_json(self.filename_settings)

        self.version = version
        self.latest_ver = version

        self.iconDir: str = self.data.get("icon-dir", "../../../icons/")
        self.latestVersionLink: str = "https://jerrin.org/downloads/retimer/latest.json"

        self.url_links = {
            "website": 'https://jerrin.org',
            "modhub": 'https://www.speedrun.com/modhub',
            "github": 'https://github.com/zugebot/Speedrun-Retimer',
            "mod-message-formatting": "https://github.com/zugebot/Speedrun-Retimer/blob/main/MOD_FORMAT.md"
        }

        self.default = {
            "fps": 30,
            "include-sub-loads": False,
            "include-paste-buttons": True,
            "show-hints": True,
            "decimal-accuracy": 3,
            "mod-message": "Mod Note: Retimed to {TT}.",
            "window-style": 0,
            "text-color": 0,
            "text-color-negative": "red",
            "background-color": "dark-grey"
        }

        self.windowStyleList = QStyleFactory.keys()
        print(self.windowStyleList)
        if "Fusion" in self.windowStyleList:
            index = self.windowStyleList.index("Fusion")
            self.default["window-style"] = index
            self.data["window-style"] = index

        self.textColorList = ["Green", "Cyan"]
        self.textColorValues = [[78, 228, 78], "cyan"]


    def get(self, key):
        return self.data.get(key, self.default.get(key, None))


    def getDict(self):
        data = dict()
        for key in self.default:
            data[key] = self.get(key)
        return data


    def set(self, key, value):
        self.data[key] = value


    def prepareOS(self):
        os_name = platform.system()
        # find which os
        OS_NAMES = ["Windows", "Linux", "Darwin"]
        if os_name in OS_NAMES:
            self.os_index = OS_NAMES.index(os_name)
        else:
            self.os_index = 3
        # finds the documents folder
        self.documentFolder = {
            0: "C:\\Users\\{}\\Documents\\Speedrun-Retimer\\",
            1: "/home/{}/Documents/Speedrun-Retimer/",
            2: "/Users/{}/Documents/Speedrun-Retimer/",
            3: ""
        }[self.os_index].format(os.getlogin())
        # create the directories
        self.templateFolder = self.dirJoiner(self.documentFolder, "rowTemplates", "")
        self.iconFolder = self.dirJoiner(self.documentFolder, "srcIcons", "")
        os.makedirs(os.path.dirname(self.documentFolder), exist_ok=True)
        os.makedirs(os.path.dirname(self.templateFolder), exist_ok=True)
        os.makedirs(os.path.dirname(self.iconFolder), exist_ok=True)


    def dirJoiner(self, *args) -> str:
        segment = ["\\", "/", "/", "/"][self.os_index]
        return segment.join(list(args))


    def save(self):
        write_json(self.data, self.filename_settings)


    def getWindowStyle(self):
        return self.windowStyleList[self.get("window-style")]


    def openFileDialog(self, filename):
        if self.os_index == 0:  # windows
            subprocess.Popen(r'explorer /select,"{}"'.format(filename))
        elif self.os_index == 1:  # linux
            subprocess.Popen(["xdg-open", "--select", filename])
        elif self.os_index == 2:  # Mac
            subprocess.Popen(["open", "-R", filename])
        else:
            print("Unsupported OS")


    def _toQColor(self, color):
        if isinstance(color, str):
            color = QColor(color)
        else:
            color = QColor(color[0], color[1], color[2])
        return color

    def getTextQColor(self):
        return self._toQColor(self.textColorValues[self.get("text-color")])


    def getNegTextQColor(self):
        return self._toQColor(self.get("text-color-negative"))

    def getBkgQColor(self):
        return self._toQColor("background-color")


    def openLink(self, link):
        webbrowser.open(link)
