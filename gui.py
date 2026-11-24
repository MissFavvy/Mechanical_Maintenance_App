#AI PLUGIN WAS USED TO REVIEW THE CODE BLOCKS

# Importing the libraries needed for the GUI, JSON files and date calculations
import tkinter as tk
import json
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Loading previously saved equipment records
with open("equipment_data.json", "r") as file:
    equipment_list = json.load(file)

# Keeping track of the last used ID numbers to avoid repeating IDs
with open("id_counters.json", "r") as file:
    id_counters = json.load(file)

# Loading previously saved work orders
with open("work_orders.json", "r") as file:
    work_order_list = json.load(file)

# Loading previously saved maintenance schedules
with open("maintenance_schedule.json", "r") as file:
    maintenance_schedule_list = json.load(file)

# Loading previously saved maintenance history
with open("maintenance_history.json", "r") as file:
    maintenance_history_list = json.load(file)

# Creating the main application window with its title and size
root = tk.Tk()
root.title("Mechanical Maintenance Management System")
root.geometry("900x600")

def open_equipment_window():
    # Creating a separate window for equipment management
    equipment_window = tk.Toplevel(root)
    equipment_window.title("Equipment Management")
    equipment_window.geometry("1000x650")

    equipment_heading = tk.Label(
        equipment_window,
        text="Equipment Records",
        font=("Arial", 16, "bold")
    )
    equipment_heading.pack(pady=15)

    # Defining the column headings for the equipment table
    columns = (
        "ID", "Name", "Type", "Location",
        "Temperature", "Vibration", "Operating Hours"
    )

    # Keeping the table and scrollbar in the same frame
    table_frame = tk.Frame(equipment_window)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    # Creating a table for registered equipment
    equipment_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=10
    )

    # Setting the heading, width and alignment of each column
    for col in columns:
        equipment_table.heading(col, text=col)
        equipment_table.column(col, width=130, anchor="center")

    # Adding a scrollbar to view more equipment records
    scrollbar = ttk.Scrollbar(
        table_frame,
        orient=tk.VERTICAL,
        command=equipment_table.yview
    )
    equipment_table.configure(yscrollcommand=scrollbar.set)

    equipment_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def display_equipment(records):
        # Clearing the table to avoid displaying duplicate records
        for item in equipment_table.get_children():
            equipment_table.delete(item)

        # Displaying equipment records with alternating row colours
        for index, equipment in enumerate(records):
            row_tag = "evenrow" if index % 2 == 0 else "oddrow"

            equipment_table.insert("", tk.END, values=(
                equipment["id"],
                equipment["name"],
                equipment["type"],
                equipment["location"],
                "null" if equipment["temperature"] is None else equipment["temperature"],
                "null" if equipment["vibration"] is None else equipment["vibration"],
                "null" if equipment["operating_hours"] is None else equipment["operating_hours"]
            ), tags=(row_tag,))

    # Alternating row colours for better readability
    equipment_table.tag_configure("evenrow", background="#FFFFFF")
    equipment_table.tag_configure("oddrow", background="#C5D3E0")

    # Displaying all saved equipment when the window opens
    display_equipment(equipment_list)

    # Keeping the equipment buttons on the same row
    equipment_button_frame = tk.Frame(equipment_window)
    equipment_button_frame.pack(pady=10)

    # Creating a space for the selected form
    form_container = tk.Frame(equipment_window)
    form_container.pack(fill=tk.X, padx=15, pady=5)

    # Creating separate forms for adding, searching, updating and deleting equipment
    add_equipment_frame = tk.Frame(form_container)
    search_equipment_frame = tk.Frame(form_container)
    update_equipment_frame = tk.Frame(form_container)
    delete_equipment_frame = tk.Frame(form_container)

    # Keeping track of which form is currently open
    active_form = None

    def show_form(frame):
        nonlocal active_form

        # Hiding the current form before opening another
        if active_form is not None:
            active_form.pack_forget()

        # Clicking the same button again closes the form
        if active_form == frame:
            active_form = None
        else:
            frame.pack(pady=10)
            active_form = frame

    def show_add_equipment_form():
        # Displaying all equipment records before opening or closing the registration form
        display_equipment(equipment_list)
        show_form(add_equipment_frame)

    def show_search_equipment_form():
        # Displaying all equipment records before opening or closing the search form
        display_equipment(equipment_list)
        show_form(search_equipment_frame)

    def show_update_equipment_form():
        # Restoring the equipment list before showing the update form
        display_equipment(equipment_list)
        show_form(update_equipment_frame)

    def show_delete_equipment_form():
        # Restoring the equipment list before showing the deletion form
        display_equipment(equipment_list)
        show_form(delete_equipment_frame)

    # Creating input fields for entering equipment details
    name_label = tk.Label(
        add_equipment_frame,
        text="Equipment Name"
    )
    name_label.grid(row=0, column=0, padx=10, pady=5)

    name_entry = tk.Entry(add_equipment_frame)
    name_entry.grid(row=1, column=0, padx=10, pady=5)

    type_label = tk.Label(
        add_equipment_frame,
        text="Equipment Type"
    )
    type_label.grid(row=0, column=1, padx=10, pady=5)

    type_entry = tk.Entry(add_equipment_frame)
    type_entry.grid(row=1, column=1, padx=10, pady=5)

    location_label = tk.Label(
        add_equipment_frame,
        text="Equipment Location"
    )
    location_label.grid(row=0, column=2, padx=10, pady=5)

    location_entry = tk.Entry(add_equipment_frame)
    location_entry.grid(row=1, column=2, padx=10, pady=5)

    temperature_label = tk.Label(
        add_equipment_frame,
        text="Temperature"
    )
    temperature_label.grid(row=2, column=0, padx=10, pady=5)

    temperature_entry = tk.Entry(add_equipment_frame)
    temperature_entry.grid(row=3, column=0, padx=10, pady=5)

    vibration_label = tk.Label(
        add_equipment_frame,
        text="Vibration"
    )
    vibration_label.grid(row=2, column=1, padx=10, pady=5)

    vibration_entry = tk.Entry(add_equipment_frame)
    vibration_entry.grid(row=3, column=1, padx=10, pady=5)

    operating_hours_label = tk.Label(
        add_equipment_frame,
        text="Operating Hours"
    )
    operating_hours_label.grid(row=2, column=2, padx=10, pady=5)

    operating_hours_entry = tk.Entry(add_equipment_frame)
    operating_hours_entry.grid(row=3, column=2, padx=10, pady=5)

    def save_equipment():
        # Getting the entered details and removing extra spaces
        equipment_name = name_entry.get().strip().title()
        equipment_type = type_entry.get().strip().title()
        equipment_location = location_entry.get().strip().title()
        temperature = temperature_entry.get().strip()
        vibration = vibration_entry.get().strip()
        operating_hours = operating_hours_entry.get().strip()

        # Making sure the name, type and location are not left empty
        if not equipment_name or not equipment_type or not equipment_location:
            messagebox.showwarning(
                "Missing Information",
                "Equipment Name, Type, and Location are required."
            )
            return

        # Converting equipment readings to numbers and storing empty readings as None
        try:
            temperature = float(temperature) if temperature else None
            vibration = float(vibration) if vibration else None
            operating_hours = float(operating_hours) if operating_hours else None

        # Showing a warning when an invalid reading is entered
        except ValueError:
            messagebox.showwarning(
                "Invalid Input",
                "Temperature, Vibration, and Operating Hours must be numbers."
            )
            return

        # Loading the last used ID number before generating a new ID
        with open("id_counters.json", "r") as file:
            counters = json.load(file)

        next_number = counters["last_equipment_id"] + 1
        equipment_id = f"EQ{next_number:03d}"

        # Checking existing equipment IDs to avoid duplicates
        with open("equipment_data.json", "r") as file:
            saved_equipment = json.load(file)

        existing_ids = {
            equipment["id"] for equipment in saved_equipment
        }

        # Increasing the ID number until an unused ID is found
        while equipment_id in existing_ids:
            next_number += 1
            equipment_id = f"EQ{next_number:03d}"

        # Storing the new equipment details in a dictionary
        new_equipment = {
            "id": equipment_id,
            "name": equipment_name,
            "type": equipment_type,
            "location": equipment_location,
            "temperature": temperature,
            "vibration": vibration,
            "operating_hours": operating_hours
        }

        # Adding the new equipment to the list and saving it to the JSON file
        saved_equipment.append(new_equipment)

        with open("equipment_data.json", "w") as file:
            json.dump(saved_equipment, file, indent=4)

        # Saving the last used ID number for the next registration
        counters["last_equipment_id"] = next_number

        with open("id_counters.json", "w") as file:
            json.dump(counters, file, indent=4)

        # Updating the equipment list with the latest saved records
        equipment_list.clear()
        equipment_list.extend(saved_equipment)

        # Refreshing the table to display the newly registered equipment
        display_equipment(equipment_list)

        # Showing a message after the equipment has been saved successfully
        messagebox.showinfo(
            "Success",
            f"Equipment {equipment_id} registered successfully."
        )

        # Clearing the input fields for the next equipment registration
        for entry in (
            name_entry,
            type_entry,
            location_entry,
            temperature_entry,
            vibration_entry,
            operating_hours_entry
        ):
            entry.delete(0, tk.END)

    # Linking the Save Equipment button to the registration function
    save_equipment_button = tk.Button(
        add_equipment_frame,
        text="Save Equipment",
        font=("Arial", 12),
        command=save_equipment
    )
    save_equipment_button.grid(row=4, column=1, pady=15)

    # Clearing the entered equipment details without saving
    def cancel_equipment_registration():
        for entry in (
            name_entry,
            type_entry,
            location_entry,
            temperature_entry,
            vibration_entry,
            operating_hours_entry
        ):
            entry.delete(0, tk.END)

        display_equipment(equipment_list)
        show_form(add_equipment_frame)

        # Showing a message to confirm that no equipment was saved
        messagebox.showinfo(
            "Registration Canceled",
            "Registration canceled. No equipment was saved.",
            parent=equipment_window
        )

    tk.Button(
        add_equipment_frame,
        text="Cancel",
        font=("Arial", 12),
        command=cancel_equipment_registration
    ).grid(row=4, column=2, pady=15)

    # Creating an input field for the equipment ID to search for a specific equipment record
    search_label = tk.Label(
        search_equipment_frame,
        text="Enter Equipment ID",
        font=("Arial", 12)
    )
    search_label.grid(row=0, column=0, padx=10, pady=10)

    search_entry = tk.Entry(search_equipment_frame)
    search_entry.grid(row=0, column=1, padx=10, pady=10)

    def search_equipment():
        # Getting the equipment ID entered by the user
        search_id = search_entry.get().strip()

        # Checking that the equipment ID is not left empty
        if not search_id:
            messagebox.showwarning(
                "Missing Information",
                "Please enter an equipment ID."
            )
            return

        # Allowing both uppercase and lowercase letters when searching for equipment
        for equipment in equipment_list:
            if equipment["id"].casefold() == search_id.casefold():

                # Displaying only the equipment that matches the entered ID
                display_equipment([equipment])
                return

        # Showing a warning if the equipment is not found
        messagebox.showwarning(
            "Equipment Not Found",
            "Equipment not found. Please check the equipment ID."
        )

    # Linking the Search button to the equipment search function
    search_button = tk.Button(
        search_equipment_frame,
        text="Search",
        font=("Arial", 12),
        command=search_equipment
    )
    search_button.grid(row=0, column=2, padx=10, pady=10)

    # Clearing the search field and displaying all equipment records again
    def cancel_equipment_search():
        search_entry.delete(0, tk.END)
        display_equipment(equipment_list)
        show_form(search_equipment_frame)

    tk.Button(
        search_equipment_frame,
        text="Cancel",
        font=("Arial", 12),
        command=cancel_equipment_search
    ).grid(row=0, column=3, padx=10, pady=10)

    # Creating a form for updating equipment details
    tk.Label(update_equipment_frame, text="Equipment ID").grid(
        row=0, column=0, padx=10, pady=5
    )
    update_id_entry = tk.Entry(update_equipment_frame)
    update_id_entry.grid(row=0, column=1, padx=10, pady=5)

    # Creating input fields for the details that can be updated
    update_fields = {}
    field_names = [
        ("name", "Equipment Name"),
        ("type", "Equipment Type"),
        ("location", "Equipment Location"),
        ("temperature", "Temperature"),
        ("vibration", "Vibration"),
        ("operating_hours", "Operating Hours")
    ]

    for row_number, (field, label_text) in enumerate(field_names, start=1):
        tk.Label(update_equipment_frame, text=label_text).grid(
            row=row_number, column=0, padx=10, pady=5
        )
        entry = tk.Entry(update_equipment_frame)
        entry.grid(row=row_number, column=1, padx=10, pady=5)
        update_fields[field] = entry

    selected_equipment = None

    def find_equipment_to_update():
        nonlocal selected_equipment

        search_id = update_id_entry.get().strip()
        selected_equipment = None

        for entry in update_fields.values():
            entry.delete(0, tk.END)

        if not search_id:
            messagebox.showwarning("Missing Information", "Enter an equipment ID.")
            return

        # Allowing both uppercase and lowercase letters when finding equipment to update
        for equipment in equipment_list:
            if equipment["id"].casefold() == search_id.casefold():
                selected_equipment = equipment
                break

        if selected_equipment is None:
            messagebox.showwarning("Not Found", "Equipment not found.")
            return

        # Filling the input fields with the previously saved equipment details
        for field, entry in update_fields.items():
            value = selected_equipment[field]
            entry.insert(0, "" if value is None else str(value))

        display_equipment([selected_equipment])

    def save_equipment_update():
        nonlocal selected_equipment

        if selected_equipment is None:
            messagebox.showwarning("Missing Information", "Find equipment first.")
            return

        updated_values = {}

        # Checking that the name, type and location are not left empty
        for field in ("name", "type", "location"):
            value = update_fields[field].get().strip().title()

            if not value:
                messagebox.showwarning(
                    "Missing Information",
                    "Equipment Name, Type, and Location are required."
                )
                return

            updated_values[field] = value

        # Checking that the readings are numbers and storing empty readings as None
        for field in ("temperature", "vibration", "operating_hours"):
            value = update_fields[field].get().strip()

            try:
                updated_values[field] = float(value) if value else None
            except ValueError:
                messagebox.showwarning(
                    "Invalid Input",
                    "Temperature, Vibration, and Operating Hours must be numbers."
                )
                return

        # Loading the latest equipment records before saving changes
        with open("equipment_data.json", "r") as file:
            saved_equipment = json.load(file)

        equipment_found = False

        for equipment in saved_equipment:
            if equipment["id"].casefold() == selected_equipment["id"].casefold():
                equipment.update(updated_values)
                equipment_found = True
                break

        if not equipment_found:
            messagebox.showwarning("Not Found", "Equipment no longer exists.")
            selected_equipment = None
            return

        # Saving the updated details to JSON and refreshing the equipment table
        with open("equipment_data.json", "w") as file:
            json.dump(saved_equipment, file, indent=4)

        equipment_list.clear()
        equipment_list.extend(saved_equipment)
        display_equipment(equipment_list)

        messagebox.showinfo("Success", "Equipment updated successfully.")
        selected_equipment = None

    tk.Button(
        update_equipment_frame,
        text="Find Equipment",
        command=find_equipment_to_update
    ).grid(row=0, column=2, padx=10)

    tk.Button(
        update_equipment_frame,
        text="Save Changes",
        command=save_equipment_update
    ).grid(row=7, column=1, pady=10)

    # Clearing the entered changes without saving them
    def cancel_equipment_update():
        nonlocal selected_equipment

        selected_equipment = None
        update_id_entry.delete(0, tk.END)

        for entry in update_fields.values():
            entry.delete(0, tk.END)

        display_equipment(equipment_list)
        show_form(update_equipment_frame)

        # Showing a message to confirm that no changes were saved
        messagebox.showinfo(
            "Update Canceled",
            "Update canceled. No changes were saved.",
            parent=equipment_window
        )

    tk.Button(
        update_equipment_frame,
        text="Cancel",
        command=cancel_equipment_update
    ).grid(row=7, column=2, padx=10, pady=10)

    # Creating the buttons for adding, searching, updating and deleting equipment
    add_equipment_button = tk.Button(
        equipment_button_frame,
        text="Add Equipment",
        font=("Arial", 12),
        width=17,
        command=show_add_equipment_form
    )
    add_equipment_button.pack(side=tk.LEFT, padx=5)

    search_equipment_button = tk.Button(
        equipment_button_frame,
        text="Search Equipment",
        font=("Arial", 12),
        width=17,
        command=show_search_equipment_form
    )
    search_equipment_button.pack(side=tk.LEFT, padx=5)

    update_equipment_button = tk.Button(
        equipment_button_frame,
        text="Update Equipment",
        font=("Arial", 12),
        width=17,
        command=show_update_equipment_form
    )
    update_equipment_button.pack(side=tk.LEFT, padx=5)

    delete_equipment_button = tk.Button(
        equipment_button_frame,
        text="Delete Equipment",
        font=("Arial", 12),
        width=17,
        command=show_delete_equipment_form
    )
    delete_equipment_button.pack(side=tk.LEFT, padx=5)


    # Creating a form for deleting equipment
    tk.Label(delete_equipment_frame, text="Equipment ID").grid(
        row=0, column=0, padx=10, pady=10
    )

    delete_id_entry = tk.Entry(delete_equipment_frame)
    delete_id_entry.grid(row=0, column=1, padx=10, pady=10)

    def delete_equipment():
        delete_id = delete_id_entry.get().strip()

        if not delete_id:
            messagebox.showwarning("Missing Information", "Enter an equipment ID.")
            return

        # Loading the latest saved equipment records before deletion
        with open("equipment_data.json", "r") as file:
            saved_equipment = json.load(file)

        equipment_to_delete = None

        for equipment in saved_equipment:
            if equipment["id"].casefold() == delete_id.casefold():
                equipment_to_delete = equipment
                break

        if equipment_to_delete is None:
            messagebox.showwarning("Not Found", "Equipment not found.")
            return

        # Checking for maintenance records linked to the selected equipment
        with open("work_orders.json", "r") as file:
            saved_work_orders = json.load(file)

        with open("maintenance_schedule.json", "r") as file:
            saved_schedules = json.load(file)

        with open("maintenance_history.json", "r") as file:
            saved_history = json.load(file)

        equipment_id = equipment_to_delete["id"]

        # Checking if the equipment has any existing work orders
        has_work_order = any(
            order["equipment_id"].casefold() == equipment_id.casefold()
            for order in saved_work_orders
        )

        # Checking if the equipment has any existing maintenance schedules
        has_maintenance_schedule = any(
            schedule["equipment_id"].casefold() == equipment_id.casefold()
            for schedule in saved_schedules
        )

        # Checking if the equipment has any existing maintenance history
        has_maintenance_history = any(
            history["equipment_id"].casefold() == equipment_id.casefold()
            for history in saved_history
        )

        # Preventing equipment deletion when there are linked maintenance records
        if has_work_order or has_maintenance_schedule or has_maintenance_history:
            reasons = []

            if has_work_order:
                reasons.append("Existing work order")

            if has_maintenance_schedule:
                reasons.append("Existing maintenance schedule")

            if has_maintenance_history:
                reasons.append("Existing maintenance history")

            messagebox.showwarning(
                "Deletion Not Allowed",
                "This equipment cannot be deleted because it has:\n\n"
                + "\n".join(reasons)
            )
            return

        # Asking the user to confirm before permanently deleting the equipment
        confirmation = messagebox.askyesno(
            "Confirm Deletion",
            f"Delete {equipment_to_delete['id']} - {equipment_to_delete['name']}?"
        )

        if not confirmation:
            return

        saved_equipment.remove(equipment_to_delete)

        # Saving the remaining equipment records to the JSON file
        with open("equipment_data.json", "w") as file:
            json.dump(saved_equipment, file, indent=4)

        equipment_list.clear()
        equipment_list.extend(saved_equipment)
        display_equipment(equipment_list)

        delete_id_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Equipment deleted successfully.")

    tk.Button(
        delete_equipment_frame,
        text="Delete Equipment",
        command=delete_equipment
    ).grid(row=1, column=1, pady=10)

    # Canceling the deletion and displaying all equipment records again
    def cancel_equipment_deletion():
        delete_id_entry.delete(0, tk.END)
        display_equipment(equipment_list)
        show_form(delete_equipment_frame)

        # Showing a message to confirm that no equipment was deleted
        messagebox.showinfo(
            "Deletion Canceled",
            "Deletion canceled. No equipment was deleted.",
            parent=equipment_window
        )

    tk.Button(
        delete_equipment_frame,
        text="Cancel",
        command=cancel_equipment_deletion
    ).grid(row=1, column=2, padx=10, pady=10)

