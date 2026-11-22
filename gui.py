import tkinter as tk
import json
from tkinter import ttk, messagebox

# Load the equipment records
with open("equipment_data.json", "r") as file:
    equipment_list = json.load(file)

# Load the ID counters
with open("id_counters.json", "r") as file:
    id_counters = json.load(file)

# Load the work orders
with open("work_orders.json", "r") as file:
    work_order_list = json.load(file)

# Load the maintenance schedules
with open("maintenance_schedule.json", "r") as file:
    maintenance_schedule_list = json.load(file)

# Load the maintenance history
with open("maintenance_history.json", "r") as file:
    maintenance_history_list = json.load(file)

root = tk.Tk()
root.title("Mechanical Maintenance Management System")
root.geometry("900x600")

def open_equipment_window():
    equipment_window = tk.Toplevel(root)
    equipment_window.title("Equipment Management")
    equipment_window.geometry("800x650")

    equipment_heading = tk.Label(
        equipment_window,
        text="Equipment Records",
        font=("Arial", 16, "bold")
    )
    equipment_heading.pack(pady=20)
  
    columns = ("ID", "Name", "Type", "Location", "Temperature", "Vibration", "Operating Hours")
   
    equipment_table = ttk.Treeview(
        equipment_window,
        columns=columns,
        show="headings"
    )
    for col in columns:
        equipment_table.heading(col, text=col)

    for equipment in equipment_list:
        equipment_table.insert("", tk.END, values=(
            equipment["id"],
            equipment["name"],
            equipment["type"],
            equipment["location"],
            equipment["temperature"],
            equipment["vibration"],
            equipment["operating_hours"]
        ))

    equipment_table.pack(pady=20, fill=tk.BOTH, expand=True)

    add_equipment_frame = tk.Frame(equipment_window)

    name_label = tk.Label(add_equipment_frame, text="Equipment Name")
    name_label.grid(row=0, column=0, padx=10, pady=5)

    name_entry = tk.Entry(add_equipment_frame)
    name_entry.grid(row=1, column=0, padx=10, pady=5)

    type_label = tk.Label(add_equipment_frame, text="Equipment Type")
    type_label.grid(row=0, column=1, padx=10, pady=5)

    type_entry = tk.Entry(add_equipment_frame)
    type_entry.grid(row=1, column=1, padx=10, pady=5)

    location_label = tk.Label(add_equipment_frame, text="Equipment Location")
    location_label.grid(row=0, column=2, padx=10, pady=5)

    location_entry = tk.Entry(add_equipment_frame)
    location_entry.grid(row=1, column=2, padx=10, pady=5)

    temperature_label = tk.Label(add_equipment_frame, text="Temperature")
    temperature_label.grid(row=2, column=0, padx=10, pady=5)

    temperature_entry = tk.Entry(add_equipment_frame)
    temperature_entry.grid(row=3, column=0, padx=10, pady=5)

    vibration_label = tk.Label(add_equipment_frame, text="Vibration")
    vibration_label.grid(row=2, column=1, padx=10, pady=5)

    vibration_entry = tk.Entry(add_equipment_frame)
    vibration_entry.grid(row=3, column=1, padx=10, pady=5)

    operating_hours_label = tk.Label(add_equipment_frame, text="Operating Hours")
    operating_hours_label.grid(row=2, column=2, padx=10, pady=5)

    operating_hours_entry = tk.Entry(add_equipment_frame)
    operating_hours_entry.grid(row=3, column=2, padx=10, pady=5)

    def save_equipment():
        equipment_name = name_entry.get().strip().title()
        equipment_type = type_entry.get().strip().title()
        equipment_location = location_entry.get().strip().title()

        temperature = temperature_entry.get().strip()
        vibration = vibration_entry.get().strip()
        operating_hours = operating_hours_entry.get().strip()

        # Check that the required fields are filled in
        if not equipment_name or not equipment_type or not equipment_location:
            messagebox.showwarning(
                "Missing Information",
                "Equipment Name, Type, and Location are required."
            )
            return

        # Check the readings and allow empty fields
        try:
            temperature = float(temperature) if temperature else None
            vibration = float(vibration) if vibration else None
            operating_hours = float(operating_hours) if operating_hours else None

        except ValueError:
            messagebox.showwarning(
                "Invalid Input",
                "Temperature, Vibration, and Operating Hours must be numbers."
            )
            return

        # Get the latest equipment ID
        with open("id_counters.json", "r") as file:
            counters = json.load(file)

        next_number = counters["last_equipment_id"] + 1
        equipment_id = f"EQ{next_number:03d}"

        # Check that the ID is not already in use
        with open("equipment_data.json", "r") as file:
            saved_equipment = json.load(file)

        existing_ids = {equipment["id"] for equipment in saved_equipment}

        while equipment_id in existing_ids:
            next_number += 1
            equipment_id = f"EQ{next_number:03d}"

        # Put the equipment details together
        new_equipment = {
            "id": equipment_id,
            "name": equipment_name,
            "type": equipment_type,
            "location": equipment_location,
            "temperature": temperature,
            "vibration": vibration,
            "operating_hours": operating_hours
        }

        # Add the new equipment to the JSON file
        saved_equipment.append(new_equipment)

        with open("equipment_data.json", "w") as file:
            json.dump(saved_equipment, file, indent=4)

        # Save the latest equipment ID
        counters["last_equipment_id"] = next_number

        with open("id_counters.json", "w") as file:
            json.dump(counters, file, indent=4)

        # Keep the equipment list up to date
        equipment_list.clear()
        equipment_list.extend(saved_equipment)

        # Add the equipment to the table
        equipment_table.insert("", tk.END, values=(
            equipment_id,
            equipment_name,
            equipment_type,
            equipment_location,
            temperature,
            vibration,
            operating_hours
        ))

        # Show a message when the equipment is saved
        messagebox.showinfo(
            "Success",
            f"Equipment {equipment_id} registered successfully."
        )

        # Clear the fields for the next entry
        for entry in (
            name_entry,
            type_entry,
            location_entry,
            temperature_entry,
            vibration_entry,
            operating_hours_entry
        ):
            entry.delete(0, tk.END)

    # Save the equipment details when clicked
    save_equipment_button = tk.Button(
        add_equipment_frame,
        text="Save Equipment",
        font=("Arial", 12),
        command=save_equipment
    )
    save_equipment_button.grid(row=4, column=1, pady=15)

    def show_add_equipment_form():
        add_equipment_frame.pack(pady=10)

    add_equipment_button = tk.Button(
        equipment_window,
        text="Add Equipment",
        font=("Arial", 12),
        command=show_add_equipment_form
    )
    add_equipment_button.pack(pady=10)

def open_work_order_window():
    work_order_window = tk.Toplevel(root)
    work_order_window.title("Work Orders")
    work_order_window.geometry("800x500")

    work_order_heading = tk.Label(
        work_order_window,
        text="Work Orders",
        font=("Arial", 16, "bold")
    )
    work_order_heading.pack(pady=20)

def open_schedule_window():
    schedule_window = tk.Toplevel(root)
    schedule_window.title("Maintenance Scheduling")
    schedule_window.geometry("800x500")

    schedule_heading = tk.Label(
        schedule_window,
        text="Maintenance Schedule",
        font=("Arial", 16, "bold")
    )
    schedule_heading.pack(pady=20)

def open_history_window():
    history_window = tk.Toplevel(root)
    history_window.title("Maintenance History")
    history_window.geometry("800x500")

    history_heading = tk.Label(
        history_window,
        text="Maintenance History",
        font=("Arial", 16, "bold")
    )
    history_heading.pack(pady=20)

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