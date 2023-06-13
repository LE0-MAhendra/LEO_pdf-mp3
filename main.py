import PySimpleGUI as sg
import os
import PyPDF2
import pyttsx3
from random_word import RandomWords


def randomname():
    r = RandomWords()
    word = r.get_random_word()
    return str(word)


layout = [
    [sg.Text("Image File"),
        sg.Input(size=(45, 1)),
        sg.FileBrowse(key="-FILE-", file_types=("PDF Document", "*.pdf"),)],
    [sg.Text('enter the starting page', size=(18, 1)), sg.InputText()],
    [sg.Text('enter the last page', size=(18, 1)), sg.InputText()],
    [sg.Button("make mp3", key="-LOAD-")]
]
window = sg.Window('Window Title', layout)
speak = pyttsx3.init()
while True:
    event, values = window.read()
    if event in [sg.WIN_CLOSED, 'Cancel']:
        break
    if event == "-LOAD-" and os.path.exists(values["-FILE-"]):
        pdf = open(values["-FILE-"], "rb")
        reader = PyPDF2.PdfReader(pdf)
        start = int(values[1]) if values[1] else None
        last = int(values[2]) if values[2] else None

        audio_filename = f"{randomname()}.mp3"

        if start is None and last is not None:
            output_text = ""
            for page in range(last):
                current_page = reader.pages[page]
                text = current_page.extract_text()
                output_text += text

        elif start is None and last is None:
            output_text = ""
            no_of_pages = len(reader.pages)
            for page in range(no_of_pages):
                current_page = reader.pages[page]
                text = current_page.extract_text()
                output_text += text

        else:
            output_text = ""
            no_of_pages = len(reader.pages)
            for page in range(start, min(last, no_of_pages)):
                current_page = reader.pages[page]
                text = current_page.extract_text()
                output_text += text
    speak.save_to_file(output_text, audio_filename)
    speak.runAndWait()
