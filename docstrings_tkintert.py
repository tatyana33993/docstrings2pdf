#!/usr/bin/env python3
from tkinter import *
import docstrings
import styles
from functools import partial
from pygments import highlight
from pygments.lexers import python
from pygments.formatters import other

result = {}


def get_filename(event):
    global result
    filename = entry.get()
    try:
        result = docstrings.get_docstrings(filename)
    except FileNotFoundError:
        filename = entry.get()
        result = docstrings.get_docstrings(filename)
    entry.destroy()
    button_ok.destroy()
    button_module = Button(tree, text=filename, background='PaleVioletRed1',
                           activebackground='PaleVioletRed3',
                           command=partial(get_docstring, result['.']))
    button_module.place(x=10, y=10)
    tree.create_line(10, 10, 10, 10 + 50)
    tree.create_line(10, 60, 10 + 200, 60)
    previousclass = ''
    x = 210
    y = 60
    for k, v in result.items():
        if k == '.':
            continue
        num = k.find('.')
        if previousclass == k[:num]:
            button_def = Button(tree, text=k[num + 1:],
                                background='aquamarine2',
                                activebackground='aquamarine4',
                                command=partial(get_docstring, v))
            button_def.place(x=x, y=y)
            tree.create_line(x - 100, y - 50, x - 100, y)
            tree.create_line(x - 100, y, x, y)
            y += 50
        elif previousclass != k[:num]:
            x -= 100
            button_class = Button(tree, text=k[:num],
                                  background='MediumPurple2',
                                  activebackground='MediumPurple4',
                                  command=partial(get_docstring, v))
            button_class.place(x=x, y=y)
            tree.create_line(x - 100, 10, x - 100, y)
            tree.create_line(x - 100, y, x, y)
            x += 100
            y += 50
            button_def = Button(tree, text=k[num + 1:],
                                background='aquamarine2',
                                activebackground='aquamarine4',
                                command=partial(get_docstring, v))
            button_def.place(x=x, y=y)
            tree.create_line(x - 100, y - 50, x - 100, y)
            tree.create_line(x - 100, y, x, y)
            y += 50
            previousclass = k[:num]


def get_docstring(v):
    comments.delete('text')
    docstrings_with_flags = is_doctests(v)
    row = 20
    column = 20
    for e in docstrings_with_flags:
        print(e)
        doctest = e[0]
        str = e[1]
        if doctest is False:
            comments.create_text(column, row, font=('Purisa', '9', 'italic'),
                                 fill='black', anchor=NW,
                                 text=str, tag='text')
            row += 20
        else:
            w = open('helper.txt', 'wb')
            highlight(str, python.Python3Lexer(), other.RawTokenFormatter(), w)
            w.close()

            r = open('helper.txt', 'r')
            for line in r:
                newline = line.replace(r'\n', '')
                color = ''
                key = newline[newline.find('Token.') + 6:newline.find('\t')]
                value = newline[newline.find('\'') + 1:newline.rfind('\'')]
                if key in styles.style.keys():
                    color = styles.style[key]
                if color != '':
                    comments.create_text(column, row,
                                         font=('Purisa', '9', 'italic'),
                                         fill=color, anchor=NW,
                                         text=value.strip(), tag='text')
                else:
                    comments.create_text(column, row,
                                         font=('Purisa', '9', 'italic'),
                                         fill='black', anchor=NW,
                                         text=value.strip(), tag='text')
                column += (len(value) * 10)
            row += 20
            column = 20
            r.close()


def is_doctests(value):
    docstrings_with_flags = []
    arr = value.split('\n')
    prev = False
    for e in arr:
        if e.find('>>>') != -1 or e.find('...') != -1:
            prev = True
            docstrings_with_flags.append((True, e))
        elif prev:
            docstrings_with_flags.append((True, e))
            prev = False
        else:
            docstrings_with_flags.append((False, e))
    return docstrings_with_flags


root = Tk()
root.title('Docstrings')
root.geometry('1200x1000+300+200')
root.resizable(False, False)
entry = Entry()
button_ok = Button(root, text='Ok')
tree = Canvas(root, width=600, height=1000, bg='misty rose')
comments = Canvas(root, width=600, height=1000, bg='white')
entry.pack(side='top')
button_ok.pack(side='top')
tree.pack(side='left')
comments.pack(side='right')
button_ok.bind('<Button-1>', get_filename)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.mainloop()
