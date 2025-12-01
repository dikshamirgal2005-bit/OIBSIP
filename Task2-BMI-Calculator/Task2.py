import tkinter as tk
from tkinter import messagebox
import csv
import os
import matplotlib.pyplot as plt
from datetime import datetime

# --------------------------
# BMI CATEGORY FUNCTION
# --------------------------
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# --------------------------
# SAVE HISTORY TO CSV
# --------------------------
def save_history(weight, height, bmi, category):
    file_exists = os.path.isfile("bmi_history.csv")

    with open("bmi_history.csv", "a", newline="") as file:
        writer = csv.writer(file)

        # write header if new file
        if not file_exists:
            writer.writerow(["Date", "Weight", "Height", "BMI", "Category"])

        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), weight, height, bmi, category])

# --------------------------
# SHOW BMI HISTORY GRAPH
# --------------------------
def show_history_graph():
    if not os.path.isfile("bmi_history.csv"):
        messagebox.showinfo("No Data", "No BMI history found!")
        return

    dates = []
    bmi_values = []

    with open("bmi_history.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            dates.append(row["Date"])
            bmi_values.append(float(row["BMI"]))

    plt.figure(figsize=(10, 5))
    plt.plot(dates, bmi_values, marker='o')
    plt.title("BMI History")
    plt.xlabel("Date")
    plt.ylabel("BMI Value")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# --------------------------
# BMI CALCULATION FUNCTION
# --------------------------
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            raise ValueError

        bmi = round(weight / (height * height), 2)
        category = get_bmi_category(bmi)

        result_label.config(text=f"BMI: {bmi} ({category})")

        save_history(weight, height, bmi, category)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid positive numbers!")

# --------------------------
# GUI WINDOW
# --------------------------
root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("400x350")
root.config(bg="lightblue")

title = tk.Label(root, text="BMI CALCULATOR", font=("Arial", 18, "bold"), bg="lightblue")
title.pack(pady=10)

weight_label = tk.Label(root, text="Enter Weight (kg):", font=("Arial", 12), bg="lightblue")
weight_label.pack()
weight_entry = tk.Entry(root, width=20)
weight_entry.pack()

height_label = tk.Label(root, text="Enter Height (m):", font=("Arial", 12), bg="lightblue")
height_label.pack()
height_entry = tk.Entry(root, width=20)
height_entry.pack()

calc_button = tk.Button(root, text="Calculate BMI", command=calculate_bmi, font=("Arial", 12), bg="white")
calc_button.pack(pady=10)

history_button = tk.Button(root, text="Show BMI History Graph", command=show_history_graph, font=("Arial", 12), bg="white")
history_button.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg="lightblue")
result_label.pack(pady=20)

root.mainloop()
