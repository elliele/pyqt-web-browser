# Bamboo Browser

### PyQt5 Web Browser Design

PyQt5 is a comprehensive set of Python bindings for Qt v5. It is implemented as more than 35 extension modules and enables Python to be used as an alternative application development language to C++ on all supported platforms including iOS and Android.

```
pip install PyQt5
```


### QWebEngine implementation

```
self.tabs[i].content = QWebEngineView()
self.tabs[i].content.load(QUrl.fromUserInput("http://google.com"))
        
```
<img width="682" alt="day29p2" src="https://user-images.githubusercontent.com/69995236/108559606-60df7580-72b0-11eb-934b-a47c42146692.PNG">

### Set up the web address bar

```
    def SetAddressBar(self, i):
        # Get the current tabs index, and set the address bar to its title.toString()
        tab = self.tabbar.tabData(i)["object"]
        if self.findChild(QWidget, tab).content == True:
            url = QUrl(self.findChild(QWidget, tab).content.url()).toString()
            self.AddressBar.setText(url)
```
### Enable switch tabs

```
    def SwitchTab(self, i):
        #Switch to tab, get currents tabs tabData ("tab0") and find object with that name
        if self.tabbar.tabData(i):
            tab = self.tabbar.tabData(i)["object"]
            self.container.layout.setCurrentWidget(self.findChild(QWidget, tab))
            self.SetAddressBar(i)
            print(self.tabs[i].content.nativeParentWidget())
```

<img width="681" alt="day30p2" src="https://user-images.githubusercontent.com/69995236/108560199-3cd06400-72b1-11eb-8e59-4a006bbc80fb.PNG">

### Implementing QtSplitter

```
def AddTab(self):
        ...
        
        self.tabs[i].content = QWebEngineView()
        self.tabs[i].content.load(QUrl.fromUserInput("http://google.com"))

        self.tabs[i].content1 = QWebEngineView()
        self.tabs[i].content1.load(QUrl.fromUserInput("http://google.com"))
        ...
        
        self.tabs[i].splitview = QSplitter()
        self.tabs[i].splitview.setOrientation(Qt.Vertical)
        self.tabs[i].layout.addWidget(self.tabs[i].splitview)

        self.tabs[i].splitview.addWidget(self.tabs[i].content)
        self.tabs[i].splitview.addWidget(self.tabs[i].content1)
```


<img width="685" alt="day30p1" src="https://user-images.githubusercontent.com/69995236/108560617-e0217900-72b1-11eb-92ca-721abbdfb44c.PNG">



