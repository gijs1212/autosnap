import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import time
import json
import os
import ctypes

# ⬇️ Minimaliseer consolevenster bij start
def minimize_console():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
    except:
        pass

CONFIG_FILE = "muis_config.json"

DEFAULT_CONFIG = {
    "foto1": None,
    "foto2": None,
    "verstuur_na_foto": None,
    "personen": [None] * 8,
    "verzend": None
}

# ⬇️ Configuratie opslaan/opladen
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()

# ⬇️ Kalibratie popup
def kalibreer_pos(naam):
    countdown = tk.Toplevel()
    countdown.title("Kalibratie")
    countdown.geometry("320x140")
    countdown.resizable(False, False)
    countdown.attributes("-topmost", True)

    ttk.Label(countdown, text=f"Beweeg je muis naar:\n{naam}", font=("Segoe UI", 12)).pack(pady=8)
    timer_label = ttk.Label(countdown, text="", font=("Segoe UI", 22, "bold"))
    timer_label.pack()

    def aftellen(seconden):
        if seconden == 0:
            countdown.destroy()
            pos = pyautogui.position()
            messagebox.showinfo("Opgeslagen", f"{naam} opgeslagen op {pos}")
            countdown.result = (pos.x, pos.y)
        else:
            timer_label.config(text=str(seconden))
            countdown.after(1000, lambda: aftellen(seconden - 1))

    countdown.result = None
    aftellen(3)
    countdown.grab_set()
    countdown.wait_window()
    return countdown.result

# ⬇️ Hoofdapplicatieklasse
class MuisAutomatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🖱️ Muis Automator")
        self.root.geometry("450x550")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        self.config = load_config()
        self.build_ui()

    def build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TCheckbutton", font=("Segoe UI", 10))
        style.configure("TLabel", font=("Segoe UI", 10))

        # 🔧 Kalibratieknop
        ttk.Button(self.root, text="🔧 Recalibreren", command=self.recalibrate).pack(pady=12)

        # 👥 Personen selectie
        personen_frame = ttk.LabelFrame(self.root, text="👥 Personen kiezen", padding=10)
        personen_frame.pack(padx=10, pady=10, fill="x")

        self.person_vars = [tk.BooleanVar(value=True) for _ in range(8)]
        for i in range(8):
            cb = ttk.Checkbutton(personen_frame, text=f"Persoon {i+1}", variable=self.person_vars[i])
            cb.grid(row=i//4, column=i%4, padx=8, pady=5, sticky="w")

        # 🔁 Herhalingsinstellingen
        settings_frame = ttk.LabelFrame(self.root, text="⚙️ Instellingen", padding=10)
        settings_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(settings_frame, text="Aantal keer afspelen:").grid(row=0, column=0, sticky="w", pady=5)
        self.count_var = tk.IntVar(value=1)
        ttk.Entry(settings_frame, textvariable=self.count_var, width=10).grid(row=0, column=1, padx=5)

        self.until_closed_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_frame, text="Tot programma sluiten", variable=self.until_closed_var).grid(row=1, column=0, columnspan=2, sticky="w", pady=5)

        ttk.Label(settings_frame, text="Delay tussen herhalingen (seconden):").grid(row=2, column=0, sticky="w", pady=5)
        self.delay_var = tk.DoubleVar(value=1.0)
        ttk.Entry(settings_frame, textvariable=self.delay_var, width=10).grid(row=2, column=1, padx=5)

        # ▶️ Startknop
        ttk.Button(self.root, text="▶️ Start Automatisering", command=self.start_automation).pack(pady=20)

        # ✅ Statuslabel
        self.status_label = ttk.Label(self.root, text="", foreground="green", font=("Segoe UI", 10, "italic"))
        self.status_label.pack()

    def recalibrate(self):
        self.status_label.config(text="Kalibreren bezig...")

        self.config["foto1"] = kalibreer_pos("Foto knop 1")
        self.config["foto2"] = kalibreer_pos("Foto knop 2")
        self.config["verstuur_na_foto"] = kalibreer_pos("Verstuur-na knop")

        for i in range(8):
            if messagebox.askyesno("Kalibratie", f"Wil je Persoon {i+1} kalibreren?"):
                self.config["personen"][i] = kalibreer_pos(f"Persoon {i+1}")
            else:
                self.config["personen"][i] = None

        self.config["verzend"] = kalibreer_pos("Verzend knop")

        save_config(self.config)
        self.status_label.config(text="✅ Kalibratie opgeslagen.")

    def start_automation(self):
        personen = [i for i, var in enumerate(self.person_vars) if var.get()]
        count = self.count_var.get()
        delay = self.delay_var.get()
        endless = self.until_closed_var.get()

        if not all([self.config["foto1"], self.config["foto2"], self.config["verstuur_na_foto"], self.config["verzend"]]):
            messagebox.showerror("Fout", "❗ Je moet eerst alles kalibreren.")
            return

        self.root.after(100, lambda: self.run_sequence(personen, count, delay, endless))

    def run_sequence(self, personen, count, delay, endless):
        def do_click(x, y):
            pyautogui.moveTo(x, y)
            pyautogui.click()

        try:
            while endless or count > 0:
                self.status_label.config(text="🔄 Automatisering bezig...")
                self.root.update()

                do_click(*self.config["foto1"])
                time.sleep(5)
                do_click(*self.config["foto2"])
                time.sleep(0.5)
                do_click(*self.config["verstuur_na_foto"])
                time.sleep(0.5)

                for i in personen:
                    pos = self.config["personen"][i]
                    if pos:
                        do_click(*pos)
                        time.sleep(0.5)

                do_click(*self.config["verzend"])
                if not endless:
                    count -= 1
                time.sleep(delay)

            self.status_label.config(text="✅ Automatisering voltooid.")
        except Exception as e:
            messagebox.showerror("Fout", str(e))
            self.status_label.config(text="❌ Fout tijdens uitvoering.")

# ⬇️ Start de app met icoon
if __name__ == "__main__":
    minimize_console()
    root = tk.Tk()
    root.iconbitmap("snapchat_black_logo_icon_147080.ico")  # ← voeg je icoon hier toe
    app = MuisAutomatorApp(root)
    root.mainloop()
