#Health Application with a focus on Hyptertension patients
#Project based on this criteria User Profile: 
# Allow the user to enter basic details like age, weight, and medical history.
#Data Logging: Create a feature to log daily blood pressure readings.
#Reminders: Use a scheduler to remind users to drink water, exercise, or avoid sugary drinks.
#Insights: Generate a weekly summary and recommendations based on trends.
#Database: Use a simple file or database to store user data.
import sqlite3
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, messagebox, filedialog

# Initialize Database
def init_db():
    conn = sqlite3.connect('health_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blood_pressure (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            systolic INTEGER,
            diastolic INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Log Blood Pressure
def log_blood_pressure():
    systolic = systolic_entry.get()
    diastolic = diastolic_entry.get()
    if not systolic or not diastolic:
        messagebox.showerror("Error", "Please enter both systolic and diastolic values.")
        return
    
    try:
        systolic = int(systolic)
        diastolic = int(diastolic)
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = sqlite3.connect('health_data.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO blood_pressure (date, systolic, diastolic) VALUES (?, ?, ?)', 
                       (date, systolic, diastolic))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Blood pressure logged successfully!")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values.")

# View Logs
def view_logs():
    conn = sqlite3.connect('health_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM blood_pressure')
    rows = cursor.fetchall()
    conn.close()
    if rows:
        logs = "\n".join([f"ID: {row[0]}, Date: {row[1]}, Systolic: {row[2]}, Diastolic: {row[3]}" for row in rows])
        messagebox.showinfo("Blood Pressure Logs", logs)
    else:
        messagebox.showinfo("Logs", "No logs found.")

# Plot Trends
def plot_trends():
    conn = sqlite3.connect('health_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT date, systolic, diastolic FROM blood_pressure')
    data = cursor.fetchall()
    conn.close()
    
    if data:
        dates = [datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") for row in data]
        systolic = [row[1] for row in data]
        diastolic = [row[2] for row in data]
        
        plt.figure(figsize=(10, 5))
        plt.plot(dates, systolic, label="Systolic", color="blue", marker="o")
        plt.plot(dates, diastolic, label="Diastolic", color="green", marker="o")
        plt.title("Blood Pressure Trends")
        plt.xlabel("Date")
        plt.ylabel("Pressure (mmHg)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showinfo("Plot", "No data available to plot.")

# Export Data to CSV
def export_to_csv():
    conn = sqlite3.connect('health_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM blood_pressure')
    data = cursor.fetchall()
    conn.close()
    
    if data:
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file:
            with open(file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Date", "Systolic", "Diastolic"])
                writer.writerows(data)
            messagebox.showinfo("Export", "Data exported successfully!")
    else:
        messagebox.showinfo("Export", "No data available to export.")

# GUI Setup
def main_app():
    global systolic_entry, diastolic_entry
    
    init_db()
    root = Tk()
    root.title("Blood Pressure Tracker")
    root.geometry("400x300")
    
    Label(root, text="Systolic (mmHg):").pack(pady=5)
    systolic_entry = Entry(root)
    systolic_entry.pack(pady=5)
    
    Label(root, text="Diastolic (mmHg):").pack(pady=5)
    diastolic_entry = Entry(root)
    diastolic_entry.pack(pady=5)
    
    Button(root, text="Log Blood Pressure", command=log_blood_pressure).pack(pady=5)
    Button(root, text="View Logs", command=view_logs).pack(pady=5)
    Button(root, text="Plot Trends", command=plot_trends).pack(pady=5)
    Button(root, text="Export to CSV", command=export_to_csv).pack(pady=5)
    Button(root, text="Exit", command=root.quit).pack(pady=5)
    
    root.mainloop()

main_app()
