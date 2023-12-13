import json
import os
# import sys
import webbrowser
from random import randint, choice, choices
from tkinter import Tk, StringVar, IntVar, Frame, Menu, PhotoImage
from tkinter.messagebox import showwarning, showinfo
from tkinter.ttk import Button, Label, Style

from sympy import divisors

import const

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


class ConfigureWindowAreaColor:
    def __call__(self, data):
        if data is not None:
            self.background = data.get('background')
            self.foreground = data.get('foreground')
            return self
        else:
            return None


class ConfigureWindowArea:
    def __call__(self, data):
        if data is not None:
            self.font = data.get('font')
            self.fontSize = data.get('fontSize')
            self.color = ConfigureWindowAreaColor()(data.get('color'))
            return self
        else:
            return None


class ConfigureWindowColor:
    def __call__(self, data):
        if data is not None:
            self.background = data.get('background')
            return self
        else:
            return None


class ConfigureWindow:
    def __call__(self, data):
        if data is not None:
            self.alpha = data.get('alpha')
            self.topmost = data.get('topmost')
            self.size = data.get('size')
            self.color = ConfigureWindowColor()(data.get('color'))
            self.infoArea = ConfigureWindowArea()(data.get('infoArea'))
            self.luckyerArea = ConfigureWindowArea()(data.get('luckyerArea'))
            self.buttonArea = ConfigureWindowArea()(data.get('buttonArea'))
            return self
        else:
            return None


class ConfigureSettings:
    def __call__(self, data):
        if data is not None:
            self.tempSave = data.get('tempSave')
            self.autoSave = data.get('autoSave')
            return self
        else:
            return None


class Configure:
    def __init__(self, data):
        self.students = data.get('students')
        self.survivors = data.get('survivors')
        self.window = ConfigureWindow()(data.get('window'))
        self.settings = ConfigureSettings()(data.get('settings'))


