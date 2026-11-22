#AI PLUGIN WAS USED TO REVIEW THE CODE BLOCKS

# Import the tools for building the GUI, reading JSON files and showing messages
import tkinter as tk
import json
from tkinter import ttk, messagebox
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Load equipment records that were saved previously
with open("equipment_data.json", "r") as file:
    equipment_list = json.load(file)

# Retrieve the saved ID counters to avoid reusing previous IDs
with open("id_counters.json", "r") as file:
    id_counters = json.load(file)

# Load the existing maintenance work orders
with open("work_orders.json", "r") as file:
    work_order_list = json.load(file)

# Retrieve the saved preventive maintenance schedules
with open("maintenance_schedule.json", "r") as file:
    maintenance_schedule_list = json.load(file)

# Load the equipment maintenance history records
with open("maintenance_history.json", "r") as file:
    maintenance_history_list = json.load(file)

# Set up the main application window and its dimensions
root = tk.Tk()
root.title("Mechanical Maintenance Management System")
root.geometry("900x600")


def open_equipment_window():
    # Open a separate window for managing equipment records
    equipment_window = tk.Toplevel(root)
    equipment_window.title("Equipment Management")
    equipment_window.geometry("1000x650")

    equipment_heading = tk.Label(
        equipment_window,
        text="Equipment Records",
        font=("Arial", 16, "bold")
    )
    equipment_heading.pack(pady=15)

    # Define the equipment details that appear as table columns
    columns = (
        "ID", "Name", "Type", "Location",
        "Temperature", "Vibration", "Operating Hours"
    )

    # Keep the equipment table and scrollbar together in one frame
    table_frame = tk.Frame(equipment_window)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    # Create a table for displaying registered equipment
    equipment_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=10
    )

    # Set the heading, width and alignment of each table column
    for col in columns:
        equipment_table.heading(col, text=col)
        equipment_table.column(col, width=130, anchor="center")

    # Add a scrollbar for navigating the equipment records
    scrollbar = ttk.Scrollbar(
        table_frame,
        orient=tk.VERTICAL,
        command=equipment_table.yview
    )
    equipment_table.configure(yscrollcommand=scrollbar.set)

    equipment_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def display_equipment(records):
        # Clear existing rows before displaying the requested records
        for item in equipment_table.get_children():
            equipment_table.delete(item)

        # Insert equipment records with alternating row colours
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

    # Use alternating row colours to separate equipment records
    equipment_table.tag_configure("evenrow", background="#FFFFFF")
    equipment_table.tag_configure("oddrow", background="#C5D3E0")

    # Display all registered equipment when the window opens
    display_equipment(equipment_list)

    # Keep the equipment action buttons together on one row
    equipment_button_frame = tk.Frame(equipment_window)
    equipment_button_frame.pack(pady=10)

    # Reserve space for the selected equipment form
    form_container = tk.Frame(equipment_window)
    form_container.pack(fill=tk.X, padx=15, pady=5)

    # Prepare separate forms for equipment registration and searching
    add_equipment_frame = tk.Frame(form_container)
    search_equipment_frame = tk.Frame(form_container)
    update_equipment_frame = tk.Frame(form_container)
    delete_equipment_frame = tk.Frame(form_container)

    # Track the form that is currently visible
    active_form = None

    def show_form(frame):
        nonlocal active_form

        # Hide the current form before switching to another
        if active_form is not None:
            active_form.pack_forget()

        # Clicking the same button again hides its form
        if active_form == frame:
            active_form = None
        else:
            frame.pack(pady=10)
            active_form = frame

    def show_add_equipment_form():
        # Restore the full equipment table and toggle the registration form
        display_equipment(equipment_list)
        show_form(add_equipment_frame)

    def show_search_equipment_form():
        # Restore the full equipment table and toggle the search form
        display_equipment(equipment_list)
        show_form(search_equipment_frame)

    def show_update_equipment_form():
        # Restore the equipment list and open the update form
        display_equipment(equipment_list)
        show_form(update_equipment_frame)

    def show_delete_equipment_form():
        # Restore the equipment list and open the deletion form
        display_equipment(equipment_list)
        show_form(delete_equipment_frame)

    # Provide input fields for the equipment details
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
        # Read the entered details and remove unwanted spaces
        equipment_name = name_entry.get().strip().title()
        equipment_type = type_entry.get().strip().title()
        equipment_location = location_entry.get().strip().title()
        temperature = temperature_entry.get().strip()
        vibration = vibration_entry.get().strip()
        operating_hours = operating_hours_entry.get().strip()

        # Require a name, type and location before saving
        if not equipment_name or not equipment_type or not equipment_location:
            messagebox.showwarning(
                "Missing Information",
                "Equipment Name, Type, and Location are required."
            )
            return

        # Convert entered readings to numbers while allowing blank values
        try:
            temperature = float(temperature) if temperature else None
            vibration = float(vibration) if vibration else None
            operating_hours = float(operating_hours) if operating_hours else None

        # Warn the user when an equipment reading is not numeric
        except ValueError:
            messagebox.showwarning(
                "Invalid Input",
                "Temperature, Vibration, and Operating Hours must be numbers."
            )
            return

        # Read the latest counter before generating an equipment ID
        with open("id_counters.json", "r") as file:
            counters = json.load(file)

        next_number = counters["last_equipment_id"] + 1
        equipment_id = f"EQ{next_number:03d}"

        # Check saved equipment IDs to prevent duplicates
        with open("equipment_data.json", "r") as file:
            saved_equipment = json.load(file)

        existing_ids = {
            equipment["id"] for equipment in saved_equipment
        }

        # Increase the number until an unused equipment ID is available
        while equipment_id in existing_ids:
            next_number += 1
            equipment_id = f"EQ{next_number:03d}"

        # Store the new equipment details in a dictionary
        new_equipment = {
            "id": equipment_id,
            "name": equipment_name,
            "type": equipment_type,
            "location": equipment_location,
            "temperature": temperature,
            "vibration": vibration,
            "operating_hours": operating_hours
        }

        # Append the new record and save the updated equipment list
        saved_equipment.append(new_equipment)

        with open("equipment_data.json", "w") as file:
            json.dump(saved_equipment, file, indent=4)

        # Save the latest ID number for future registrations
        counters["last_equipment_id"] = next_number

        with open("id_counters.json", "w") as file:
            json.dump(counters, file, indent=4)

        # Synchronise the GUI equipment list with the saved records
        equipment_list.clear()
        equipment_list.extend(saved_equipment)

        # Refresh the table to show the newly registered equipment
        display_equipment(equipment_list)

        # Confirm successful equipment registration
        messagebox.showinfo(
            "Success",
            f"Equipment {equipment_id} registered successfully."
        )

        # Clear the form so another equipment record can be entered
        for entry in (
            name_entry,
            type_entry,
            location_entry,
            temperature_entry,
            vibration_entry,
            operating_hours_entry
        ):
            entry.delete(0, tk.END)

    # Connect the Save Equipment button to the registration function
    save_equipment_button = tk.Button(
        add_equipment_frame,
        text="Save Equipment",
        font=("Arial", 12),
        command=save_equipment
    )
    save_equipment_button.grid(row=4, column=1, pady=15)

    # Provide an entry field for searching by equipment ID
    search_label = tk.Label(
        search_equipment_frame,
        text="Enter Equipment ID",
        font=("Arial", 12)
    )
    search_label.grid(row=0, column=0, padx=10, pady=10)

    search_entry = tk.Entry(search_equipment_frame)
    search_entry.grid(row=0, column=1, padx=10, pady=10)

    def search_equipment():
        # Read the equipment ID entered for the search
        search_id = search_entry.get().strip()

        # Prevent a search when no equipment ID is provided
        if not search_id:
            messagebox.showwarning(
                "Missing Information",
                "Please enter an equipment ID."
            )
            return

        # Compare IDs without treating uppercase and lowercase letters differently
        for equipment in equipment_list:
            if equipment["id"].casefold() == search_id.casefold():

                # Show only the matching equipment record in the table
                display_equipment([equipment])
                return

        # Notify the user when the equipment ID cannot be found
        messagebox.showwarning(
            "Equipment Not Found",
            "Equipment not found. Please check the equipment ID."
        )

    # Run the equipment search when the Search button is clicked
    search_button = tk.Button(
        search_equipment_frame,
        text="Search",
        font=("Arial", 12),
        command=search_equipment
    )
    search_button.grid(row=0, column=2, padx=10, pady=10)

    
    # Create the form for finding equipment to update
    tk.Label(update_equipment_frame, text="Equipment ID").grid(
        row=0, column=0, padx=10, pady=5
    )
    update_id_entry = tk.Entry(update_equipment_frame)
    update_id_entry.grid(row=0, column=1, padx=10, pady=5)

    # Prepare entry boxes for the equipment details
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

        # Find the equipment without considering letter case
        for equipment in equipment_list:
            if equipment["id"].casefold() == search_id.casefold():
                selected_equipment = equipment
                break

        if selected_equipment is None:
            messagebox.showwarning("Not Found", "Equipment not found.")
            return

        # Display the existing details for editing
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

        # Validate the required text fields
        for field in ("name", "type", "location"):
            value = update_fields[field].get().strip().title()

            if not value:
                messagebox.showwarning(
                    "Missing Information",
                    "Equipment Name, Type, and Location are required."
                )
                return

            updated_values[field] = value

        # Validate numeric readings while allowing blank values
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

        # Reload the latest saved records before applying the update
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

        # Save the changes and refresh the GUI records
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

    # Set up the buttons for equipment management actions
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


    # Set up the form for deleting an equipment record
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

        # Read the latest equipment records before deletion
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

        # Check for records linked to the selected equipment
        with open("work_orders.json", "r") as file:
            saved_work_orders = json.load(file)

        with open("maintenance_schedule.json", "r") as file:
            saved_schedules = json.load(file)

        with open("maintenance_history.json", "r") as file:
            saved_history = json.load(file)

        equipment_id = equipment_to_delete["id"]

        # Identify any work orders linked to the equipment
        has_work_order = any(
            order["equipment_id"].casefold() == equipment_id.casefold()
            for order in saved_work_orders
        )

        # Identify any maintenance schedules linked to the equipment
        has_maintenance_schedule = any(
            schedule["equipment_id"].casefold() == equipment_id.casefold()
            for schedule in saved_schedules
        )

        # Identify any maintenance history linked to the equipment
        has_maintenance_history = any(
            history["equipment_id"].casefold() == equipment_id.casefold()
            for history in saved_history
        )

        # Prevent deletion if the equipment has related maintenance records
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

        # Ask for confirmation before permanently removing the record
        confirmation = messagebox.askyesno(
            "Confirm Deletion",
            f"Delete {equipment_to_delete['id']} - {equipment_to_delete['name']}?"
        )

        if not confirmation:
            return

        saved_equipment.remove(equipment_to_delete)

        # Save the remaining equipment records to JSON
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


