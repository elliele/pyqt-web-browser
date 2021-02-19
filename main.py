import sys
import os
import json

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *




class AddressBar(QLineEdit):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, e):
        self.selectAll()


class App(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bamboo Browser")

        self.CreateApp()
        self.setMinimumSize(1366, 768)
        self.setWindowIcon(QIcon("logo.jpg"))

    def CreateApp(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create Tab
        self.tabbar = QTabBar(movable=True, tabsClosable=True)
        self.tabbar.tabCloseRequested.connect(self.CloseTab)
        self.tabbar.tabBarClicked.connect(self.SwitchTab)
        # set the current index of tab bar that tell the tabbar which tab is active
        self.tabbar.setCurrentIndex(0)  # initialize with active tab bar
        self.tabbar.setDrawBase(False)

        self.shortcutNewTab = QShortcut(QKeySequence("Ctrl+T"), self)
        self.shortcutNewTab.activated.connect(self.AddTab)

        self.shortcutReload = QShortcut(QKeySequence("Ctrl+R"), self)
        self.shortcutReload.activated.connect(self.ReloadPage)

        #Keep track of tabs and corresponding tab content
        self.tabCount = 0
        self.tabs =[] #contains every widget that belong to a tab; tab object


        # Create AddressBar
        self.Toolbar = QWidget()
        self.Toolbar.setObjectName("Toolbar")
        self.ToolbarLayout = QHBoxLayout()
        self.addressbar = AddressBar()
        self.AddTabButton = QPushButton("+")

        #Connect AddressBar + button Signals
        self.addressbar.returnPressed.connect(self.BrowseTo)
        self.AddTabButton.clicked.connect(self.AddTab)  # connect AddTabButton to method def AddTab(self):

        #Set Toolbar Buttons
        self.BackButton = QPushButton("<")
        self.BackButton.clicked.connect(self.GoBack)

        self.ForwardButton = QPushButton(">")
        self.ForwardButton.clicked.connect(self.GoForward)

        self.ReloadButton = QPushButton("R")
        self.ReloadButton.clicked.connect(self.ReloadPage)


        #Build toolbar
        self.Toolbar.setLayout(self.ToolbarLayout)
        self.ToolbarLayout.addWidget(self.BackButton)
        self.ToolbarLayout.addWidget(self.ForwardButton)
        self.ToolbarLayout.addWidget(self.ReloadButton)
        self.ToolbarLayout.addWidget(self.addressbar)
        self.ToolbarLayout.addWidget(self.AddTabButton)

        #set main view
        self.container = QWidget()
        self.container.layout = QStackedLayout()
        self.container.setLayout(self.container.layout) #tell QWidget() to use QStackedLayout()

        #stacked layout
        self.layout.addWidget(self.tabbar)
        self.layout.addWidget(self.Toolbar)
        self.layout.addWidget(self.container)


        self.setLayout(self.layout)

        #calling AddTab so there is always a tab active
        self.AddTab()

        self.show()

    def CloseTab(self, i):
        self.tabbar.removeTab(i)

    def AddTab(self):
        i = self.tabCount

        #Set self.tab<#> = QWidget
        self.tabs.append(QWidget()) #add stuff to self.tablist
        self.tabs[i].layout = QVBoxLayout() #modify the widget which access QWidget, can be treated as same QWidget b/c it's targeting QWidget
        self.tabs[i].layout.setContentsMargins(0, 0, 0, 0)




        #For tab switching
        self.tabs[i].setObjectName("tab" + str(i))

        #Create webview within the tabs top level widget
        self.tabs[i].content = QWebEngineView()
        self.tabs[i].content.load(QUrl.fromUserInput("http://google.com"))

        #self.tabs[i].content1 = QWebEngineView()
        #self.tabs[i].content1.load(QUrl.fromUserInput("http://google.com"))

        self.tabs[i].content.titleChanged.connect(lambda: self.SetTabContent(i, "title"))
        self.tabs[i].content.iconChanged.connect(lambda: self.SetTabContent(i,"icon"))
        self.tabs[i].content.urlChanged.connect(lambda: self.SetTabContent(i, "url"))

        #Add widget to tab .layout
        self.tabs[i].layout.addWidget(self.tabs[i].content)
        #self.tabs[i].splitview = QSplitter()
        #self.tabs[i].splitview.setOrientation(Qt.Vertical)
        #self.tabs[i].layout.addWidget(self.tabs[i].splitview)

        #self.tabs[i].splitview.addWidget(self.tabs[i].content)
        #self.tabs[i].splitview.addWidget(self.tabs[i].content1)

        #Set tabLayout to .layout
        self.tabs[i].setLayout(self.tabs[i].layout)

        #Add and set new tabs content to the stack widget
        self.container.layout.addWidget(self.tabs[i])
        self.container.layout.setCurrentWidget(self.tabs[i])

        #Create tab on tabbar, representing this tab,
        #Set tabData to tab<#> So it knows what self.tabs[#] it needs to control
        self.tabbar.addTab("New Tab")
        #tell tab what object name it should control
        self.tabbar.setTabData(i, {"object": "tab" + str(i), "initial": i})


        self.tabbar.setCurrentIndex(i)

        #increase tab count
        self.tabCount += 1

    def SetAddressBar(self, i):
        # Get the current tabs index, and set the address bar to its title.toString()
        tab = self.tabbar.tabData(i)["object"]
        if self.findChild(QWidget, tab).content == True:
            url = QUrl(self.findChild(QWidget, tab).content.url()).toString()
            self.AddressBar.setText(url)

    def SwitchTab(self, i):
        #Switch to tab, get currents tabs tabData ("tab0") and find object with that name
        if self.tabbar.tabData(i):
            tab = self.tabbar.tabData(i)["object"]
            self.container.layout.setCurrentWidget(self.findChild(QWidget, tab))
            self.SetAddressBar(i)
            print(self.tabs[i].content.nativeParentWidget())


    def BrowseTo(self):
        txt = self.addressbar.text()
        print(txt)

        #getting the index of current tab, set the tab to that index, and
        i = self.tabbar.currentIndex()
        tab = self.tabbar.tabData(i)["object"]
        web_view = self.findChild(QWidget, tab).content


        if "http" not in txt:
            if "." not in txt:
                url = "https://www.google.com/search?q=" + txt
            else:
                url = "http://" + txt
        else:
            url = txt

        web_view.load(QUrl.fromUserInput(url))

    def SetTabContent(self, i, type):
        '''
            self.tabs[i].objectName = tab1
            self.tabbar.tabData(i)["object"] = tab1
        '''
        tab_name  = self.tabs[i].objectName()
        #tab1

        count = 0
        running = True
        '''
        #create a SetAddressBar method
        current_tab = self.tabbar.tabData(self.tabbar.currentIndex())["object"]

        if current_tab == tab_name and type == "url":
            new_url = self.findChild(QWidget, tab_name).content.url().toString()
            self.addressbar.setText(new_url)
            return False
        '''


        while running:
            tab_data_name = self.tabbar.tabData(count)

            if count >= 99:
                running = False

            if tab_name  == tab_data_name["object"]:
                if type == "title":
                    newTitle = self.findChild(QWidget, tab_name).content.title()
                    self.tabbar.setTabText(count,newTitle)
                elif type == "icon":
                    newIcon = self.findChild(QWidget, tab_name).content.icon()
                    self.tabbar.setTabIcon(count, newIcon)
                running = False
            else:
                count += 1


    def GoBack(self):
        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.findChild(QWidget, tab_name).content

        tab_content.back()

    def GoForward(self):
        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.findChild(QWidget, tab_name).content

        tab_content.forward()

    def ReloadPage(self):
        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.findChild(QWidget, tab_name).content

        tab_content.reload()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = "667"

    window = App()

    with open("style.css", "r") as style:
        app.setStyleSheet(style.read())

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")



