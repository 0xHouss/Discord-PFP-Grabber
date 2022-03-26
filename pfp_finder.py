import asyncio
import sys
import requests
import json
import os
from tkinter import *
import tkinter.font as font
from PIL import Image, ImageTk
from urllib.request import Request, urlopen
from io import BytesIO

window: Tk = None
with open(sys.path[0] + "\\assets\\config.json", "r") as of:
    token = json.load(of)["token"]

def center_window(window: Frame, w=250, h=280):
    # get screen width and height
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))


def click(event: Event, entries: dict, hide=""):
    leave_all(entries)
    entry = event.widget
    if not entry.get() or entry.get() == entries[entry]:
        entry.delete(0, 'end')
        entry.config(fg='black', show=hide)
    entry.focus()


def leave(entry: Entry, placeholder: str):
    if entry.get() == "":
        entry.delete(0, 'end')
        entry.insert(0, placeholder)
        entry.config(fg='grey', show="")


def leave_all(entries: dict):
    for entry in entries:
        leave(entry, entries[entry])
    window.focus()


def clear(frame: Frame):
    try:
        for widget in frame.winfo_children():
            widget.destroy()
    except:
        pass


def download(image, userid):
    username = requests.get(f'https://discord.com/api/v9/users/{userid}', headers={
        "Authorization": f"Bot {token}"}).json()['username']

    try:
        os.mkdir(sys.path[0] + "\\pfps\\")
    except:
        pass
    image.save(sys.path[0] + f"\\pfps\\pfp_{username}({userid}).png")


async def getpfp(userid=None):
    if userid and len(userid) > 1 and userid != "Enter user id":
        global PFPImage

        avatarid = requests.get(f'https://discord.com/api/v9/users/{userid}', headers={
            "Authorization": f"Bot {token}"}).json()['avatar']

        req = Request(
            f"https://cdn.discordapp.com/avatars/{userid}/{avatarid}.webp", headers={'User-Agent': 'Mozilla/5.0'})

        with urlopen(req) as u:
            raw_data = u.read()

        PFPImage = Image.open(BytesIO(raw_data))

    else:

        PFPImage = Image.open(sys.path[0] + "\\assets\\pfp_default.png")

    TKImage = ImageTk.PhotoImage(PFPImage)
    label = Label(image=TKImage, width=130, height=130, relief=SOLID)
    label.image = TKImage
    label.place(relx=0.5, y=80, anchor=CENTER)


def main():
    MainFrame = Frame(window, bg="white")
    MainFrame.place(relx=0, rely=0, relwidth=1, relheight=1)

    mainFont = font.Font(family='Comic Sans MS', size=10)

    asyncio.run(getpfp())

    IDVar = StringVar()
    IDEntry = Entry(MainFrame, textvariable=IDVar,
                    font=mainFont, width=20, relief=SOLID)
    IDEntry.place(relx=0.5, y=200, anchor=CENTER, width=150)

    DownloadButton = Button(MainFrame, text="Download PFP", font=mainFont,
                            command=lambda: download(PFPImage, IDEntry.get()), width=19, relief=SOLID)
    DownloadButton.place(relx=0.5, y=230, anchor=CENTER, width=150)

    # Bindings
    Entries = {IDEntry: "Enter user id"}

    MainFrame.bind("<Button-1>", lambda event: [leave_all(Entries)])
    window.bind("<FocusOut>", lambda event: [
        leave_all(Entries)])

    IDEntry.bind(
        "<Button-1>", lambda event: [click(event, Entries)])
    leave_all(Entries)

    IDEntry.bind("<KeyRelease>", lambda event: asyncio.run(
        getpfp(IDVar.get())))


if __name__ == '__main__':
    window = Tk()
    center_window(window)
    window.title("Discord Profile Picture Grabber")
    window.iconbitmap(sys.path[0] + '\\assets\\icon.ico')
    window.resizable(False, False)

    main()

    window.mainloop()
