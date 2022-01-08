from tkinter import ttk

def initComboBoxStyle():
    style = ttk.Style()

    style.theme_create('dark_theme', parent='alt',
                             settings = {
                                        'TCombobox':{'configure':
                                          {'fieldbackground': '#1E1E1E',
                                           'background': '#C8C8C8'
                                           }}}
                             )
    style.theme_use('dark_theme')
