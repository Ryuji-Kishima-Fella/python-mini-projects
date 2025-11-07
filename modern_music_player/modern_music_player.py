import os
import pygame
import requests
import customtkinter as ctk
from tkinter import filedialog, END

# ------------------------------------------------------------
# Initialize
# ------------------------------------------------------------
ctk.set_appearance_mode("dark")  # "light" or "dark"
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🎵 Modern Music Player Pro")
app.geometry("700x550")

# ------------------------------------------------------------
# Download images (optional)
# ------------------------------------------------------------
def download_image(url, filename):
    if not os.path.exists(filename):
        response = requests.get(url)
        with open(filename, "wb") as f:
            f.write(response.content)

icons = {
    "play": "https://media.geeksforgeeks.org/wp-content/uploads/20240610151926/play.png",
    "pause": "https://media.geeksforgeeks.org/wp-content/uploads/20240610151926/pause.png",
    "next": "https://media.geeksforgeeks.org/wp-content/uploads/20240610151926/next.png",
    "previous": "https://media.geeksforgeeks.org/wp-content/uploads/20240610151926/previous.png",
}

for name, url in icons.items():
    download_image(url, f"{name}.png")

# ------------------------------------------------------------
# Music system setup
# ------------------------------------------------------------
pygame.mixer.init()
playlist = []
current_song = ""
is_paused = False
current_directory = ""
song_length = 0

# ------------------------------------------------------------
# Functions
# ------------------------------------------------------------
def load_music():
    global current_directory
    current_directory = filedialog.askdirectory()
    if not current_directory:
        return

    playlist.clear()
    playlist_box.delete("1.0", END)

    for file in os.listdir(current_directory):
        if file.endswith(".mp3"):
            playlist.append(file)
            playlist_box.insert(END, file + "\n")

def play_music():
    global current_song, is_paused, song_length
    if not playlist:
        return

    selection = playlist_box.get("insert linestart", "insert lineend").strip()
    if selection and selection in playlist:
        current_song = selection

    if not is_paused:
        song_path = os.path.join(current_directory, current_song)
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        song_length = get_song_length(song_path)
    else:
        pygame.mixer.music.unpause()
        is_paused = False

    status_label.configure(text=f"▶ Playing: {current_song}")
    update_progress_bar()

def pause_music():
    global is_paused
    pygame.mixer.music.pause()
    is_paused = True
    status_label.configure(text=f"⏸ Paused: {current_song}")

def next_song():
    global current_song
    if not playlist:
        return
    idx = playlist.index(current_song)
    current_song = playlist[(idx + 1) % len(playlist)]
    play_music()

def previous_song():
    global current_song
    if not playlist:
        return
    idx = playlist.index(current_song)
    current_song = playlist[(idx - 1) % len(playlist)]
    play_music()

def toggle_theme():
    current = ctk.get_appearance_mode()
    ctk.set_appearance_mode("light" if current == "dark" else "dark")

def set_volume(value):
    pygame.mixer.music.set_volume(float(value))

def get_song_length(filepath):
    try:
        from mutagen.mp3 import MP3
        audio = MP3(filepath)
        return audio.info.length
    except:
        return 0

def update_progress_bar():
    if pygame.mixer.music.get_busy() and not is_paused and song_length > 0:
        current_pos = pygame.mixer.music.get_pos() / 1000.0  # milliseconds → seconds
        progress = min(current_pos / song_length, 1.0)
        progress_bar.set(progress)
        current_time_label.configure(text=f"{int(current_pos // 60)}:{int(current_pos % 60):02d}")
    app.after(500, update_progress_bar)

# ------------------------------------------------------------
# UI Layout
# ------------------------------------------------------------
title_label = ctk.CTkLabel(app, text="🎶 Modern Music Player Pro", font=("Segoe UI", 24, "bold"))
title_label.pack(pady=15)

# Playlist area
playlist_frame = ctk.CTkFrame(app, corner_radius=10)
playlist_frame.pack(padx=20, pady=10, fill="both", expand=True)

playlist_box = ctk.CTkTextbox(playlist_frame, width=500, height=250, font=("Consolas", 13))
playlist_box.pack(padx=10, pady=10, fill="both", expand=True)

# Status bar
status_label = ctk.CTkLabel(app, text="No song playing", font=("Segoe UI", 14))
status_label.pack(pady=5)

# Progress bar
progress_frame = ctk.CTkFrame(app)
progress_frame.pack(pady=5, fill="x", padx=40)

current_time_label = ctk.CTkLabel(progress_frame, text="0:00", width=50)
current_time_label.pack(side="left")

progress_bar = ctk.CTkProgressBar(progress_frame, width=400)
progress_bar.pack(side="left", expand=True, padx=10)
progress_bar.set(0)

total_time_label = ctk.CTkLabel(progress_frame, text="--:--", width=50)
total_time_label.pack(side="right")

# Volume control
volume_frame = ctk.CTkFrame(app)
volume_frame.pack(pady=5)
ctk.CTkLabel(volume_frame, text="🔊 Volume").pack(side="left", padx=5)
volume_slider = ctk.CTkSlider(volume_frame, from_=0, to=1, command=set_volume)
volume_slider.set(0.7)
volume_slider.pack(side="left", padx=10)

# Controls
controls_frame = ctk.CTkFrame(app, corner_radius=15)
controls_frame.pack(pady=10)

btn_prev = ctk.CTkButton(controls_frame, text="⏮", width=60, command=previous_song)
btn_play = ctk.CTkButton(controls_frame, text="▶", width=60, fg_color="#4CAF50", command=play_music)
btn_pause = ctk.CTkButton(controls_frame, text="⏸", width=60, fg_color="#FFC107", command=pause_music)
btn_next = ctk.CTkButton(controls_frame, text="⏭", width=60, command=next_song)
btn_theme = ctk.CTkButton(controls_frame, text="🌓", width=60, fg_color="#607D8B", command=toggle_theme)

btn_prev.grid(row=0, column=0, padx=10)
btn_play.grid(row=0, column=1, padx=10)
btn_pause.grid(row=0, column=2, padx=10)
btn_next.grid(row=0, column=3, padx=10)
btn_theme.grid(row=0, column=4, padx=10)

# Load music button
load_button = ctk.CTkButton(app, text="📂 Select Folder", command=load_music)
load_button.pack(pady=10)

# ------------------------------------------------------------
# Run app
# ------------------------------------------------------------
app.mainloop()