def open_work_order_window():
    # Open the window for managing maintenance work orders
    work_order_window = tk.Toplevel(root)
    work_order_window.title("Work Orders")
    work_order_window.geometry("1200x650")

    tk.Label(
        work_order_window,
        text="Work Orders",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    # Set up the work order table
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

    # Add a scrollbar for viewing all work orders
    scrollbar = ttk.Scrollbar(
        table_frame,
        orient=tk.VERTICAL,
        command=work_order_table.yview
    )
    work_order_table.configure(yscrollcommand=scrollbar.set)

    work_order_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Use the same alternating colours as the equipment table
    work_order_table.tag_configure("evenrow", background="#FFFFFF")
    work_order_table.tag_configure("oddrow", background="#C5D3E0")

    def load_work_orders():
        # Read the latest work orders from JSON
        with open("work_orders.json", "r") as file:
            records = json.load(file)

        work_order_list.clear()
        work_order_list.extend(records)
        return records

    def display_work_orders(records):
        # Clear old rows before displaying the requested records
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
        # Reload all work orders and refresh the table
        display_work_orders(load_work_orders())

    refresh_work_orders()

    # Keep the work order action buttons together
    button_frame = tk.Frame(work_order_window)
    button_frame.pack(pady=10)

    # Show only one work order form at a time
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

    # Create the buttons for managing work orders
    # Work orders are already displayed automatically in the table
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
        # Create a labelled input field
        tk.Label(frame, text=label).grid(
            row=row, column=0, padx=10, pady=6, sticky="e"
        )
        entry = tk.Entry(frame, width=35)
        entry.grid(row=row, column=1, padx=10, pady=6)
        return entry

    def equipment_exists(equipment_id):
        # Confirm that the equipment is registered
        with open("equipment_data.json", "r") as file:
            records = json.load(file)

        return any(
            equipment["id"].casefold() == equipment_id.casefold()
            for equipment in records
        )

    def linked_history_exists(work_order_id):
        # Check whether a work order has maintenance history
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
        # Read and validate the work order details
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

        # Read the latest counter and generate an unused work order ID
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

        # Save the work order and its ID counter
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

    # ---------------- SEARCH WORK ORDER ----------------

    search_entry = add_field(search_frame, "Work Order ID", 0)

    def search_work_order_gui():
        # Search without considering uppercase or lowercase letters
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

                # Protect completed work orders with linked history
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

        # Validate all fields before changing the work order
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

        # Check again before saving to protect linked history
        if (
            selected_order["status"].casefold() == "completed"
            and linked_history_exists(selected_order["id"])
        ):
            messagebox.showwarning(
                "Update Not Allowed",
                "This completed work order has linked maintenance history."
            )
            return

        # Check whether this update completes the work order
        completing_order = (
            status == "Completed"
            and selected_order["status"].casefold() != "completed"
        )

        # Apply the validated changes
        selected_order.update({
            "fault_description": fault,
            "equipment_id": equipment_id,
            "priority": priority,
            "status": status
        })

        # Create maintenance history automatically when completed
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

            # Use the same history fields as main.py
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

        # Save the updated work order details
        with open("work_orders.json", "w") as file:
            json.dump(orders, file, indent=4)

        refresh_work_orders()
        selected_work_order_id = None

        messagebox.showinfo(
            "Success", "Work order updated successfully."
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

    # ---------------- DELETE WORK ORDER ----------------

    delete_id_entry = add_field(delete_frame, "Work Order ID", 0)

    def delete_work_order_gui():
        # Find the work order before attempting deletion
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

        # Do not delete work orders linked to maintenance history
        if linked_history_exists(order_to_delete["id"]):
            messagebox.showwarning(
                "Deletion Not Allowed",
                "Cannot delete this work order because it has "
                "linked maintenance history."
            )
            return

        # Ask for confirmation before permanently deleting
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

def open_schedule_window():
    # Open the maintenance scheduling window
    schedule_window = tk.Toplevel(root)
    schedule_window.title("Maintenance Scheduling")
    schedule_window.geometry("1000x650")

    tk.Label(
        schedule_window,
        text="Maintenance Scheduling",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    # Create the table to display maintenance schedules
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

    # Load and save maintenance schedules
    def load_schedules():
        with open("maintenance_schedule.json", "r") as file:
            return json.load(file)

    def save_schedules(records):
        with open("maintenance_schedule.json", "w") as file:
            json.dump(records, file, indent=4)

    # Determine the current maintenance status
    def maintenance_status(next_date):
        today = datetime.today().date()
        due_date = datetime.strptime(next_date, "%Y-%m-%d").date()

        if due_date < today:
            return "Overdue"
        elif due_date == today:
            return "Due Today"
        else:
            return "Upcoming"

    # Display maintenance schedules automatically
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

    # Check that equipment is registered
    def equipment_exists(equipment_id):
        with open("equipment_data.json", "r") as file:
            equipment_records = json.load(file)

        for equipment in equipment_records:
            if equipment["id"].casefold() == equipment_id.casefold():
                return True

        return False

    # Accept the six date formats supported by main.py
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

    # Calculate the next maintenance date
    def calculate_next_date(last_date, interval, unit):
        date = datetime.strptime(last_date, "%Y-%m-%d")

        if unit == "Days":
            next_date = date + timedelta(days=interval)
        elif unit == "Months":
            next_date = date + relativedelta(months=interval)
        else:
            next_date = date + relativedelta(years=interval)

        return next_date.strftime("%Y-%m-%d")

    # Validate maintenance schedule details
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

    # Create buttons and an area for the forms
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

    # Create labelled entry fields
    def add_field(frame, label, row):
        tk.Label(
            frame,
            text=label
        ).grid(row=row, column=0, padx=10, pady=6, sticky="e")

        entry = tk.Entry(frame, width=35)
        entry.grid(row=row, column=1, padx=10, pady=6)

        return entry

    # Create a dropdown for interval units
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

        # Generate the next schedule ID
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

        # Save schedule and counter
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

        # Clear the create form
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

                # Fill the form with existing details
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

        # Save changes together and recalculate next maintenance
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

        # Discard unsaved changes
        selected_schedule_id = None
        clear_update_form()
        refresh_schedules()

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

def open_history_window():
    # Open the maintenance history window
    history_window = tk.Toplevel(root)
    history_window.title("Maintenance History")
    history_window.geometry("800x500")

    history_heading = tk.Label(
        history_window,
        text="Maintenance History",
        font=("Arial", 16, "bold")
    )
    history_heading.pack(pady=20)


# Display the application name on the main window
heading = tk.Label(
    root,
    text="Mechanical Maintenance Management System",
    font=("Arial", 20, "bold")
)
heading.pack(pady=20)

# Provide navigation buttons for the four main sections
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

# Keep the GUI running until the window is closed
root.mainloop()
