## pyqt笔记第一篇 ##
原文地址：[Hello World · PyQt5 中文教程](https://maicss.gitbooks.io/pyqt5/content/hello_world.html)

<b>安装过程</b>：
```
pip install SIP
pip install PyQt5
pip install wheel
```
下载QTCreator：[Index of /official_releases/qtcreator](http://download.qt.io/official_releases/qtcreator/)
下载Pyqt5：[PyQt - Browse /PyQt5 at SourceForge.net](https://sourceforge.net/projects/pyqt/files/PyQt5/)

<b>pycharm配置ui转py的第三方工具</b>
![kVqI2T.png](https://s2.ax1x.com/2019/01/24/kVqI2T.png)

```
Name填：工具名称
Description填：工具说明
Program填：python路径
Arguments:填：-m PyQt5.uic.pyuic $FileName$ -o $FileNameWithoutExtension$.py
Working directory填：存放UI的目录
```
![kVL9MD.png](https://s2.ax1x.com/2019/01/24/kVL9MD.png)

<b>ui转py</b>
![kVLgSK.md.png](https://s2.ax1x.com/2019/01/24/kVLgSK.md.png)
配置好后右键pyuic即可转换

![kVL5TA.md.png](https://s2.ax1x.com/2019/01/24/kVL5TA.md.png)

<b>窗口设置</b>
```
import sys
from PyQt5.QtWidgets import QWidget,QApplication

class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.intui()

    def intui(self):
        self.resize(350,250) #设置宽度和高度
        self.move(300,500) #设置屏幕出现的位置
        self.setWindowTitle("我应该去死") #设置标题
        self.show() #显示窗体

if __name__ == '__main__':
    app=QApplication(sys.argv)
    obj=Demo()
    sys.exit(app.exec_())
```
![](https://s2.ax1x.com/2019/01/24/kVOUht.png)


使用setGemoetry()函数来代替resize()和move的，是resize和move的集合体
```
import sys
from PyQt5.QtWidgets import QWidget,QApplication

class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.intui()

    def intui(self):
        self.setGeometry(300,300,300,300)
        self.setWindowTitle("我应该去死")
        self.show()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    obj=Demo()
    sys.exit(app.exec_())
```
![](https://s2.ax1x.com/2019/01/24/kZPPUO.png)

<b>提示框和按钮</b>
```
import sys
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QToolTip
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication
class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.intui()

    def intui(self):
        QToolTip.setFont(QFont('SansSerif',10)) #设置字体和大小
        btn=QPushButton("提交",self) #设置按钮名称和出现在那个窗口
        btn.resize(btn.sizeHint()) #设置窗口大小，btn.sizeHint()为默认大小
        btn.setToolTip("你是想<b>拔刀</b>吗？") #按钮提示框
        btn.move(102,102) #按钮出现的位置
        self.setGeometry(300,300,300,300) #设置窗体出现的位置和高度宽度
        self.setWindowTitle("源氏")
        self.show() #窗体出现
        self.setToolTip("有何贵干老铁？") #窗体提示框

if __name__ == '__main__':
    app=QApplication(sys.argv)
    obj=Demo()
    sys.exit(app.exec_())
```
注意：按钮不能放在show()下面，因为窗体出现后就不会在加载任何东西了
![kZPsz9.png](https://s2.ax1x.com/2019/01/24/kZPsz9.png)

![kZPgqx.png](https://s2.ax1x.com/2019/01/24/kZPgqx.png)

<b>按钮事件</b>
也就是说在点击按钮后会执行对应的事件
```
import sys
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QToolTip
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication
class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.intui()

    def intui(self):
        QToolTip.setFont(QFont('SansSerif',10))
        btn=QPushButton("提交",self)
        btn.clicked.connect(QCoreApplication.instance().quit) #点击按钮后会退出，QCoreApplication.instance().quit是退出所有程序的事件
        btn.resize(btn.sizeHint())
        btn.setToolTip("你是想<b>拔刀</b>吗？")
        btn.move(102,102)
        self.setGeometry(300,300,300,300)
        self.setWindowTitle("源氏")
        self.show()
        self.setToolTip("有何贵干老铁？")

if __name__ == '__main__':
    app=QApplication(sys.argv)
    obj=Demo()
    sys.exit(app.exec_())
```
![](https://s2.ax1x.com/2019/01/24/kZijn1.png)

<b>关闭窗口</b>
```
import sys
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QToolTip,QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication
class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.intui()

    def intui(self):
        QToolTip.setFont(QFont('SansSerif',10))
        btn=QPushButton("提交",self)
        btn.clicked.connect(QCoreApplication.instance().quit)
        btn.resize(btn.sizeHint())
        btn.setToolTip("你是想<b>拔刀</b>吗？")
        btn.move(102,102)
        self.setGeometry(300,300,300,300)
        self.setWindowTitle("源氏")
        self.show()
        self.setToolTip("有何贵干老铁？")

    def closeEvent(self, event): #重新定义了closeEvent(),改变控件的默认行为，就是替换掉默认的事件处理。
        reply=QMessageBox.question(self,'退出','你真的要退出吗？',QMessageBox.Yes| QMessageBox.No,QMessageBox.No) #退出选择，第一个是退出框的标题，第二个退出框的说明，第三个是按钮，第四个也是按钮，第五个是默认按钮
        if reply==QMessageBox.Yes: #如果选择YES就退出
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    obj=Demo()
    sys.exit(app.exec_())
```
![](https://s2.ax1x.com/2019/01/24/kZkPaV.png)

<b>居中对齐</b>

```
import sys
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QToolTip,QMessageBox,QDesktopWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication
class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.intui()

    def intui(self):
        QToolTip.setFont(QFont('SansSerif',10))
        btn=QPushButton("提交",self)
        btn.clicked.connect(QCoreApplication.instance().quit)
        btn.resize(btn.sizeHint())
        btn.setToolTip("你是想<b>拔刀</b>吗？")
        qr = self.frameGeometry() #获取桌面分辨率
        cp = QDesktopWidget().availableGeometry().center() #获取中心位置
        qr.moveCenter(cp) #获取窗口中心位置
        self.resize(300,250)
        self.move(qr.topLeft()) #移动到中心
        self.setWindowTitle("源氏")
        self.show()
        self.setToolTip("有何贵干老铁？")

    def closeEvent(self, event):
        reply=QMessageBox.question(self,'退出','你真的要退出吗？',QMessageBox.Yes| QMessageBox.No,QMessageBox.No)
        if reply==QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    obj=Demo()
    sys.exit(app.exec_())
```
![](https://s2.ax1x.com/2019/01/24/kZkLe1.md.png)

<b>给窗体设置logo</b>
这里我就用这张图
![20170710120441_39.jpg](http://img.inmywordz.com/uploads/20170710120441_39.jpg)

```
import sys
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QToolTip,QMessageBox,QDesktopWidget
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtCore import QCoreApplication
class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.intui()

    def intui(self):
        self.setWindowIcon(QIcon('1.jpg'))  # w.setWindowIcon(QIcon('图片名称')) #设置logo
        QToolTip.setFont(QFont('SansSerif',10))
        btn=QPushButton("提交",self)
        btn.clicked.connect(QCoreApplication.instance().quit)
        btn.resize(btn.sizeHint())
        btn.setToolTip("你是想<b>拔刀</b>吗？")
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.resize(300,250)
        self.move(qr.topLeft())
        self.setWindowTitle("源氏")
        self.show()
        self.setToolTip("有何贵干老铁？")

    def closeEvent(self, event):
        reply=QMessageBox.question(self,'退出','你真的要退出吗？',QMessageBox.Yes| QMessageBox.No,QMessageBox.No)
        if reply==QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    obj=Demo()
    sys.exit(app.exec_())
```
![](https://s2.ax1x.com/2019/01/24/kZEkjJ.png)