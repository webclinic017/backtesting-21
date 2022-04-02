import PySimpleGUI as sg

layout = [
    [sg.Text("Hello from PySimpleGUI")],
    [sg.Button("OK")]
]

# Main window
window = sg.Window(title="Hello world!", layout=layout, margins=(100,50))


# Event loop
while True:
    event, values = window.read()

    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()