def open_work_order_window():
    # Creating a separate window for managing work orders
    work_order_window = tk.Toplevel(root)
    work_order_window.title("Work Orders")
    work_order_window.geometry("1200x650")

    tk.Label(
        work_order_window,
        text="Work Orders",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    # Creating a table to display work order details
    columns = (
        "Work Order ID", "Equipment ID", "Fault Description",
        "Priority", "Status"
    )

    table_frame = tk.Frame(work_order_window)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    work_order_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=8
    )

    for column in columns:
        work_order_table.heading(column, text=column)
        work_order_table.column(column, width=180, anchor="center")

    # Adding a scrollbar to view more work orders
    scrollbar = ttk.Scrollbar(
        table_frame,
        orient=tk.VERTICAL,
        command=work_order_table.yview
    )
    work_order_table.configure(yscrollcommand=scrollbar.set)

    work_order_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Maintaining the same row colours as the equipment table
    work_order_table.tag_configure("evenrow", background="#FFFFFF")
    work_order_table.tag_configure("oddrow", background="#C5D3E0")

    def load_work_orders():
        # Loading the latest saved work orders from the JSON file
        with open("work_orders.json", "r") as file:
            records = json.load(file)

        work_order_list.clear()
        work_order_list.extend(records)
        return records

    def display_work_orders(records):
        # Clearing the table to avoid displaying duplicate records
        for item in work_order_table.get_children():
            work_order_table.delete(item)

        for index, order in enumerate(records):
            row_tag = "evenrow" if index % 2 == 0 else "oddrow"

            work_order_table.insert("", tk.END, values=(
                order["id"],
                order["equipment_id"],
                order["fault_description"],
                order["priority"],
                order["status"]
            ), tags=(row_tag,))

    def refresh_work_orders():
        # Refreshing the table with the latest saved work orders
        display_work_orders(load_work_orders())

    refresh_work_orders()

    # Keeping the work order buttons on the same row
    button_frame = tk.Frame(work_order_window)
    button_frame.pack(pady=10)

    # Displaying only one work order form at a time
    form_container = tk.Frame(work_order_window)
    form_container.pack(fill=tk.X, padx=15, pady=5)

    create_frame = tk.Frame(form_container)
    search_frame = tk.Frame(form_container)
    update_frame = tk.Frame(form_container)
    delete_frame = tk.Frame(form_container)

    active_form = None

    def show_form(frame):
        nonlocal active_form

        if active_form is not None:
            active_form.pack_forget()

        if active_form == frame:
            active_form = None
        else:
            frame.pack(pady=10)
            active_form = frame

    def show_create_form():
        refresh_work_orders()
        show_form(create_frame)

    def show_search_form():
        refresh_work_orders()
        show_form(search_frame)

    def show_update_form():
        refresh_work_orders()
        show_form(update_frame)

    def show_delete_form():
        refresh_work_orders()
        show_form(delete_frame)

    # Creating the buttons for managing work orders
    # All saved work orders are displayed when the window opens
    actions = (
        ("Create Work Order", show_create_form),
        ("Search Work Order", show_search_form),
        ("Update Work Order", show_update_form),
        ("Delete Work Order", show_delete_form)
    )

    for label, action in actions:
        tk.Button(
            button_frame,
            text=label,
            command=action,
            width=19,
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=4)

    def add_field(frame, label, row):
        # Creating reusable input fields with their labels
        tk.Label(frame, text=label).grid(
            row=row, column=0, padx=10, pady=6, sticky="e"
        )
        entry = tk.Entry(frame, width=35)
        entry.grid(row=row, column=1, padx=10, pady=6)
        return entry

    def equipment_exists(equipment_id):
        # Checking that the equipment is already registered
        with open("equipment_data.json", "r") as file:
            records = json.load(file)

        return any(
            equipment["id"].casefold() == equipment_id.casefold()
            for equipment in records
        )

    def linked_history_exists(work_order_id):
        # Checking if the work order has linked maintenance history
        with open("maintenance_history.json", "r") as file:
            records = json.load(file)

        return any(
            isinstance(history.get("work_order_id"), str)
            and history["work_order_id"].casefold() == work_order_id.casefold()
            for history in records
        )

    # ---------------- CREATE WORK ORDER ----------------

    fault_entry = add_field(create_frame, "Fault Description", 0)
    equipment_entry = add_field(create_frame, "Equipment ID", 1)

    tk.Label(create_frame, text="Priority").grid(
        row=2, column=0, padx=10, pady=6
    )

    priority_choice = ttk.Combobox(
        create_frame,
        values=("Low", "Medium", "High"),
        state="readonly",
        width=32
    )
    priority_choice.grid(row=2, column=1, padx=10, pady=6)

    def create_work_order_gui():
        # Getting the entered work order details and checking for missing information
        fault = fault_entry.get().strip()
        equipment_id = equipment_entry.get().strip().upper()
        priority = priority_choice.get().strip()

        if not fault or not equipment_id or not priority:
            messagebox.showwarning(
                "Missing Information",
                "Fault Description, Equipment ID and Priority are required."
            )
            return

        if not equipment_exists(equipment_id):
            messagebox.showwarning(
                "Invalid Equipment",
                "Equipment ID not found. Enter a registered equipment ID."
            )
            return

        # Generating a new work order ID without repeating existing IDs
        with open("id_counters.json", "r") as file:
            counters = json.load(file)

        orders = load_work_orders()
        next_number = counters["last_work_order_id"] + 1
        work_order_id = f"WO{next_number:03d}"

        existing_ids = {order["id"].casefold() for order in orders}

        while work_order_id.casefold() in existing_ids:
            next_number += 1
            work_order_id = f"WO{next_number:03d}"

        # Every new work order starts with Pending status
        new_order = {
            "id": work_order_id,
            "fault_description": fault,
            "equipment_id": equipment_id,
            "priority": priority,
            "status": "Pending"
        }

        orders.append(new_order)
        counters["last_work_order_id"] = next_number

        # Saving the new work order and the last used ID number
        with open("work_orders.json", "w") as file:
            json.dump(orders, file, indent=4)

        with open("id_counters.json", "w") as file:
            json.dump(counters, file, indent=4)

        refresh_work_orders()

        messagebox.showinfo(
            "Success",
            f"Work Order {work_order_id} created successfully."
        )

        fault_entry.delete(0, tk.END)
        equipment_entry.delete(0, tk.END)
        priority_choice.set("")

    tk.Button(
        create_frame,
        text="Save Work Order",
        command=create_work_order_gui
    ).grid(row=3, column=1, pady=12)

    # Clearing the entered work order details without saving
    def cancel_work_order_creation():
        fault_entry.delete(0, tk.END)
        equipment_entry.delete(0, tk.END)
        priority_choice.set("")

        refresh_work_orders()
        show_form(create_frame)

        # Showing a message to confirm that no work order was saved
        messagebox.showinfo(
            "Creation Canceled",
            "Creation canceled. No work order was saved.",
            parent=work_order_window
        )

    tk.Button(
        create_frame,
        text="Cancel",
        command=cancel_work_order_creation
    ).grid(row=3, column=2, padx=10, pady=12)

    # ---------------- SEARCH WORK ORDER ----------------

    search_entry = add_field(search_frame, "Work Order ID", 0)

    def search_work_order_gui():
        # Allowing both uppercase and lowercase letters when searching for a work order
        search_id = search_entry.get().strip()

        if not search_id:
            messagebox.showwarning(
                "Missing Information", "Enter a work order ID."
            )
            return

        for order in load_work_orders():
            if order["id"].casefold() == search_id.casefold():
                display_work_orders([order])
                return

        messagebox.showwarning(
            "Not Found", "Work order not found. Check the work order ID."
        )

    tk.Button(
        search_frame,
        text="Search",
        command=search_work_order_gui
    ).grid(row=1, column=1, pady=10)

    # Clearing the search field and displaying all work orders again
    def cancel_work_order_search():
        search_entry.delete(0, tk.END)
        refresh_work_orders()
        show_form(search_frame)

    tk.Button(
        search_frame,
        text="Cancel",
        command=cancel_work_order_search
    ).grid(row=1, column=2, padx=10, pady=10)

    # ---------------- UPDATE WORK ORDER ----------------

    update_id_entry = add_field(update_frame, "Work Order ID", 0)

    update_fields = {}
    update_labels = (
        ("fault_description", "Fault Description"),
        ("equipment_id", "Equipment ID")
    )

    for row, (field, label) in enumerate(update_labels, start=1):
        update_fields[field] = add_field(update_frame, label, row)

    tk.Label(update_frame, text="Priority").grid(
        row=3, column=0, padx=10, pady=6
    )
    update_priority = ttk.Combobox(
        update_frame,
        values=("Low", "Medium", "High"),
        state="readonly",
        width=32
    )
    update_priority.grid(row=3, column=1, padx=10, pady=6)

    tk.Label(update_frame, text="Status").grid(
        row=4, column=0, padx=10, pady=6
    )
    update_status = ttk.Combobox(
        update_frame,
        values=("Pending", "In Progress", "Completed"),
        state="readonly",
        width=32
    )
    update_status.grid(row=4, column=1, padx=10, pady=6)

    selected_work_order_id = None

    def find_work_order_to_update():
        nonlocal selected_work_order_id

        selected_work_order_id = None
        search_id = update_id_entry.get().strip()

        if not search_id:
            messagebox.showwarning(
                "Missing Information", "Enter a work order ID."
            )
            return

        for order in load_work_orders():
            if order["id"].casefold() == search_id.casefold():

                # Preventing changes to completed work orders with linked maintenance history
                if (
                    order["status"].casefold() == "completed"
                    and linked_history_exists(order["id"])
                ):
                    messagebox.showwarning(
                        "Update Not Allowed",
                        "This completed work order has linked maintenance "
                        "history and cannot be updated."
                    )
                    return

                selected_work_order_id = order["id"]

                for field, entry in update_fields.items():
                    entry.delete(0, tk.END)
                    entry.insert(0, order[field])

                update_priority.set(order["priority"])
                update_status.set(order["status"])
                display_work_orders([order])
                return

        messagebox.showwarning("Not Found", "Work order not found.")

    def save_work_order_update():
        nonlocal selected_work_order_id

        if selected_work_order_id is None:
            messagebox.showwarning(
                "Missing Information", "Find a work order first."
            )
            return

        fault = update_fields["fault_description"].get().strip()
        equipment_id = update_fields["equipment_id"].get().strip().upper()
        priority = update_priority.get().strip()
        status = update_status.get().strip()

        # Checking that all required details have been entered before saving changes
        if not fault or not equipment_id or not priority or not status:
            messagebox.showwarning(
                "Missing Information", "All work order fields are required."
            )
            return

        if not equipment_exists(equipment_id):
            messagebox.showwarning(
                "Invalid Equipment", "Equipment ID not found."
            )
            return

        if priority not in ("Low", "Medium", "High"):
            messagebox.showwarning(
                "Invalid Priority", "Select Low, Medium or High."
            )
            return

        if status not in ("Pending", "In Progress", "Completed"):
            messagebox.showwarning(
                "Invalid Status", "Select a valid work order status."
            )
            return

        orders = load_work_orders()
        selected_order = None

        for order in orders:
            if order["id"].casefold() == selected_work_order_id.casefold():
                selected_order = order
                break

        if selected_order is None:
            messagebox.showwarning(
                "Not Found", "This work order no longer exists."
            )
            selected_work_order_id = None
            return

        # Checking again for linked maintenance history before saving changes
        if (
            selected_order["status"].casefold() == "completed"
            and linked_history_exists(selected_order["id"])
        ):
            messagebox.showwarning(
                "Update Not Allowed",
                "This completed work order has linked maintenance history."
            )
            return

        # Checking if the work order status is being changed to Completed
        completing_order = (
            status == "Completed"
            and selected_order["status"].casefold() != "completed"
        )

        # Updating the work order with the checked details
        selected_order.update({
            "fault_description": fault,
            "equipment_id": equipment_id,
            "priority": priority,
            "status": status
        })

        history_id = None

        # Automatically creating a maintenance history record when a work order is completed
        if completing_order and not linked_history_exists(selected_order["id"]):
            with open("maintenance_history.json", "r") as file:
                history_records = json.load(file)

            with open("id_counters.json", "r") as file:
                counters = json.load(file)

            next_number = counters["last_history_id"] + 1
            history_id = f"MH{next_number:03d}"

            existing_ids = {
                history["id"].casefold() for history in history_records
            }

            while history_id.casefold() in existing_ids:
                next_number += 1
                history_id = f"MH{next_number:03d}"

            # Maintaining the same maintenance history structure as main.py
            history_records.append({
                "id": history_id,
                "work_order_id": selected_order["id"],
                "equipment_id": selected_order["equipment_id"],
                "maintenance_date": datetime.today().strftime("%Y-%m-%d"),
                "work_performed": "",
                "parts_replaced": "",
                "fault_description": selected_order["fault_description"],
                "maintenance_cost_currency": None,
                "maintenance_cost": None
            })

            counters["last_history_id"] = next_number

            with open("maintenance_history.json", "w") as file:
                json.dump(history_records, file, indent=4)

            with open("id_counters.json", "w") as file:
                json.dump(counters, file, indent=4)

        # Saving the updated work order details to the JSON file
        with open("work_orders.json", "w") as file:
            json.dump(orders, file, indent=4)

        refresh_work_orders()
        selected_work_order_id = None

        # Informing the user when a maintenance history record has been created automatically
        if history_id is not None:
            messagebox.showinfo(
                "Success",
                "Work order updated successfully.\n\n"
                f"Maintenance history {history_id} was created automatically.\n\n"
                "Go to Update Maintenance History to enter the work performed, "
                "parts replaced, maintenance cost and currency.",
                parent=work_order_window
            )
        else:
            messagebox.showinfo(
                "Success",
                "Work order updated successfully.",
                parent=work_order_window
            )

    tk.Button(
        update_frame,
        text="Find Work Order",
        command=find_work_order_to_update
    ).grid(row=0, column=2, padx=10)

    tk.Button(
        update_frame,
        text="Save Changes",
        command=save_work_order_update
    ).grid(row=5, column=1, pady=12)

    # Clearing the entered work order changes without saving
    def cancel_work_order_update():
        nonlocal selected_work_order_id

        selected_work_order_id = None
        update_id_entry.delete(0, tk.END)

        for entry in update_fields.values():
            entry.delete(0, tk.END)

        update_priority.set("")
        update_status.set("")

        refresh_work_orders()
        show_form(update_frame)

        # Showing a message to confirm that no changes were saved
        messagebox.showinfo(
            "Update Canceled",
            "Update canceled. No changes were saved.",
            parent=work_order_window
        )

    tk.Button(
        update_frame,
        text="Cancel",
        command=cancel_work_order_update
    ).grid(row=5, column=2, padx=10, pady=12)

    # ---------------- DELETE WORK ORDER ----------------

    delete_id_entry = add_field(delete_frame, "Work Order ID", 0)

    def delete_work_order_gui():
        # Finding the work order that matches the entered ID
        delete_id = delete_id_entry.get().strip()

        if not delete_id:
            messagebox.showwarning(
                "Missing Information", "Enter a work order ID."
            )
            return

        orders = load_work_orders()
        order_to_delete = None

        for order in orders:
            if order["id"].casefold() == delete_id.casefold():
                order_to_delete = order
                break

        if order_to_delete is None:
            messagebox.showwarning("Not Found", "Work order not found.")
            return

        # Preventing deletion of work orders with linked maintenance history
        if linked_history_exists(order_to_delete["id"]):
            messagebox.showwarning(
                "Deletion Not Allowed",
                "Cannot delete this work order because it has "
                "linked maintenance history."
            )
            return

        # Asking the user to confirm before permanently deleting the work order
        confirmation = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete {order_to_delete['id']}?"
        )

        if not confirmation:
            return

        orders.remove(order_to_delete)

        with open("work_orders.json", "w") as file:
            json.dump(orders, file, indent=4)

        refresh_work_orders()
        delete_id_entry.delete(0, tk.END)

        messagebox.showinfo(
            "Success", "Work order deleted successfully."
        )

    tk.Button(
        delete_frame,
        text="Delete Work Order",
        command=delete_work_order_gui
    ).grid(row=1, column=1, pady=10)

    # Canceling the deletion without removing the work order
    def cancel_work_order_deletion():
        delete_id_entry.delete(0, tk.END)

        # Displaying all work orders again and closing the deletion form
        refresh_work_orders()
        show_form(delete_frame)

        # Showing a message to confirm that no work order was deleted
        messagebox.showinfo(
            "Deletion Canceled",
            "Deletion canceled. No work order was deleted.",
            parent=work_order_window
        )

    tk.Button(
        delete_frame,
        text="Cancel",
        command=cancel_work_order_deletion
    ).grid(row=1, column=2, padx=10, pady=10)

