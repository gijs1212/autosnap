# autosnap
📸 Snap Automator – Auto Snap Sender for Snapchat
🟡 What is this?
Snap Automator is a Python desktop tool designed to automatically send snaps in Snapchat by simulating mouse clicks at calibrated positions. It helps automate repetitive Snapchat actions, like sending a snap to selected friends — over and over again — without manual clicking.

✨ Features
🖱️ Mouse calibration – Select screen positions by hovering your mouse over buttons (e.g. camera, send)

👥 Choose recipients – Up to 8 people, each with an individual position

🔁 Repeating – Choose how many times to repeat or run until manually stopped

🧠 Config persistence – Saves your calibration settings between sessions

💻 No console or taskbar icon – Runs quietly in the background with a clean UI

🖼️ Custom window icon – Includes a Snapchat-style icon

🛠️ Requirements
Windows OS

Python 3.8 or higher

Python modules:

tkinter (usually built-in)

pyautogui

ctypes, os, json, time

Install the only external dependency:
```bash
pip install pyautogui

🚀 How to Use
Download the repository

Make sure snapchat_black_logo_icon_147080.ico is in the same folder

Run autosnap.py

Click 🔧 Recalibrate and follow the prompts to set:

Camera button

Second photo button

Send-after-photo button

Up to 8 recipient buttons

Final send button

Choose how many times to repeat the action or select "until app closes"

Click ▶️ Start Automation

Watch your snaps get sent automatically!

🧪 Tip: Test First
You can first calibrate using dummy windows or screenshots to test behavior without sending real snaps.

Files required:
snapchat_black_logo_icon_147080.ico	App window icon (Snapchat style)

🧠 Note
This tool does not interact with Snapchat APIs

It only simulates mouse clicks on screen positions, so you must keep the Snapchat window in focus

Use responsibly. This is meant for educational or personal purposes.
