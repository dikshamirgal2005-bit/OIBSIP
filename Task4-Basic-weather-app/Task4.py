import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
from io import BytesIO
import os

API_KEY = "d09143483f83286dd9f85336983488bf"  # Your API Key

# ---------------- Setup absolute paths for small GIFs ---------------- #
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BG_FOLDER = os.path.join(BASE_DIR, "backgrounds")

SUNNY_GIF = os.path.join(BG_FOLDER, "sunny.gif")
RAINY_GIF = os.path.join(BG_FOLDER, "rainy.gif")
CLOUDY_GIF = os.path.join(BG_FOLDER, "cloudy.gif")
SNOW_GIF = os.path.join(BG_FOLDER, "snow.gif")

# ---------------- Placeholder handling ---------------- #
def on_entry_click(event):
    if city_entry.get() == "Enter City":
        city_entry.delete(0, "end")
        city_entry.config(fg="black")

def on_focusout(event):
    if city_entry.get() == "":
        city_entry.insert(0, "Enter City")
        city_entry.config(fg="grey")

# ---------------- Animate small GIF ---------------- #
def animate_small_gif(label, frames, delay, frame_index=0):
    frame = frames[frame_index]
    label.config(image=frame)
    label.image = frame
    label.after(delay, animate_small_gif, label, frames, delay, (frame_index + 1) % len(frames))

def set_small_gif(weather):
    try:
        weather_lower = weather.lower()
        if "rain" in weather_lower or "drizzle" in weather_lower or "thunderstorm" in weather_lower:
            gif_path = RAINY_GIF
        elif "cloud" in weather_lower:
            gif_path = CLOUDY_GIF
        elif "snow" in weather_lower:
            gif_path = SNOW_GIF
        else:
            gif_path = SUNNY_GIF

        gif = Image.open(gif_path)
        frames = [ImageTk.PhotoImage(frame.copy().resize((100,100))) for frame in ImageSequence.Iterator(gif)]
        animate_small_gif(weather_gif_label, frames, delay=100)

    except Exception as e:
        print("Error loading GIF:", e)

# ---------------- Fetch weather ---------------- #
def get_weather():
    city = city_entry.get().strip()
    if city == "" or city == "Enter City":
        messagebox.showerror("Error", "Please enter a city name")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] != 200:
            messagebox.showerror("Error", "City not found. Enter a valid city.")
            return

        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        desc = data["weather"][0]["description"].title()

        # Update labels
        temp_label.config(text=f"{temp}°C")
        feels_label.config(text=f"Feels Like: {feels}°C")
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_label.config(text=f"Wind Speed: {wind} m/s")
        desc_label.config(text=desc)

        # Set small animated GIF
        set_small_gif(desc)

    except Exception as e:
        messagebox.showerror("Error", f"Unable to fetch weather. {e}")

# ---------------- GUI ---------------- #
root = tk.Tk()
root.title("Weather App")
root.geometry("400x500")
root.resizable(False, False)
root.config(bg="#e3f2fd")

# Title
title_label = tk.Label(root, text="🌤 Weather Forecast", font=("Helvetica", 24, "bold"), bg="#e3f2fd", fg="#34495e")
title_label.pack(pady=20)

# Input Frame
input_frame = tk.Frame(root, bg="#e3f2fd")
input_frame.pack(pady=10)

city_entry = tk.Entry(input_frame, font=("Helvetica", 16), width=20, bd=2, relief="groove", fg="grey")
city_entry.pack(side="left", padx=10)
city_entry.insert(0, "Enter City")
city_entry.bind("<FocusIn>", on_entry_click)
city_entry.bind("<FocusOut>", on_focusout)

search_btn = tk.Button(input_frame, text="Get Weather", font=("Helvetica", 14), bg="#3498db", fg="white",
                       activebackground="#2980b9", command=get_weather)
search_btn.pack(side="left")

# Small GIF Label
weather_gif_label = tk.Label(root, bg="#e3f2fd")
weather_gif_label.pack(pady=10)

# Weather Info Frame
info_frame = tk.Frame(root, bg="#e3f2fd")
info_frame.pack(pady=10)

temp_label = tk.Label(info_frame, text="", font=("Helvetica", 32, "bold"), bg="#e3f2fd", fg="#e67e22")
temp_label.pack(pady=5)

desc_label = tk.Label(info_frame, text="", font=("Helvetica", 20), bg="#e3f2fd", fg="#2c3e50")
desc_label.pack(pady=5)

feels_label = tk.Label(info_frame, text="", font=("Helvetica", 14), bg="#e3f2fd")
feels_label.pack(pady=2)

humidity_label = tk.Label(info_frame, text="", font=("Helvetica", 14), bg="#e3f2fd")
humidity_label.pack(pady=2)

wind_label = tk.Label(info_frame, text="", font=("Helvetica", 14), bg="#e3f2fd")
wind_label.pack(pady=2)

# Footer
footer_label = tk.Label(root, text="Data provided by OpenWeatherMap", font=("Helvetica", 10), bg="#e3f2fd", fg="#7f8c8d")
footer_label.pack(side="bottom", pady=10)

root.mainloop()
