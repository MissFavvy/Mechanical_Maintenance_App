import tkinter as tk

root = tk.Tk()
root.title("Mechanical Maintenance Management System")
root.geometry("900x600")

def open_equipment_window():
    equipment_window = tk.Toplevel(root)
    equipment_window.title("Equipment Management")
    equipment_window.geometry("800x500")

def open_work_order_window():
    work_order_window = tk.Toplevel(root)
    work_order_window.title("Work Orders")
    work_order_window.geometry("800x500")

def open_schedule_window():
    schedule_window = tk.Toplevel(root)
    schedule_window.title("Maintenance Scheduling")
    schedule_window.geometry("800x500")

def open_history_window():
    history_window = tk.Toplevel(root)
    history_window.title("Maintenance History")
    history_window.geometry("800x500")

heading = tk.Label(root, text="Mechanical Maintenance Management System", font=("Arial", 20, "bold"))
heading.pack(pady=20)
equipment_button = tk.Button(root, text="Equipment Management", font=("Arial", 14), command=open_equipment_window)
equipment_button.pack(pady=10)
work_order_button = tk.Button(root, text="Work Orders", font=("Arial", 14), command=open_work_order_window)
work_order_button.pack(pady=10)
schedule_button = tk.Button(root, text="Maintenance Scheduling", font=("Arial", 14), command=open_schedule_window)
schedule_button.pack(pady=10)
history_button = tk.Button(root, text="Maintenance History", font=("Arial", 14), command=open_history_window)
history_button.pack(pady=10)

root.mainloop()