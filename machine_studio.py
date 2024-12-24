import vlc
import tkinter as tk
from tkinter import messagebox
import json

# Create VLC media player instance
player = vlc.MediaPlayer()

# Function to play music from an online stream URL using VLC
def play_music(url):
    try:
        media = vlc.Media(url)
        player.set_media(media)
        player.play()
        update_now_playing(url)  # Update the "Now Playing" label with the URL
    except Exception as e:
        messagebox.showerror("Error", f"Failed to play the radio stream: {e}")

# Function to stop the music
def stop_music():
    player.stop()
    update_now_playing("Stopped")

# Function to update the "Now Playing" label
def update_now_playing(name):
    now_playing_label.config(text=f"Now Playing: {name}")

# Function to load and parse the JSON file containing radio station data
def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            radios = []
            for station in data.get("radios", []):  # Access the 'radios' key
                radios.append({
                    "id": station.get("id"),
                    "name": station.get("name"),
                    "url": station.get("url")
                })
            return radios
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load the JSON file: {e}")
        return []

# Function to create the GUI
def create_gui(radios):
    global now_playing_label

    # Main window setup
    window = tk.Tk()
    window.title("Radio Music Player")
    window.geometry("400x500")
    window.config(bg="#F1F1F1")

    # Title label
    title_label = tk.Label(window, text="Radio Music Player", font=("Segoe UI", 16, 'bold'), bg="#F1F1F1", fg="#4A90E2")
    title_label.pack(pady=10)

    # Now Playing label
    now_playing_label = tk.Label(window, text="Now Playing: None", font=("Segoe UI", 12), bg="#F1F1F1", fg="#4A90E2")
    now_playing_label.pack(pady=10)

    # Create buttons for each radio station URL
    def on_select_radio(url, name):
        stop_music()  # Stop any currently playing music
        play_music(url)  # Play the stream from the URL
        update_now_playing(name)  # Display the radio name in the "Now Playing" label

    # Scrollable canvas setup for radio stations
    canvas_frame = tk.Frame(window, bg="#F1F1F1")
    canvas_frame.pack(pady=10, fill="both", expand=True)

    canvas = tk.Canvas(canvas_frame, bg="#F1F1F1")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    canvas.config(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Frame for buttons (inside the scrollable canvas)
    button_frame = tk.Frame(canvas, bg="#F1F1F1")
    canvas.create_window((0, 0), window=button_frame, anchor="nw")

    # Create radio station buttons
    for idx, station in enumerate(radios):
        btn = tk.Button(button_frame, text=station['name'], width=50, height=2, bg="#4A90E2", fg="white",
                        font=("Segoe UI", 10), relief="flat", command=lambda station=station: on_select_radio(station['url'], station['name']))
        btn.pack(pady=5, padx=10, fill="x")

    # Stop button
    stop_button = tk.Button(window, text="Stop", command=stop_music, width=20, height=2, bg="#E94E77", fg="white",
                            font=("Segoe UI", 12, 'bold'), relief="flat")
    stop_button.pack(pady=30)
    window.iconbitmap("icons8_quran_64_Dzu_icon.ico")  # Make sure to provide the correct path to your .ico file
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 390
    window_height = 540

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")


    # Start the GUI loop
    window.mainloop()

# Main function
if __name__ == "__main__":
    # Load radios from the JSON file
    radios = load_json("radios.json")  # Replace with your actual JSON file path
    
    if radios:
        create_gui(radios)
    else:
        print("No radios available to display.")
