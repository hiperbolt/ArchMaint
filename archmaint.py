from tkinter import *
from tkinter import messagebox
from sys import exit
from subprocess import *
import shutil
import  os

'''
This program was created by hiperbolt (tomasimoes03@gmail.com / hiperbolt.wordpress.com) and implements rmshit.py by Jakub Klinkovský (lahwaacz).
'''

__author__ = 'hiperbolt'

shittyfiles = [
    '~/.adobe',              # Flash crap
    '~/.macromedia',         # Flash crap
    '~/.recently-used',
    '~/.local/share/recently-used.xbel',
    '~/Desktop',             # Firefox creates this
    '~/.thumbnails',
    '~/.gconfd',
    '~/.gconf',
    '~/.local/share/gegl-0.2',
    '~/.FRD/log/app.log',   # FRD
    '~/.FRD/links.txt',     # FRD
    '~/.objectdb',          # FRD
    '~/.gstreamer-0.10',
    '~/.pulse',
    '~/.esd_auth',
    '~/.config/enchant',
    '~/.spicec',            # contains only log file; unconfigurable
    '~/.dropbox-dist',
    '~/.parallel',
    '~/.dbus',
    '~/ca2',                # WTF?
    '~/ca2~',               # WTF?
    '~/.distlib/',          # contains another empty dir, don't know which software creates it
    '~/.bazaar/',           # bzr insists on creating files holding default values
    '~/.bzr.log',
    '~/.nv/',
    '~/.viminfo',           # configured to be moved to ~/.cache/vim/viminfo, but it is still sometimes created...
    '~/.npm/',              # npm cache
]

def yesno():
    return True


def rmshit():
    print("Found shittyfiles:")
    found = []
    for f in shittyfiles:
        absf = os.path.expanduser(f)
        if os.path.exists(absf):
            found.append(absf)
            print("    %s" % f)

    if len(found) == 0:
        print("No shitty files found :)")
        return

    if yesno():
        for f in found:
            if os.path.isfile(f):
                os.remove(f)
            else:
                shutil.rmtree(f)
        print("All cleaned")
    else:
        print("No file removed")


class RootWindow:
    def __init__(self, window):
        self.window = window
        self.window.geometry('1000x800')
        self.window.title('ArchMaint')
        self.frame1 = Frame(self.window)
        self.frame2 = Frame(self.window)
        self.label1 = Label(self.frame1, text='Welcome to ArchMaint', font=5)
        self.button1 = Button(self.frame2, text='Update Pacman Packages', width='20',
                              command=lambda: self.updatepackges())
        self.button2 = Button(self.frame2, text='Clear Pacman Cache', width='20', command=lambda: self.clearcache())
        self.button3 = Button(self.frame2, text='Clear Orphaned Packages', width='20',
                              command=lambda: self.clearorphaned())
        self.button4 = Button(self.frame2, text='Optimize Package Database', width='20',
                              command=lambda: self.optimizedatabase())
        self.button5 = Button(self.frame2, text='Clear Broken Symlinks', width='20',
                              command=lambda: self.clearsymlinks())
        self.button6 = Button(self.frame2, text='Clear TempFiles', width='20', command=lambda: self.cleartemps())
        self.button7 = Button(self.frame2, text='Credits', width='20', command=lambda: messagebox.showinfo("Credits",
                                                                                                           "Originally Made by: hiperbolt / Tomás Simões (tomasimoes03@gmail.com)"))
        self.button8 = Button(self.frame2, text='Exit', width='20', command=lambda: exit())
        self.frame1.pack(anchor='nw')
        self.frame2.pack(anchor='center')
        self.label1.pack()
        self.button1.pack()
        self.button2.pack()
        self.button3.pack()
        self.button4.pack()
        self.button5.pack()
        self.button6.pack()
        self.button7.pack()
        self.button8.pack()

    def updatepackges(self):
        try:
            check_call('pacman --noconfirm -Syyu', shell=True)
        except CalledProcessError:
            messagebox.showerror('Error', 'An error occurred, that is all we know.')
        else:
            messagebox.showinfo("Sucess", "Pacman Packages Updated!")

    def clearcache(self):
        try:
            check_call("pacman --noconfirm -Sc", shell=True)
        except CalledProcessError:
            messagebox.showerror('Error', 'An error occurred, that is all we know.')
        else:
            messagebox.showinfo('Success', 'Pacman Package Cache Cleared!')

    def clearorphaned(self):
        try:
            check_call('pacman -Rns $(pacman -Qtdq)', shell=True)
        except CalledProcessError:
            messagebox.showerror('Error', 'Either you had no orphaned packages or something wrong occurred.')
        else:
            messagebox.showinfo('Success', 'Orphaned Packages Cleared')

    def optimizedatabase(self):
        try:
            check_call('pacman-optimize --nocolor', shell=True)
        except CalledProcessError:
            messagebox.showerror('Error', 'An error occurred, that is all we know.')
        else:
            messagebox.showinfo('Success', 'Pacman Database Optimized.')

    def clearsymlinks(self):
        try:
            check_call('find . -type l -! -exec test -e {} \; -delete', shell=True)
        except CalledProcessError:
            messagebox.showerror('Error', 'An error occurred, that is all we know.')
        else:
            messagebox.showinfo('Success', 'Broken Symlinks Cleared.')

    def cleartemps(self):
        rmshit()

if __name__ == '__main__':
    root = Tk()
    RootWindow(root)
    root.mainloop()