class RandomLuckyer(Frame):
    def __init__(self, master, **kw):
        Frame.__init__(self, master, kw)

        self.style = Style()

        self.menu = None

        self.students = list(range(1, 51))
        self.survivors = self.students.copy()

        self.luckyer = StringVar(value='0')
        self.info = StringVar(value=f'剩余同学:{len(self.survivors)}')

        self.alpha = 0.8
        self.topmost = True
        self.windowSize = '300x300-50+50'
        self.windowBackgroundColor = 'white'
        self.infoFont = '微软雅黑'
        self.luckyerFont = '微软雅黑'
        self.buttonFont = '微软雅黑'
        self.infoFontSize = 12
        self.luckyerFontSize = 100
        self.buttonFontSize = 15
        self.infoBackgroundColor = 'white'
        self.luckyerBackgroundColor = 'white'
        self.buttonBackgroundColor = 'white'
        self.infoForegroundColor = 'black'
        self.luckyerForegroundColor = 'black'
        self.buttonForegroundColor = 'black'

        self.tempSave = False
        self.autoSave = False
        self.tempSaveMode = IntVar(value=0)
        self.autoSaveMode = IntVar(value=0)

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

            if configure.survivors is not None:
                self.survivors = [s for s in configure.survivors if s in self.students]
                self.info.set(f'剩余同学:{len(self.survivors)}')

            if configure.window is not None:
                if configure.window.alpha is not None:
                    self.alpha = configure.window.alpha
                if configure.window.topmost is not None:
                    self.topmost = configure.window.topmost
                if configure.window.size is not None:
                    self.windowSize = configure.window.size
                    self._root().geometry(self.windowSize)
                if configure.window.color is not None:
                    if configure.window.color.background is not None:
                        self.windowBackgroundColor = configure.window.color.background
                        self._root().configure(background=self.windowBackgroundColor)
                if configure.window.infoArea is not None:
                    if configure.window.infoArea.font is not None:
                        self.infoFont = configure.window.infoArea.font
                    if configure.window.infoArea.fontSize is not None:
                        self.infoFontSize = configure.window.infoArea.fontSize
                    if configure.window.infoArea.color is not None:
                        if configure.window.infoArea.color.background is not None:
                            self.infoBackgroundColor = configure.window.infoArea.color.background
                        if configure.window.infoArea.color.foreground is not None:
                            self.infoForegroundColor = configure.window.infoArea.color.foreground
                if configure.window.luckyerArea is not None:
                    if configure.window.luckyerArea.font is not None:
                        self.luckyerFont = configure.window.luckyerArea.font
                    if configure.window.luckyerArea.fontSize is not None:
                        self.luckyerFontSize = configure.window.luckyerArea.fontSize
                    if configure.window.luckyerArea.color is not None:
                        if configure.window.luckyerArea.color.background is not None:
                            self.luckyerBackgroundColor = configure.window.luckyerArea.color.background
                        if configure.window.luckyerArea.color.foreground is not None:
                            self.luckyerForegroundColor = configure.window.luckyerArea.color.foreground
                if configure.window.buttonArea is not None:
                    if configure.window.buttonArea.font is not None:
                        self.buttonFont = configure.window.buttonArea.font
                    if configure.window.buttonArea.fontSize is not None:
                        self.buttonFontSize = configure.window.buttonArea.fontSize
                    if configure.window.buttonArea.color is not None:
                        if configure.window.buttonArea.color.background is not None:
                            self.buttonBackgroundColor = configure.window.buttonArea.color.background
                        if configure.window.buttonArea.color.foreground is not None:
                            self.buttonForegroundColor = configure.window.buttonArea.color.foreground

            if configure.settings is not None:
                if configure.settings.tempSave is not None:
                    self.tempSave = configure.settings.tempSave
                    self.tempSaveMode.set(1 if self.tempSave else 0)
                if configure.settings.autoSave is not None:
                    self.autoSave = configure.settings.autoSave
                    self.autoSaveMode.set(1 if self.autoSave else 0)

        self.menu = Menu(self)
        self.setMenu()

        Label(
            master=self,
            textvariable=self.info,
            font=(self.infoFont, self.infoFontSize),
            background=self.infoBackgroundColor,
            foreground=self.infoForegroundColor
        ).pack()

        Label(
            master=self,
            textvariable=self.luckyer,
            font=(self.luckyerFont, self.luckyerFontSize),
            background=self.luckyerBackgroundColor,
            foreground=self.luckyerForegroundColor
        ).pack()

        Button(
            master=self,
            text='抽取同学',
            command=self.choose,
        ).pack(padx=10, pady=10)

        self.style.configure(
            'TButton',
            font=(self.buttonFont, self.buttonFontSize),
            background=self.buttonBackgroundColor,
            foreground=self.buttonForegroundColor
        )

        self.configure(background=self.windowBackgroundColor)

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
        SettingMenu = Menu(self.menu, background='white', tearoff=False)
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
        FileMenu.add_command(
            label='保存当前配置',
            command=self.save
        )

        EditMenu.add_command(
            label='重加载',
            command=lambda: (
                self.clear(),
                self.initialize()
            )
        )

        SampleMenu = Menu(self.menu, background='white', tearoff=False)
        SimpleSampleMenu = Menu(self.menu, background='white', tearoff=False)
        SystemSampleMenu = Menu(self.menu, background='white', tearoff=False)
        StratifiedSampleMenu = Menu(self.menu, background='white', tearoff=False)

        for num in range(1, len(self.students) + 1):
            SimpleSampleMenu.add_command(
                label=str(num),
                command=self.simpleSampleMethod(num)
            )

        for num in divisors(len(self.students), generator=True):
            SystemSampleMenu.add_command(
                label=str(num),
                command=self.systemSampleMethod(num)
            )
            StratifiedSampleMenu.add_command(
                label=str(num),
                command=self.stratifiedSampleMethod(num)
            )

        SampleMenu.add_cascade(
            label='简单随机抽样',
            menu=SimpleSampleMenu
        )
        SampleMenu.add_cascade(
            label='系统抽样',
            menu=SystemSampleMenu
        )
        SampleMenu.add_cascade(
            label='分层抽样',
            menu=StratifiedSampleMenu
        )
        EditMenu.add_cascade(
            label='随机抽样',
            menu=SampleMenu
        )

        SettingMenu.add_checkbutton(
            label='缓存',
            variable=self.tempSaveMode,
            command=self.tempSaveModeSwitch
        )
        SettingMenu.add_checkbutton(
            label='自动保存',
            variable=self.autoSaveMode,
            command=self.autoSaveModeSwitch
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
                '版本:Luckyer大乘期至臻版0.2.0\n'
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
            menu=SettingMenu
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
            func=lambda event: self.exit()
        )
        self._root().bind(
            sequence='<Control-n>',
            func=lambda event: self.choose()
        )
        self._root().bind(
            sequence='<Control-s>',
            func=lambda event: self.save()
        )

        self._root().protocol("WM_DELETE_WINDOW", self.exit)

    def configureWindow(self):
        pass

    def exit(self):
        if self.autoSave:
            self.save()
        self._root().destroy()

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

    def save(self):
        self.saveConfigureFile(
            data={
                "students": self.students,
                "survivors": self.survivors if self.tempSave else None,
                "window": {
                    "alpha": self.alpha,
                    "topmost": self.topmost,
                    "size": self.windowSize,
                    "infoArea": {
                        'font': self.infoFont,
                        'fontSize': self.infoFontSize
                    },
                    "luckyerArea": {
                        'font': self.luckyerFont,
                        'fontSize': self.luckyerFontSize
                    },
                    "buttonArea": {
                        'font': self.buttonFont,
                        'fontSize': self.buttonFontSize
                    }
                },
                "settings": {
                    "tempSave": self.tempSave,
                    "autoSave": self.autoSave,
                }
            }
        )

    def autoSaveModeSwitch(self):
        self.autoSave = self.autoSaveMode.get() == 1

    def tempSaveModeSwitch(self):
        self.tempSave = self.tempSaveMode.get() == 1

    def simpleSampleMethod(self, num):
        return lambda: self.simpleSample(num)

    def systemSampleMethod(self, num):
        return lambda: self.systemSample(num)

    def stratifiedSampleMethod(self, num):
        return lambda: self.stratifiedSample(num)

    def simpleSample(self, num):
        showinfo(
            title='简单随机抽样',
            message='结果:' + ', '.join(
                [
                    str(s)
                    for s in choices(self.students, k=num)
                ]
            )
        )

    def systemSample(self, num):
        showinfo(
            title='系统抽样',
            message='结果:' + ', '.join(
                [
                    str(s)
                    for s in self.students[
                             randint(
                                 0,
                                 int(len(self.students) / num) - 1
                             )::
                             int(len(self.students) / num)
                             ]
                ]
            )
        )

    def stratifiedSample(self, num):
        showinfo(
            title='分层抽样',
            message='结果:' + ', '.join(
                [
                    str(choice(s))
                    for s in [
                        self.students[i:i + int(len(self.students) / num)]
                        for i in range(0, len(self.students), int(len(self.students) / num))
                    ]
                ]
            )
        )


if __name__ == '__main__':
    root = Tk()
    root.geometry('300x300-50+50')
    root.title('随机抽取一个幸运同学')
    root.iconphoto(True, PhotoImage(data=const.icon))
    root.configure(background='white')
    root.update()
    app = RandomLuckyer(root)
    app.pack()
    root.mainloop()
