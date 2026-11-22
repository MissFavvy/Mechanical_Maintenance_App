#AI PLUGIN WAS USED TO REVIEW THE CODE BLOCKS

# Import the tools for building the GUI, reading JSON files and showing messages
import tkinter as tk
import json
from tkinter import ttk, messagebox

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
    # Open the work order window
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
    # Open the maintenance scheduling window
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
