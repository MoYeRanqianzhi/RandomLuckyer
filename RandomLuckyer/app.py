from tkinter.ttk import Button, Label, Style
from tkinter import Tk, StringVar, Frame, Menu
from tkinter.messagebox import showwarning, showinfo
from random import randint
import os
import const
import json
# import sys
import webbrowser


LICENSE = '''MIT License

Copyright (c) 2023 MoYeRanQianZhi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''


class ConfigureWindowArea:
    def __call__(self, data):
        if data is not None:
            self.font = data.get('font')
            self.fontSize = data.get('fontSize')
            return self
        else:
            return None


class ConfigureWindow:
    def __call__(self, data):
        if data is not None:
            self.alpha = data.get('alpha')
            self.topmost = data.get('topmost')
            self.infoArea = ConfigureWindowArea()(data.get('infoArea'))
            self.luckyerArea = ConfigureWindowArea()(data.get('luckyerArea'))
            self.buttonArea = ConfigureWindowArea()(data.get('buttonArea'))
            return self
        else:
            return None


class Configure:
    def __init__(self, data):
        self.students = data.get('students')
        self.window = ConfigureWindow()(data.get('window'))


class RandomLuckyer(Frame):
    def __init__(self, master, **kw):
        Frame.__init__(self, master, kw)

        self.style = Style()

        self.menu = Menu(self._root())
        self.setMenu()

        self.students = list(range(1, 51))
        self.survivors = self.students.copy()

        self.luckyer = StringVar(value='0')
        self.info = StringVar(value=f'剩余同学:{len(self.survivors)}')

        self.alpha = 0.8
        self.topmost = True
        self.infoFont = '微软雅黑'
        self.luckyerFont = '微软雅黑'
        self.buttonFont = '微软雅黑'
        self.infoFontSize = 12
        self.luckyerFontSize = 100
        self.buttonFontSize = 15

        self.initialize()
        self.binds()

    def initialize(self):
        if os.path.exists(const.configureFile):
            with open(const.configureFile, mode='r', encoding='utf-8') as f:
                configure = Configure(json.loads(f.read()))

            if configure.students is not None:
                self.students = configure.students
                self.survivors = self.students.copy()
                self.info.set(f'剩余同学:{len(self.survivors)}')

            if configure.window is not None:
                if configure.window.alpha is not None:
                    self.alpha = configure.window.alpha
                if configure.window.topmost is not None:
                    self.topmost = configure.window.topmost
                if configure.window.infoArea is not None:
                    if configure.window.infoArea.font is not None:
                        self.infoFont = configure.window.infoArea.font
                    if configure.window.infoArea.fontSize is not None:
                        self.infoFontSize = configure.window.infoArea.fontSize
                    if configure.window.luckyerArea.font is not None:
                        self.luckyerFont = configure.window.luckyerArea.font
                    if configure.window.luckyerArea.fontSize is not None:
                        self.luckyerFontSize = configure.window.luckyerArea.fontSize
                    if configure.window.buttonArea.font is not None:
                        self.buttonFont = configure.window.buttonArea.font
                    if configure.window.buttonArea.fontSize is not None:
                        self.buttonFontSize = configure.window.buttonArea.fontSize

        Label(
            master=self,
            textvariable=self.info,
            font=(self.infoFont, self.infoFontSize),
            background='white'
        ).pack()

        Label(
            master=self,
            textvariable=self.luckyer,
            font=(self.luckyerFont, self.luckyerFontSize),
            background='white'
        ).pack()

        Button(
            master=self,
            text='抽取同学',
            command=self.choose,
        ).pack(padx=10, pady=10)

        self.style.configure(
            'TButton',
            font=(self.buttonFont, self.buttonFontSize),
            background='white'
        )

        self.configure(background='white')

        self._root().attributes('-alpha', self.alpha)
        self._root().attributes('-topmost', self.topmost)

    def choose(self):
        self.luckyer.set(
            self.survivors.pop(
                randint(0, len(self.survivors) - 1)
            )
        )

        if len(self.survivors) == 0:
            self.survivors = self.students.copy()

        self.info.set(f'剩余同学:{len(self.survivors)}')

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    def setMenu(self):
        FileMenu = Menu(self.menu, background='white', tearoff=False)
        EditMenu = Menu(self.menu, background='white', tearoff=False)
        SetMenu = Menu(self.menu, background='white', tearoff=False)
        HelpMenu = Menu(self.menu, background='white', tearoff=False)

        FileMenu.add_command(
            label='下载默认配置',
            command=lambda: open(
                const.configureFile,
                mode='w',
                encoding='utf-8'
            ).write(
                json.dumps(
                    const.defaultConfigureContent,
                    indent=4,
                    ensure_ascii=False
                )
            )
        )
        FileMenu.add_command(
            label='打开配置文件',
            command=self.openConfigureFile
        )

        EditMenu.add_command(
            label='重加载',
            command=lambda: (
                self.clear(),
                self.initialize()
            )
        )

        HelpMenu.add_command(
            label='配置教程',
            command=lambda: webbrowser.open('https://luckyer.pages.dev/')
        )
        HelpMenu.add_command(
            label='开源代码',
            command=lambda: webbrowser.open('https://github.com/MoYeRanqianzhi/RandomLuckyer')
        )
        HelpMenu.add_command(
            label='开源协议',
            command=lambda: webbrowser.open('https://moyeranqianzhi.mit-license.org/')
        )
        HelpMenu.add_command(
            label='开源协议离线版',
            command=lambda: showinfo(
                '开源协议',
                LICENSE
            )
        )
        HelpMenu.add_command(
            label='联系墨叶染千枝',
            command=lambda: webbrowser.open('mailto:MoYeRanQianZhi@gmail.com')
        )
        HelpMenu.add_command(
            label='联络信息',
            command=lambda: showinfo(
                '联络信息',
                'QQ:3228993382\n'
                'WeChat:MoYeRanQianZhi\n'
                'email:MoYeRanQianZhi@gmail.com(首选),\n'
                '    MoYeRanQianZhi@outlook.com,\n'
                '    MoYeRanSoft@gmail.com,\n'
                '    MoYeRanSoft@outlook.com\n'
                'Telegram:@moyeranqianzhi\n'
                'X(原Twitter):@MoYeRanQianZhi\n'
                'GitHub:https://github.com/MoYeRanQianZhi'
            )
        )
        HelpMenu.add_command(
            label='软件信息',
            command=lambda: showinfo(
                '软件信息',
                'APP:随机抽取一个幸运同学\n'
                'Package:com.m.luckyer\n'
                '版本:Luckyer大乘期至臻版0.1.0\n'
                '开源协议:MIT\n'
                '作者:墨叶染千枝\n'
                '产品经理:墨叶染千枝\n'
                '首席技术官:墨叶染千枝\n'
                '首席设计师:墨叶染千枝\n'
                '首席测试官:墨叶染千枝'
            )
        )

        self.menu.add_cascade(
            label='文件',
            menu=FileMenu
        )
        self.menu.add_cascade(
            label='编辑',
            menu=EditMenu
        )
        self.menu.add_cascade(
            label='设置',
            menu=SetMenu
        )
        self.menu.add_cascade(
            label='帮助',
            menu=HelpMenu
        )

        self._root().configure(
            menu=self.menu
        )

    def binds(self):
        self._root().bind(
            sequence='<Control-e>',
            func=lambda event: self._root().destroy()
        )
        self._root().bind(
            sequence='<Control-n>',
            func=lambda event: self.choose()
        )

    def configureWindow(self):
        pass

    @staticmethod
    def openConfigureFile():
        if os.path.exists(const.configureFile):
            os.startfile(const.configureFile)
        else:
            showwarning(
                '错误',
                '当前运行环境下没有配置文件'
            )

    @staticmethod
    def saveConfigureFile(data):
        with open(const.configureFile, mode='w', encoding='utf-8') as f:
            f.write(
                json.dumps(
                    data,
                    indent=4,
                    ensure_ascii=False
                )
            )


if __name__ == '__main__':
    root = Tk()
    root.geometry('300x300-50+50')
    root.title('随机抽取一个幸运同学')
    # root.iconbitmap(sys.executable)
    root.configure(background='white')
    app = RandomLuckyer(root)
    app.pack()
    root.mainloop()
