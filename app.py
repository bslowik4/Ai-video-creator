import requests
from bs4 import BeautifulSoup
from tkinter import Tk, Text, Button, Entry, filedialog, END
from moviepy.editor import VideoFileClip, AudioFileClip
import os

def url_scraper(url):
    fetch = requests.get(url)
    soup = BeautifulSoup(fetch.content, 'html.parser')
    paragraphs = [p.get_text() for p in soup.find_all('p')]
    return '\n'.join(paragraphs)

def save_selected_text():
    selected_text = text_box.get(1.0, END)
    with open('selected_text.txt', 'w') as f:
        f.write(selected_text)
    generate_tts('selected_text.txt')

def generate_tts(text_file):
    with open(text_file, 'r') as file:
        text = file.read()

    tts_url = 'https://ttsmp3.com/makemp3_new.php'
    params = {'msg': text, 'lang': 'Joanna', 'source': 'ttsmp3'}
    final = requests.post(tts_url, data=params)

    with open('audio.mp3', 'wb') as f:
        f.write(final.content)

    choose_background_video()

def choose_background_video():
    video_path = filedialog.askopenfilename(title="Select Background Video", filetypes=[("Video files", "*.mp4")])
    if video_path:
        create_video(video_path, 'audio.mp3')

def create_video(background_video_path, audio_path):
    video = VideoFileClip(background_video_path)
    audio = AudioFileClip(audio_path)
    final = video.set_audio(audio)
    output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    final.write_videofile(output_path, codec="libx264")
    print("Video created successfully!")

def setup_gui():
    root = Tk()
    root.title("AI Video Creator")

    global text_box
    text_box = Text(root, height=20, width=80)
    text_box.pack()

    def fetch_text_from_url():
        url = url_entry.get()
        extracted_text = url_scraper(url)
        text_box.delete(1.0, END)
        text_box.insert(END, extracted_text)

    global url_entry
    url_entry = Entry(root, width=50)
    url_entry.pack()

    fetch_button = Button(root, text="Fetch Text from URL", command=fetch_text_from_url)
    fetch_button.pack()

    select_button = Button(root, text="Create Video", command=save_selected_text)
    select_button.pack()

    root.mainloop()

if __name__ == "__main__":
    setup_gui()
