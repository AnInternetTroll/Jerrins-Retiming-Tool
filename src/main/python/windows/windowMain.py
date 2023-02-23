# Jerrin Shirks

# native imports
from PyQt5.QtCore import Qt
import webbrowser
from functools import partial

# custom imports
from src.main.python.support import *
from src.main.python.windows.windowRetimer import WindowRetimer
from src.main.python.windows.windowSettings import WindowSettings
from src.main.python.windows.windowAddPage import WindowAddPage
from src.main.python.windows.windowAddTemplate import WindowAddTemplate
from src.main.python.windows.windowRetimerTiny import WindowRetimerTiny



class WindowMain(QMainWindow):
    def __init__(self, app, settings, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.openRowTemplateAction = None
        self.app: QApplication = app
        self.settings = settings
        self.palette: QPalette = QPalette()
        self.applyPalette()

        # self.setWindowOpacity(1)

        self.latestUrl: str = ""

        self.windowRetimer: WindowRetimer = WindowRetimer(self)
        self.windowAddTemplate: WindowAddTemplate = None
        self.windowSettings: WindowSettings = None
        self.windowAddPage: WindowAddPage = None
        self.windowRetimerTiny: WindowRetimerTiny = None


        self.initUI()

        self.menuBar: QMenuBar = self.menuBar()
        self.initMenuBar()

        # startup funcs
        self.findLatestVersion()
        self.windowRetimer.loadSaveFile()


    def initUI(self):
        self.setTitle()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setMaximumSize(450, 363)
        self.setCentralWidget(self.windowRetimer.widget)


    def applyPalette(self):
        grey1 = self.settings.getQColor("grey1")
        grey3 = self.settings.getQColor("grey3")
        self.palette.setColor(QPalette.Window, grey1)
        self.palette.setColor(QPalette.AlternateBase, grey1)
        self.palette.setColor(QPalette.Button, grey1)
        self.palette.setColor(QPalette.Base, grey3)
        self.palette.setColor(QPalette.HighlightedText, Qt.black)
        self.palette.setColor(QPalette.ToolTipBase, Qt.black)
        self.palette.setColor(QPalette.WindowText, Qt.white)
        self.palette.setColor(QPalette.ToolTipText, Qt.white)
        self.palette.setColor(QPalette.Text, Qt.white)
        self.palette.setColor(QPalette.ButtonText, Qt.white)

        text = self.settings.getTextQColor()
        highlight = self.settings.getHighlightQColor()

        self.palette.setColor(QPalette.BrightText, text)
        self.palette.setColor(QPalette.Link, text)
        self.palette.setColor(QPalette.Highlight, highlight)

        self.app.setPalette(self.palette)
        self.app.setStyle(self.settings.getWindowStyle())





    def iconify(self, filename):
        return self.settings.iconDir + filename


    def openWindowAddPage(self):
        self.windowAddPage = WindowAddPage(self)
        self.windowAddPage.setWindowModality(Qt.ApplicationModal)
        self.windowAddPage.show()


    def openWindowAddTemplate(self):
        self.windowAddTemplate = WindowAddTemplate(self)
        self.windowAddTemplate.setWindowModality(Qt.ApplicationModal)
        self.windowAddTemplate.show()


    def openWindowSettings(self):
        self.windowSettings = WindowSettings(self)
        self.windowSettings.setGeometry(*placeOnSide(self, 350, 400, "left"))
        self.windowSettings.setWindowModality(Qt.ApplicationModal)
        self.windowSettings.show()


    def openWindowRetimerTiny(self):
        self.windowRetimerTiny = WindowRetimerTiny(self)
        self.hide()
        self.windowRetimerTiny.show()




    def updateSettings(self):
        self.windowRetimer.updateSettings()
        self.app.setStyle(self.settings.getWindowStyle())




    def closeEvent(self, event):
        self.windowRetimer.saveFile()
        self.settings.save()
        if self.windowSettings is not None:
            self.windowSettings.close()
        event.accept()


    def setTitle(self, *args):
        title = "Jerrin's Retiming Tool"
        for arg in args:
            if arg is None:
                continue
            title += f" [{arg}]"
        self.setWindowTitle(title)


    def findLatestVersion(self):
        try:
            latest = requests.get(self.settings.latestVersionLink).text.split("\n")
            self.settings.latestDownloadUrl = f"{self.settings.latestVersionLink}{latest[1]}".replace(" ", "%20")
            print(self.settings.version, latest[0])
            if self.settings.version < latest[0]:
                update_bar = self.menuBar.addMenu("Update")
                addNewAction(update_bar, f"Download {self.settings.latest_ver}!", self.downloadUpdate)
        except Exception as e:
            print(e)
            "do nothing lol, no internet"


    def addWebsitePage(self):
        pass


    def downloadUpdate(self):
        webbrowser.open(self.latestUrl)


    def showCredits(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Credits")
        msg.setText("UI + Coding   : jerrinth3glitch#6280      \n"
                    "Icon Design    : Alexis.#3047\n"
                    "Early Support : Aiivan#8227")
        msg.setInformativeText(rf"<b>Version {self.settings.version}<\b>")
        msg.setDetailedText(
                            "1. Added Settings!"
                            "\n  - Toggles for theme style and color"
                            "\n  - Settings on startup actually work"
                            "\n2. Added Custom Mod Messages!"
                            "\n3. Added Templates!"
                            "\n  - Templates allow for saving and "
                            "\n    loading row presets."
                            )
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


    def viewTemplateFolder(self):
        self.settings.openFileDialog(self.settings.templateFolder)


    def initMenuBar(self):
        self.menuBar.setStyleSheet("QMenu::separator { background-color: red; }")
        self.menuBar.setFocusPolicy(Qt.StrongFocus)


        fileMenu: QMenu = self.menuBar.addMenu("File")

        addNewIconAction(self, fileMenu, self.iconify("document.png"), "&Open Folder", self.windowRetimer.viewDocumentFolder, "Ctrl+O")
        addNewIconAction(self, fileMenu, None, "Single Row Mode", self.openWindowRetimerTiny, "Ctrl+F")
        addNewIconAction(self, fileMenu, self.iconify("gear2.png"), "Settings", self.openWindowSettings, "Ctrl+A")


        editMenu: QMenu = self.menuBar.addMenu("Edit")

        addNewIconAction(self, editMenu, self.iconify("copy.png"), "Copy Rows as Text", self.windowRetimer.copyRowsAsText, "Ctrl+D")
        addNewIconAction(self, editMenu, self.iconify("trash.png"), "Clear Rows", self.windowRetimer.resetSplits, "Ctrl+Z")
        addNewIconAction(self, editMenu, self.iconify("skull.png"), "Clear Times", self.windowRetimer.resetTimes, "Ctrl+X")

        # gif = self.settings.iconDir + "spinning.gif"
        # self.actionClearRows = AnimatedIconAction(gif, "Clear Times")
        # self.actionClearRows.addToMenu(editMenu, self.windowRetimer.resetTimes, "Ctrl+X")


        templateMenu: QMenu = self.menuBar.addMenu("Templates")
        # addNewIconAction(self, templateMenu, self.iconify("document"), "View &Template Folder", self.viewTemplateFolder, "Ctrl+T")

        self.openRowTemplateAction: QAction = addNewIconAction(self, templateMenu, self.iconify("document"), "&Open Template", None)
        if len(self.getTemplates()) == 0:
            self.openRowTemplateAction.setVisible(False)

        addNewIconAction(self, templateMenu, self.iconify("plus.png"), "&New Template", self.openWindowAddTemplate, "Ctrl+N")
        self.populateTemplates()


        websiteMenu: QMenu = self.menuBar.addMenu("Websites")
        addNewIconAction(self, websiteMenu, self.iconify("trophy2.png"), "Moderation Hub", partial(self.settings.openLink, "modhub"), "Ctrl+Q")
        addNewIconAction(self, websiteMenu, self.iconify("globe2.png"), "Edit Pages [TBD]", self.openWindowAddPage, "Ctrl+E")


        aboutMenu: QMenu = self.menuBar.addMenu("About")
        addNewIconAction(self, aboutMenu, self.iconify("github2.png"), "Github Page", partial(self.settings.openLink, "github"))
        addNewAction(aboutMenu, "How to Use [WIP]", partial(self.settings.openLink, "website"))
        addNewAction(aboutMenu, "Credits", self.showCredits)



    def getTemplates(self):
        files = os.listdir(self.settings.templateFolder)
        templates = []
        for file in files:
            filename = self.settings.dirJoiner(self.settings.templateFolder, file)
            if not os.path.isfile(filename):
                continue
            if not file.endswith(".rt"):
                continue
            templates.append(file)
        return templates


    def populateTemplates(self):
        templates = self.getTemplates()

        menu = QMenu()
        for template in templates:
            filename = self.settings.dirJoiner(self.settings.templateFolder, template)
            data = read_json(filename)
            name = data.get("display-name", "N/A")
            addNewAction(menu, name, partial(self.windowRetimer.loadTemplate, filename))
        self.openRowTemplateAction.setMenu(menu)