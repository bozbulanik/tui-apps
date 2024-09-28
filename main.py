"""
    File name: main.py
    Description: Simple sticky note taking TUI app.
    Author: Emek Kırarslan
    E-mail: "kirarslanemek@gmail.com"
    Date created: 29/09/2024 - 01:17:00
    Date last modified: 29/09/2024
    Python Version: 3.12.5
    Version: 0.0.1
    License: GNU-GPLv3
    Status: Production
""" 

import urwid as u
from datetime import datetime
import os

class MainWindow(u.WidgetWrap):
    def __init__(self):
        self.textedit = u.Edit(multiline=True)
        self.textedit = u.AttrMap(self.textedit, 'textedit')
        self.listbox = u.ListBox(u.SimpleFocusListWalker([self.textedit]))

        super().__init__(self.listbox)

class Notes(object):
    def unhandled_input(self, key):
        if key in ('q', 'Q', 'ctrl q'):
            raise u.ExitMainLoop()
        elif key == 'tab':
            if(self.tab_pressed):
                self.footer.base_widget.set_text("")
                self.tab_pressed = False
            else:
                self.footer.base_widget.set_text(self.footer_text)
                self.tab_pressed = True
        elif key == 'f1':
            self.save_note()
        
    def __init__(self):
        self.loop = None
        self.palette = [
            ('footer', 'light gray', 'black'),
            ('header', 'light gray', 'black'),
            ('text_error', 'dark red', 'default'),
            ('textedit', 'light gray', 'black'),

        ]
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.current_user = os.getenv('USER') or os.getenv('USERNAME') or os.getlogin()
        self.view = MainWindow()
        self.footer = u.AttrMap(u.Text(f""), 'footer')
        self.tab_pressed = False
        self.footer_text = f"Note created at {self.start_time} by {self.current_user} | F1: save"

    def save_note(self):
            note_content = self.view.textedit.base_widget.get_edit_text()
            
            filename = f"note_{self.start_time}.txt"
            
            with open(filename, 'w') as file:
                file.write(note_content)
            self.footer_text = f"Note saved as {filename} | Press F1 to save another note."
            self.footer.base_widget.set_text(self.footer_text)
            
            
    def run(self):
        self.frame = u.Frame(self.view, header=None, footer=self.footer)
        self.loop = u.MainLoop(self.frame, palette=self.palette, unhandled_input=self.unhandled_input)
        self.loop.run()

if __name__ == "__main__":
    notes = Notes()
    notes.run()