def open_schedule_window():
    # Creating a separate window for maintenance scheduling
    schedule_window = tk.Toplevel(root)
    schedule_window.title("Maintenance Scheduling")
    schedule_window.geometry("1000x650")

    tk.Label(
        schedule_window,
        text="Maintenance Scheduling",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    # Creating a table for displaying maintenance schedules
    columns = (
        "Schedule ID",
        "Equipment ID",
        "Maintenance Task",
        "Last Maintenance",
        "Interval",
        "Next Maintenance",
        "Status"
    )

    table_frame = tk.Frame(schedule_window)
    table_frame.pack(fill=tk.BOTH, padx=15, pady=10)

    schedule_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=9
    )

    widths = (105, 110, 250, 135, 125, 135, 110)

    for column, width in zip(columns, widths):
        schedule_table.heading(column, text=column)
        schedule_table.column(column, width=width, anchor="center")

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient=tk.VERTICAL,
        command=schedule_table.yview
    )

    schedule_table.configure(yscrollcommand=scrollbar.set)
    schedule_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    schedule_table.tag_configure("evenrow", background="#FFFFFF")
    schedule_table.tag_configure("oddrow", background="#C5D3E0")

    # Loading and saving maintenance schedules using JSON files
    def load_schedules():
        with open("maintenance_schedule.json", "r") as file:
            return json.load(file)

    def save_schedules(records):
        with open("maintenance_schedule.json", "w") as file:
            json.dump(records, file, indent=4)

    # Comparing the next maintenance date with today's date to determine its status
    def maintenance_status(next_date):
        today = datetime.today().date()
        due_date = datetime.strptime(next_date, "%Y-%m-%d").date()

        if due_date < today:
            return "Overdue"
        elif due_date == today:
            return "Due Today"
        else:
            return "Upcoming"

    # Displaying saved maintenance schedules in the table
    def display_schedules(records):
        for item in schedule_table.get_children():
            schedule_table.delete(item)

        for index, schedule in enumerate(records):
            row_tag = "evenrow" if index % 2 == 0 else "oddrow"

            schedule_table.insert(
                "",
                tk.END,
                values=(
                    schedule["id"],
                    schedule["equipment_id"],
                    schedule["maintenance_task"],
                    schedule["last_maintenance_date"],
                    f'{schedule["maintenance_interval"]} {schedule["interval_unit"]}',
                    schedule["next_maintenance_date"],
                    maintenance_status(schedule["next_maintenance_date"])
                ),
                tags=(row_tag,)
            )

    def refresh_schedules():
        display_schedules(load_schedules())

    refresh_schedules()

    # Checking that the equipment is already registered
    def equipment_exists(equipment_id):
        with open("equipment_data.json", "r") as file:
            equipment_records = json.load(file)

        for equipment in equipment_records:
            if equipment["id"].casefold() == equipment_id.casefold():
                return True

        return False

    # Allowing the same six date formats as main.py
    def validate_date(value):
        date_formats = (
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%m-%d-%Y",
            "%Y/%m/%d",
            "%d/%m/%Y",
            "%m/%d/%Y"
        )

        for date_format in date_formats:
            try:
                date = datetime.strptime(value, date_format)
                return date.strftime("%Y-%m-%d")
            except ValueError:
                continue

        return None

    # Calculating the next maintenance date based on the selected interval and unit
    def calculate_next_date(last_date, interval, unit):
        date = datetime.strptime(last_date, "%Y-%m-%d")

        if unit == "Days":
            next_date = date + timedelta(days=interval)
        elif unit == "Months":
            next_date = date + relativedelta(months=interval)
        else:
            next_date = date + relativedelta(years=interval)

        return next_date.strftime("%Y-%m-%d")

    # Checking the entered maintenance details before saving
    def validate_schedule(task, date_text, interval_text, unit):
        if not task or not date_text or not interval_text or not unit:
            messagebox.showwarning(
                "Missing Information",
                "All maintenance schedule fields are required.",
                parent=schedule_window
            )
            return None

        last_date = validate_date(date_text)

        if last_date is None:
            messagebox.showwarning(
                "Invalid Date",
                "Enter a valid maintenance date.",
                parent=schedule_window
            )
            return None

        try:
            interval = int(interval_text)

            if interval <= 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Invalid Interval",
                "Maintenance interval must be a whole number greater than zero.",
                parent=schedule_window
            )
            return None

        if unit not in ("Days", "Months", "Years"):
            messagebox.showwarning(
                "Invalid Unit",
                "Select Days, Months or Years.",
                parent=schedule_window
            )
            return None

        next_date = calculate_next_date(last_date, interval, unit)

        return last_date, interval, next_date

    # Creating a space for the buttons and maintenance schedule forms
    button_frame = tk.Frame(schedule_window)
    button_frame.pack(pady=10)

    form_container = tk.Frame(schedule_window)
    form_container.pack(fill=tk.X, padx=15, pady=5)

    create_frame = tk.Frame(form_container)
    search_frame = tk.Frame(form_container)
    update_frame = tk.Frame(form_container)
    delete_frame = tk.Frame(form_container)

    active_form = None

    def show_form(frame):
        nonlocal active_form

        if active_form is not None:
            active_form.pack_forget()

        if active_form == frame:
            active_form = None
        else:
            frame.pack(pady=10)
            active_form = frame

    def show_create_form():
        refresh_schedules()
        show_form(create_frame)

    def show_search_form():
        refresh_schedules()
        show_form(search_frame)

    def show_update_form():
        refresh_schedules()
        show_form(update_frame)

    def show_delete_form():
        refresh_schedules()
        show_form(delete_frame)

    actions = (
        ("Create Schedule", show_create_form),
        ("Search Schedule", show_search_form),
        ("Update Schedule", show_update_form),
        ("Delete Schedule", show_delete_form)
    )

    for label, action in actions:
        tk.Button(
            button_frame,
            text=label,
            command=action,
            width=19,
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)

    # Creating reusable input fields with their labels
    def add_field(frame, label, row):
        tk.Label(
            frame,
            text=label
        ).grid(row=row, column=0, padx=10, pady=6, sticky="e")

        entry = tk.Entry(frame, width=35)
        entry.grid(row=row, column=1, padx=10, pady=6)

        return entry

    # Providing a dropdown for selecting Days, Months or Years
    def add_unit_field(frame, row):
        tk.Label(
            frame,
            text="Interval Unit"
        ).grid(row=row, column=0, padx=10, pady=6, sticky="e")

        choice = ttk.Combobox(
            frame,
            values=("Days", "Months", "Years"),
            state="readonly",
            width=32
        )

        choice.grid(row=row, column=1, padx=10, pady=6)
        return choice

    # ---------------- CREATE MAINTENANCE SCHEDULE ----------------

    create_equipment = add_field(create_frame, "Equipment ID", 0)
    create_task = add_field(create_frame, "Maintenance Task", 1)
    create_date = add_field(create_frame, "Last Maintenance Date", 2)
    create_unit = add_unit_field(create_frame, 3)
    create_interval = add_field(create_frame, "Maintenance Interval", 4)

    def create_schedule_gui():
        equipment_id = create_equipment.get().strip().upper()
        task = create_task.get().strip()
        date_text = create_date.get().strip()
        interval_text = create_interval.get().strip()
        unit = create_unit.get().strip()

        if equipment_id == "":
            messagebox.showwarning(
                "Missing Information",
                "Equipment ID cannot be empty.",
                parent=schedule_window
            )
            return

        if not equipment_exists(equipment_id):
            messagebox.showwarning(
                "Invalid Equipment",
                "Equipment ID not found. Enter a registered equipment ID.",
                parent=schedule_window
            )
            return

        validated = validate_schedule(
            task, date_text, interval_text, unit
        )

        if validated is None:
            return

        last_date, interval, next_date = validated

        # Generating a new maintenance schedule ID without repeating existing IDs
        with open("id_counters.json", "r") as file:
            counters = json.load(file)

        schedules = load_schedules()

        next_number = counters["last_schedule_id"] + 1
        schedule_id = f"MS{next_number:03d}"

        existing_ids = {
            schedule["id"].casefold() for schedule in schedules
        }

        while schedule_id.casefold() in existing_ids:
            next_number += 1
            schedule_id = f"MS{next_number:03d}"

        new_schedule = {
            "id": schedule_id,
            "equipment_id": equipment_id,
            "maintenance_task": task,
            "last_maintenance_date": last_date,
            "maintenance_interval": interval,
            "interval_unit": unit,
            "next_maintenance_date": next_date
        }

        schedules.append(new_schedule)
        counters["last_schedule_id"] = next_number

        # Saving the maintenance schedule and the last used ID number
        save_schedules(schedules)

        with open("id_counters.json", "w") as file:
            json.dump(counters, file, indent=4)

        refresh_schedules()

        messagebox.showinfo(
            "Success",
            f"Schedule {schedule_id} created successfully.\n"
            f"Next maintenance date: {next_date}",
            parent=schedule_window
        )

        # Clearing the input fields for the next maintenance schedule
        create_equipment.delete(0, tk.END)
        create_task.delete(0, tk.END)
        create_date.delete(0, tk.END)
        create_interval.delete(0, tk.END)
        create_unit.set("")

    tk.Button(
        create_frame,
        text="Save Schedule",
        command=create_schedule_gui
    ).grid(row=5, column=1, pady=12)

    # Clearing the entered maintenance schedule details without saving
    def cancel_schedule_creation():
        for entry in (
            create_equipment,
            create_task,
            create_date,
            create_interval
        ):
            entry.delete(0, tk.END)

        create_unit.set("")

        # Displaying all saved schedules again and closing the form
        refresh_schedules()
        show_form(create_frame)

        # Showing a message to confirm that no maintenance schedule was saved
        messagebox.showinfo(
            "Creation Canceled",
            "Creation canceled. No schedule was saved.",
            parent=schedule_window
        )

    tk.Button(
        create_frame,
        text="Cancel",
        command=cancel_schedule_creation
    ).grid(row=5, column=2, padx=10, pady=12)

    # ---------------- SEARCH MAINTENANCE SCHEDULE ----------------

    search_entry = add_field(search_frame, "Schedule ID", 0)

    def search_schedule_gui():
        search_id = search_entry.get().strip()

        if search_id == "":
            messagebox.showwarning(
                "Missing Information",
                "Enter a schedule ID.",
                parent=schedule_window
            )
            return

        schedules = load_schedules()

        for schedule in schedules:
            if schedule["id"].casefold() == search_id.casefold():
                display_schedules([schedule])
                return

        messagebox.showwarning(
            "Not Found",
            "Maintenance schedule not found. Check the schedule ID.",
            parent=schedule_window
        )

    tk.Button(
        search_frame,
        text="Search",
        command=search_schedule_gui
    ).grid(row=1, column=1, pady=10)

    # Clearing the search field and displaying all maintenance schedules again
    def cancel_schedule_search():
        search_entry.delete(0, tk.END)
        refresh_schedules()
        show_form(search_frame)

    tk.Button(
        search_frame,
        text="Cancel",
        command=cancel_schedule_search
    ).grid(row=1, column=2, padx=10, pady=10)

    # ---------------- UPDATE MAINTENANCE SCHEDULE ----------------

    update_id = add_field(update_frame, "Schedule ID", 0)
    update_task = add_field(update_frame, "Maintenance Task", 1)
    update_date = add_field(update_frame, "Last Maintenance Date", 2)
    update_unit = add_unit_field(update_frame, 3)
    update_interval = add_field(update_frame, "Maintenance Interval", 4)

    selected_schedule_id = None

    def clear_update_form():
        update_id.delete(0, tk.END)
        update_task.delete(0, tk.END)
        update_date.delete(0, tk.END)
        update_interval.delete(0, tk.END)
        update_unit.set("")

    def find_schedule_to_update():
        nonlocal selected_schedule_id

        selected_schedule_id = None
        schedule_id = update_id.get().strip()

        if schedule_id == "":
            messagebox.showwarning(
                "Missing Information",
                "Enter a schedule ID.",
                parent=schedule_window
            )
            return

        schedules = load_schedules()

        for schedule in schedules:
            if schedule["id"].casefold() == schedule_id.casefold():
                selected_schedule_id = schedule["id"]

                # Filling the input fields with the previously saved maintenance details
                update_task.delete(0, tk.END)
                update_task.insert(0, schedule["maintenance_task"])

                update_date.delete(0, tk.END)
                update_date.insert(0, schedule["last_maintenance_date"])

                update_interval.delete(0, tk.END)
                update_interval.insert(
                    0, str(schedule["maintenance_interval"])
                )

                update_unit.set(schedule["interval_unit"])
                display_schedules([schedule])
                return

        messagebox.showwarning(
            "Not Found",
            "Maintenance schedule not found.",
            parent=schedule_window
        )

    def save_schedule_update():
        nonlocal selected_schedule_id

        if selected_schedule_id is None:
            messagebox.showwarning(
                "Missing Information",
                "Find a schedule first.",
                parent=schedule_window
            )
            return

        task = update_task.get().strip()
        date_text = update_date.get().strip()
        interval_text = update_interval.get().strip()
        unit = update_unit.get().strip()

        validated = validate_schedule(
            task, date_text, interval_text, unit
        )

        if validated is None:
            return

        last_date, interval, next_date = validated

        schedules = load_schedules()
        selected_schedule = None

        for schedule in schedules:
            if schedule["id"].casefold() == selected_schedule_id.casefold():
                selected_schedule = schedule
                break

        if selected_schedule is None:
            messagebox.showwarning(
                "Not Found",
                "This maintenance schedule no longer exists.",
                parent=schedule_window
            )
            selected_schedule_id = None
            return

        # Saving the updated schedule details along with the recalculated maintenance date
        selected_schedule["maintenance_task"] = task
        selected_schedule["last_maintenance_date"] = last_date
        selected_schedule["maintenance_interval"] = interval
        selected_schedule["interval_unit"] = unit
        selected_schedule["next_maintenance_date"] = next_date

        save_schedules(schedules)
        refresh_schedules()

        selected_schedule_id = None
        clear_update_form()

        messagebox.showinfo(
            "Success",
            "Maintenance schedule updated successfully.\n"
            f"Next maintenance date: {next_date}",
            parent=schedule_window
        )

    def cancel_schedule_update():
        nonlocal selected_schedule_id

        # Clearing the entered changes without saving them
        selected_schedule_id = None
        clear_update_form()

        # Displaying all maintenance schedules again and closing the update form
        refresh_schedules()
        show_form(update_frame)

        messagebox.showinfo(
            "Update Canceled",
            "Update canceled. No changes were saved.",
            parent=schedule_window
        )

    tk.Button(
        update_frame,
        text="Find Schedule",
        command=find_schedule_to_update
    ).grid(row=0, column=2, padx=10)

    tk.Button(
        update_frame,
        text="Save Changes",
        command=save_schedule_update
    ).grid(row=5, column=1, pady=12)

    tk.Button(
        update_frame,
        text="Cancel",
        command=cancel_schedule_update
    ).grid(row=5, column=2, padx=10, pady=12)

    # ---------------- DELETE MAINTENANCE SCHEDULE ----------------

    delete_id = add_field(delete_frame, "Schedule ID", 0)

    def delete_schedule_gui():
        schedule_id = delete_id.get().strip()

        if schedule_id == "":
            messagebox.showwarning(
                "Missing Information",
                "Enter a schedule ID.",
                parent=schedule_window
            )
            return

        schedules = load_schedules()
        selected_schedule = None

        for schedule in schedules:
            if schedule["id"].casefold() == schedule_id.casefold():
                selected_schedule = schedule
                break

        if selected_schedule is None:
            messagebox.showwarning(
                "Not Found",
                "Maintenance schedule not found.",
                parent=schedule_window
            )
            return

        confirmation = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete {selected_schedule['id']}?",
            parent=schedule_window
        )

        if not confirmation:
            return

        schedules.remove(selected_schedule)
        save_schedules(schedules)
        refresh_schedules()

        delete_id.delete(0, tk.END)

        messagebox.showinfo(
            "Success",
            "Maintenance schedule deleted successfully.",
            parent=schedule_window
        )

    tk.Button(
        delete_frame,
        text="Delete Schedule",
        command=delete_schedule_gui
    ).grid(row=1, column=1, pady=10)

    # Canceling the deletion without removing the maintenance schedule
    def cancel_schedule_deletion():
        delete_id.delete(0, tk.END)

        # Displaying all maintenance schedules again and closing the deletion form
        refresh_schedules()
        show_form(delete_frame)

        # Showing a message to confirm that no maintenance schedule was deleted
        messagebox.showinfo(
            "Deletion Canceled",
            "Deletion canceled. No schedule was deleted.",
            parent=schedule_window
        )

    tk.Button(
        delete_frame,
        text="Cancel",
        command=cancel_schedule_deletion
    ).grid(row=1, column=2, padx=10, pady=10)

