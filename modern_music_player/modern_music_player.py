import ttkbootstrap as ttk
from ttkbootstrap.constants import *

app = ttk.Window(title="Modern Music Player", themename="darkly", size=(600, 400))

style = ttk.Style()
style.configure('TButton', font=('Segoe UI', 11))
style.configure('TLabel', font=('Segoe UI', 12))

frame = ttk.Frame(app, padding=10)
frame.pack(fill=BOTH, expand=True)

playlist_box = ttk.Treeview(frame, columns=("Songs"), show="headings", height=10)
playlist_box.heading("Songs", text="Songs in Playlist")
playlist_box.pack(fill=BOTH, expand=True, pady=10)

button_frame = ttk.Frame(frame)
button_frame.pack(pady=10)

ttk.Button(button_frame, text="⏮ Previous", bootstyle="secondary-outline").pack(side=LEFT, padx=5)
ttk.Button(button_frame, text="▶ Play", bootstyle="success-outline").pack(side=LEFT, padx=5)
ttk.Button(button_frame, text="⏸ Pause", bootstyle="warning-outline").pack(side=LEFT, padx=5)
ttk.Button(button_frame, text="⏭ Next", bootstyle="secondary-outline").pack(side=LEFT, padx=5)

app.mainloop()
