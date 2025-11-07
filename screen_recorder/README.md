# 🎥 Screen Recorder using Python

A simple screen recorder built in Python that captures your screen in real-time and saves the output as a video file.

## 🧠 About the Project
This project uses **OpenCV**, **PyAutoGUI**, and **NumPy** to record your screen and generate an `.avi` video file.  
It was built as a learning exercise based on a [GeeksforGeeks tutorial](https://www.geeksforgeeks.org/python/create-a-screen-recorder-using-python/).

## ✨ Features
- Captures your entire screen in real-time
- Saves the recording as `output.avi`
- Adjustable recording FPS
- Keyboard interrupt (`Ctrl + C`) to stop recording safely

## 🧩 Technologies Used
- `pyautogui` — for screen capture  
- `cv2` (OpenCV) — for video encoding and saving  
- `numpy` — for image array processing  

## ▶️ How to Run
1. Install dependencies:
   ```bash
   pip install opencv-python pyautogui numpy
   ```
2. Run the script:
   ```bash
   python screen_recorder.py

   ```
3. Press Ctrl + C when you want to stop recording.

## 📂 Example Output
After recording, an output.avi file will appear in the same folder.

You can play it using VLC or any media player.

## 📚 What I Learned

- How to use PyAutoGUI to capture the screen

- How OpenCV writes frame-by-frame video

- Basic understanding of video processing in Python

## 📖 Credits

- Original Tutorial: [GeeksforGeeks](https://www.geeksforgeeks.org/python/create-a-screen-recorder-using-python/)

- Modified and documented by Ryuji Kijima