def open_history_window():
    # Creating a separate window for maintenance history
    history_window = tk.Toplevel(root)
    history_window.title("Maintenance History")
    history_window.geometry("2000x850")

    tk.Label(
        history_window,
        text="Maintenance History",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    # Creating a table for displaying maintenance history records
    columns = (
        "History ID",
        "Work Order ID",
        "Equipment ID",
        "Maintenance Date",
        "Fault Description",
        "Work Performed",
        "Parts Replaced",
        "Currency",
        "Cost"
    )

    table_frame = tk.Frame(history_window)
    table_frame.pack(fill=tk.BOTH, padx=15, pady=10)

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=9
    )

    widths = (100, 110, 110, 130, 200, 230, 170, 90, 110)

    for column, width in zip(columns, widths):
        table.heading(column, text=column)
        table.column(column, width=width, anchor="center")

    vertical_scrollbar = ttk.Scrollbar(
        table_frame,
        orient=tk.VERTICAL,
        command=table.yview
    )

    horizontal_scrollbar = ttk.Scrollbar(
        table_frame,
        orient=tk.HORIZONTAL,
        command=table.xview
    )

    table.configure(
        yscrollcommand=vertical_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set
    )

    table.grid(row=0, column=0, sticky="nsew")
    vertical_scrollbar.grid(row=0, column=1, sticky="ns")
    horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

    table_frame.columnconfigure(0, weight=1)
    table_frame.rowconfigure(0, weight=1)

    table.tag_configure("evenrow", background="#FFFFFF")
    table.tag_configure("oddrow", background="#C5D3E0")

    # Loading previously saved maintenance history records from the JSON file
    def load_history():
        with open("maintenance_history.json", "r") as file:
            return json.load(file)

    # Saving maintenance history records to the JSON file
    def save_history(records):
        with open("maintenance_history.json", "w") as file:
            json.dump(records, file, indent=4)

    # Displaying maintenance history records in the table
    def display_history(records):
        for item in table.get_children():
            table.delete(item)

        for index, history in enumerate(records):
            row_tag = "evenrow" if index % 2 == 0 else "oddrow"

            work_order_id = history.get("work_order_id")
            if not work_order_id:
                work_order_id = "N/A"

            currency = history.get("maintenance_cost_currency")
            cost = history.get("maintenance_cost")

            if cost is None:
                cost_display = "Not recorded"
            else:
                cost_display = str(cost)

            if currency is None:
                currency_display = "N/A"
            else:
                currency_display = currency

            table.insert(
                "",
                tk.END,
                values=(
                    history["id"],
                    work_order_id,
                    history["equipment_id"],
                    history["maintenance_date"],
                    history.get("fault_description", ""),
                    history.get("work_performed", ""),
                    history.get("parts_replaced", ""),
                    currency_display,
                    cost_display
                ),
                tags=(row_tag,)
            )

    def refresh_history():
        display_history(load_history())

    refresh_history()

    # Checking whether the equipment ID exists in the saved equipment records
    def equipment_exists(equipment_id):
        with open("equipment_data.json", "r") as file:
            equipment_records = json.load(file)

        for equipment in equipment_records:
            if equipment["id"].casefold() == equipment_id.casefold():
                return True

        return False

    # Allowing the same six date formats as main.py
    def validate_date(date_text):
        date_formats = (
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%m-%d-%Y",
            "%Y/%m/%d",
            "%d/%m/%Y",
            "%m/%d/%Y"
        )

        for date_format in date_formats:
            try:
                date = datetime.strptime(date_text, date_format)
                return date.strftime("%Y-%m-%d")
            except ValueError:
                continue

        return None

    # Checking that the maintenance cost is a valid, finite and non-negative number
    def validate_cost(cost_text):
        try:
            cost = float(cost_text)

            if cost < 0 or not (-float("inf") < cost < float("inf")):
                raise ValueError

            return cost

        except ValueError:
            messagebox.showwarning(
                "Invalid Cost",
                "Maintenance cost must be a valid non-negative number.",
                parent=history_window
            )
            return None

    # Creating a space for the action buttons and maintenance history forms
    button_frame = tk.Frame(history_window)
    button_frame.pack(pady=10)

    form_container = tk.Frame(history_window)
    form_container.pack(fill=tk.X, padx=15, pady=5)

    search_frame = tk.Frame(form_container)
    update_frame = tk.Frame(form_container)
    delete_frame = tk.Frame(form_container)

    active_form = None

    def show_form(frame):
        nonlocal active_form

        if active_form is not None:
            active_form.pack_forget()

        if active_form == frame:
            active_form = None
        else:
            frame.pack(pady=10)
            active_form = frame

    def show_search_form():
        refresh_history()
        show_form(search_frame)

    def show_update_form():
        refresh_history()
        show_form(update_frame)

    def show_delete_form():
        refresh_history()
        show_form(delete_frame)

    actions = (
        ("Search History", show_search_form),
        ("Update History", show_update_form),
        ("Delete History", show_delete_form)
    )

    for label, action in actions:
        tk.Button(
            button_frame,
            text=label,
            command=action,
            width=19,
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)

    # Creating reusable input fields with their labels
    def add_field(frame, label, row):
        tk.Label(
            frame,
            text=label
        ).grid(row=row, column=0, padx=10, pady=5, sticky="e")

        entry = tk.Entry(frame, width=40)
        entry.grid(row=row, column=1, padx=10, pady=5)

        return entry

    # Providing a dropdown for selecting GBP, USD or NGN
    def add_currency_field(frame, row):
        tk.Label(
            frame,
            text="Maintenance Cost Currency"
        ).grid(row=row, column=0, padx=10, pady=5, sticky="e")

        currency = ttk.Combobox(
            frame,
            values=("GBP", "USD", "NGN"),
            state="readonly",
            width=37
        )

        currency.grid(row=row, column=1, padx=10, pady=5)
        return currency

    # ---------------- SEARCH MAINTENANCE HISTORY ----------------

    search_entry = add_field(search_frame, "History ID", 0)

    def search_history_gui():
        history_id = search_entry.get().strip()

        if history_id == "":
            messagebox.showwarning(
                "Missing Information",
                "Enter a maintenance history ID.",
                parent=history_window
            )
            return

        records = load_history()

        for history in records:
            if history["id"].casefold() == history_id.casefold():
                display_history([history])
                return

        messagebox.showwarning(
            "Not Found",
            "Maintenance history not found. Check the history ID.",
            parent=history_window
        )

    tk.Button(
        search_frame,
        text="Search",
        command=search_history_gui
    ).grid(row=1, column=1, pady=10)

    # Clearing the search field and displaying all maintenance history records again
    def cancel_history_search():
        search_entry.delete(0, tk.END)
        refresh_history()
        show_form(search_frame)

    tk.Button(
        search_frame,
        text="Cancel",
        command=cancel_history_search
    ).grid(row=1, column=2, padx=10, pady=10)

    # ---------------- UPDATE MAINTENANCE HISTORY ----------------

    update_id = add_field(update_frame, "History ID", 0)
    update_date = add_field(update_frame, "Maintenance Date", 1)
    update_fault = add_field(update_frame, "Fault Description", 2)
    update_work = add_field(update_frame, "Work Performed", 3)
    update_parts = add_field(update_frame, "Parts Replaced", 4)
    update_currency = add_currency_field(update_frame, 5)
    update_cost = add_field(update_frame, "Maintenance Cost", 6)

    selected_history_id = None

    def clear_update_form():
        for entry in (
            update_id,
            update_date,
            update_fault,
            update_work,
            update_parts,
            update_cost
        ):
            entry.delete(0, tk.END)

        update_currency.set("")

    def find_history_to_update():
        nonlocal selected_history_id

        selected_history_id = None
        history_id = update_id.get().strip()

        if history_id == "":
            messagebox.showwarning(
                "Missing Information",
                "Enter a maintenance history ID.",
                parent=history_window
            )
            return

        records = load_history()

        for history in records:
            if history["id"].casefold() == history_id.casefold():
                selected_history_id = history["id"]

                # Filling the update form with the previously saved maintenance history details
                fields = (
                    (update_date, history["maintenance_date"]),
                    (update_fault, history.get("fault_description", "")),
                    (update_work, history.get("work_performed", "")),
                    (update_parts, history.get("parts_replaced", ""))
                )

                for entry, value in fields:
                    entry.delete(0, tk.END)
                    entry.insert(0, value or "")

                currency = history.get("maintenance_cost_currency")
                update_currency.set(currency or "")

                cost = history.get("maintenance_cost")
                update_cost.delete(0, tk.END)

                if cost is not None:
                    update_cost.insert(0, str(cost))

                display_history([history])
                return

        messagebox.showwarning(
            "Not Found",
            "Maintenance history not found.",
            parent=history_window
        )

    def save_history_update():
        nonlocal selected_history_id

        if selected_history_id is None:
            messagebox.showwarning(
                "Missing Information",
                "Find a maintenance history record first.",
                parent=history_window
            )
            return

        date_text = update_date.get().strip()
        fault_description = update_fault.get().strip()
        work_performed = update_work.get().strip()
        parts_replaced = update_parts.get().strip()
        currency = update_currency.get().strip()
        cost_text = update_cost.get().strip()

        maintenance_date = validate_date(date_text)

        if maintenance_date is None:
            messagebox.showwarning(
                "Invalid Date",
                "Enter a valid maintenance date.",
                parent=history_window
            )
            return

        # Checking the existing maintenance history before updating its details
        # Allowing automatically created records to contain incomplete details
        records = load_history()
        selected_history = None

        for history in records:
            if history["id"].casefold() == selected_history_id.casefold():
                selected_history = history
                break

        if selected_history is None:
            messagebox.showwarning(
                "Not Found",
                "This maintenance history record no longer exists.",
                parent=history_window
            )
            selected_history_id = None
            return

        # Preventing an existing work description from being replaced with an empty value
        original_work = selected_history.get("work_performed", "")

        if work_performed == "" and original_work:
            messagebox.showwarning(
                "Missing Information",
                "Work description cannot be empty.",
                parent=history_window
            )
            return

        # Allowing maintenance costs to remain unrecorded until they are available
        if cost_text == "":
            if selected_history.get("maintenance_cost") is None:
                maintenance_cost = None
            else:
                messagebox.showwarning(
                    "Invalid Cost",
                    "Enter a valid maintenance cost.",
                    parent=history_window
                )
                return
        else:
            if currency not in ("GBP", "USD", "NGN"):
                messagebox.showwarning(
                    "Invalid Currency",
                    "Select a maintenance cost currency first.",
                    parent=history_window
                )
                return

            maintenance_cost = validate_cost(cost_text)

            if maintenance_cost is None:
                return

        if currency and currency not in ("GBP", "USD", "NGN"):
            messagebox.showwarning(
                "Invalid Currency",
                "Select GBP, USD or NGN.",
                parent=history_window
            )
            return

        # Saving all updated maintenance history details together
        selected_history["maintenance_date"] = maintenance_date
        selected_history["fault_description"] = fault_description
        selected_history["work_performed"] = work_performed
        selected_history["parts_replaced"] = parts_replaced
        selected_history["maintenance_cost_currency"] = currency or None
        selected_history["maintenance_cost"] = maintenance_cost

        save_history(records)
        refresh_history()

        selected_history_id = None
        clear_update_form()

        messagebox.showinfo(
            "Success",
            "Maintenance history updated successfully!",
            parent=history_window
        )

    def cancel_history_update():
        nonlocal selected_history_id

        # Clearing the entered changes without saving them
        selected_history_id = None
        clear_update_form()

        # Displaying all maintenance history records again and closing the update form
        refresh_history()
        show_form(update_frame)

        messagebox.showinfo(
            "Update Canceled",
            "Update canceled. No changes were saved.",
            parent=history_window
        )

    tk.Button(
        update_frame,
        text="Find History",
        command=find_history_to_update
    ).grid(row=0, column=2, padx=10)

    tk.Button(
        update_frame,
        text="Save Changes",
        command=save_history_update
    ).grid(row=7, column=1, pady=12)

    tk.Button(
        update_frame,
        text="Cancel",
        command=cancel_history_update
    ).grid(row=7, column=2, padx=10, pady=12)

    # ---------------- DELETE MAINTENANCE HISTORY ----------------

    delete_id = add_field(delete_frame, "History ID", 0)

    def delete_history_gui():
        history_id = delete_id.get().strip()

        if history_id == "":
            messagebox.showwarning(
                "Missing Information",
                "Enter a maintenance history ID.",
                parent=history_window
            )
            return

        records = load_history()
        selected_history = None

        for history in records:
            if history["id"].casefold() == history_id.casefold():
                selected_history = history
                break

        if selected_history is None:
            messagebox.showwarning(
                "Not Found",
                "Maintenance history not found.",
                parent=history_window
            )
            return

        # Preventing deletion of maintenance history linked to completed work orders
        work_order_id = selected_history.get("work_order_id")

        if work_order_id and str(work_order_id).lower() != "null":
            with open("work_orders.json", "r") as file:
                work_orders = json.load(file)

            for work_order in work_orders:
                if work_order["id"].casefold() == work_order_id.casefold():
                    if work_order["status"].casefold() == "completed":
                        messagebox.showwarning(
                            "Deletion Not Allowed",
                            "This maintenance history cannot be deleted "
                            "because it is linked to a completed work order.",
                            parent=history_window
                        )
                        return

        # Asking the user to confirm before deleting the maintenance history record
        confirmation = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete {selected_history['id']}?",
            parent=history_window
        )

        if not confirmation:
            return

        records.remove(selected_history)
        save_history(records)
        refresh_history()

        delete_id.delete(0, tk.END)

        messagebox.showinfo(
            "Success",
            "Maintenance history deleted successfully!",
            parent=history_window
        )

    tk.Button(
        delete_frame,
        text="Delete History",
        command=delete_history_gui
    ).grid(row=1, column=1, pady=10)

    # Canceling the deletion without removing the maintenance history record
    def cancel_history_deletion():
        delete_id.delete(0, tk.END)

        # Displaying all maintenance history records again and closing the deletion form
        refresh_history()
        show_form(delete_frame)

        messagebox.showinfo(
            "Deletion Canceled",
            "Deletion canceled. No record was deleted.",
            parent=history_window
        )

    tk.Button(
        delete_frame,
        text="Cancel",
        command=cancel_history_deletion
    ).grid(row=1, column=2, padx=10, pady=10)

# Displaying the application name at the top of the main window
heading = tk.Label(
    root,
    text="Mechanical Maintenance Management System",
    font=("Arial", 20, "bold")
)
heading.pack(pady=20)

# Creating navigation buttons for accessing the four main sections of the application
equipment_button = tk.Button(
    root,
    text="Equipment Management",
    font=("Arial", 14),
    command=open_equipment_window
)
equipment_button.pack(pady=10)

work_order_button = tk.Button(
    root,
    text="Work Orders",
    font=("Arial", 14),
    command=open_work_order_window
)
work_order_button.pack(pady=10)

schedule_button = tk.Button(
    root,
    text="Maintenance Scheduling",
    font=("Arial", 14),
    command=open_schedule_window
)
schedule_button.pack(pady=10)

history_button = tk.Button(
    root,
    text="Maintenance History",
    font=("Arial", 14),
    command=open_history_window
)
history_button.pack(pady=10)

# Keeping the application running until the main window is closed
root.mainloop()
