import os
import PySimpleGUI as sg        # https://github.com/PySimpleGUI/PySimpleGUI/tree/master/DemoPrograms


def layout_01():
    title = "Hello world!"
    layout = [
        [sg.Text("Hello from PySimpleGUI")],
        [sg.Button("OK")]
    ]
    return title, layout

def layout_02():
    title = "Image browser"
    file_list_column = [
        [
            sg.Text("Image Folder"),
            sg.In(size=(25,1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse()
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40,20),
                key="-FILE LIST-"
            )
        ]
    ]

    image_viewer_column = [
        [sg.Text("Choose an image:")],
        [sg.Text(size=(40,1), key="-TPATH-")],
        [sg.Text(size=(40,1), key="-TFILE-")],
        [sg.Image(key="-IMAGE-")]
    ]

    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeparator(),
            sg.Column(image_viewer_column)
        ]
    ]

    return title, layout


#title, layout = layout_01()
title, layout = layout_02()
window = sg.Window(title=title, layout=layout)


# Event loop

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    if event == "OK":
        break
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            files = os.listdir(folder)
        except Exception as e:
            files = []
        fnames = [f for f in files if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith((".png",".gif")) ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":
        try:
            filename = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])
            window["-TPATH-"].update(values["-FOLDER-"])
            window["-TFILE-"].update(values["-FILE LIST-"][0])
            window["-IMAGE-"].update(filename=filename)
        except Exception as e:
            pass

window.close()
