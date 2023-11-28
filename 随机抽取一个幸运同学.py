from tkinter.ttk import Button, Label, Style
from tkinter import Tk, StringVar
from tkinter.font import Font
from random import randint

students = list(range(1, 51))
survivors = students.copy()

def choose():
    global survivors

    luckyer.set(
        survivors.pop(
            randint(0, len(survivors) - 1)
        )
    )

    if len(survivors) == 0:
        survivors = students.copy()
    
    info.set(f'剩余同学:{len(survivors)}')


root = Tk()
root.attributes('-alpha', 0.8)
root.attributes('-topmost', True)
root.geometry('300x300')
root.title('随机抽取一个幸运同学')

stype = Style()
stype.configure(
    'TButton',
    font=('微软雅黑', 15)
)

luckyer = StringVar(value='0')
info = StringVar(value=f'剩余同学:{len(survivors)}')

Label(
    master=root,
    textvariable=info,
    font=('微软雅黑', 12)
).pack()

Label(
    master=root,
    textvariable=luckyer,
    font=('微软雅黑', 100)
).pack()
Button(
    master=root,
    text='抽取同学',
    command=choose
).pack(padx=10, pady=10)


root.mainloop()



