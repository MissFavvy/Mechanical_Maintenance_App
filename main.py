#AI PLUGIN WAS USED TO REVIEW THE CODE BLOCKS

# Importing the libraries needed for JSON storage and maintenance date calculations
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Loading previously saved equipment records
with open("equipment_data.json", "r") as file:
    equipment_list = json.load(file)

# Keeping track of the last used ID numbers
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

# Defining a custom exception for canceling an operation
class OperationCancelled(Exception):
    pass


# Checking for cancellation before processing the user's input
def operation_input(prompt):
    value = input(prompt)
    if value.strip().casefold() == "cancel":
        raise OperationCancelled
    return value


# Handling canceled operations and returning the user to the main menu
def cancellable(function):
    def run():
        print("Type cancel at any prompt to return to the main menu.")
        try:
            function()
        except OperationCancelled:
            print("Operation canceled. No changes were saved.")
    return run


# Displaying the new record for review before saving
def confirm_save(record):
    print("\nReview the new record:")
    print(record)
    while True:
        print("1. Save")
        print("2. Cancel")
        choice = operation_input("Enter your choice: ").strip()
        if choice == "1":
            return True
        if choice == "2":
            print("Operation canceled. No changes were saved.")
            return False
        print("Invalid choice. Please select 1 or 2.")


# Registering new equipment with a generated equipment ID
@cancellable
def add_new_equipment():
    # Generating the next ID without changing the counter until saving
    equipment_number = id_counters["last_equipment_id"] + 1

    equipment_id = f"EQ{equipment_number:03d}"

    print("Generated Equipment ID:", equipment_id)

    # Making sure the equipment name is not left empty
    while True:
        equipment_name = operation_input("Enter equipment name: ").strip().title()

        if equipment_name == "":
            print("Equipment name cannot be empty. Please try again.")
            continue
        break

    # Making sure the equipment type is not left empty
    while True:
        equipment_type = operation_input("Enter equipment type: ").strip().title()
        if equipment_type == "":
            print("Equipment type cannot be empty. Please try again.")
            continue
        break

    # Getting the equipment location and removing extra spaces
    while True:
        equipment_location = operation_input("Enter equipment location: ").strip().title()
        if equipment_location == "":
            print("Equipment location cannot be empty. Please try again.")
            continue
        break

    # Accepting numerical temperature readings or storing missing readings as None
    while True:
        temperature = operation_input("Enter equipment temperature (press Enter if unavailable): ")
        if temperature == "":
            temperature = None
            break
        else:
            try:
                temperature = float(temperature)
                break
            except ValueError:
                print("Invalid temperature. Please enter a number.")

    # Accepting numerical vibration readings or storing missing readings as None
    while True:
        vibration = operation_input("Enter equipment vibration (press Enter if unavailable): ")
        if vibration == "":
            vibration = None
            break
        else:
            try:
                vibration = float(vibration)
                break
            except ValueError:
                print("Invalid vibration. Please enter a number.")

    # Accepting numerical operating hours or storing missing readings as None
    while True:
        operating_hours = operation_input("Enter equipment operating hours (press Enter if unavailable): ")
        if operating_hours == "":
            operating_hours = None
            break
        else:
            try:
                operating_hours = float(operating_hours)
                break
            except ValueError:
                print("Invalid operating hours. Please enter a number.")

    # Storing the equipment details in a dictionary
    new_equipment = {
         "id": equipment_id,
         "name": equipment_name,
         "type": equipment_type,
         "location": equipment_location,
         "temperature": temperature,
         "vibration": vibration,
         "operating_hours": operating_hours
    }

    # Confirming the new equipment before saving the record and ID counter
    if not confirm_save(new_equipment):
        return

    id_counters["last_equipment_id"] = equipment_number
    equipment_list.append(new_equipment)

    with open("equipment_data.json", "w") as file:
        json.dump(equipment_list, file, indent=4)

    with open("id_counters.json", "w") as file:
        json.dump(id_counters, file, indent=4)

# Searching for equipment by ID regardless of letter case
@cancellable
def search_equipment():
    search_id = operation_input("Enter equipment ID to search: ").strip()
    found = False

    for equipment in equipment_list:
        if equipment["id"].casefold() == search_id.casefold():
            print("Equipment found!")
            print(equipment)
            found = True

    if found == False:
        print("Equipment not found. Please check the equipment ID.")

# Updating equipment details before saving the changes
@cancellable
def update_equipment_details():
    equipment_id = operation_input("Enter the equipment ID you want to update: ").strip()

    for equipment in equipment_list:
        if equipment["id"].casefold() == equipment_id.casefold():
            print("Equipment found!")
            print(equipment)

            # Using a copy to keep the original equipment details unchanged until saving
            updated_equipment = equipment.copy()

            while True:
                print("\nWhat would you like to update?")
                print("1. Equipment Name")
                print("2. Equipment Type")
                print("3. Equipment Location")
                print("4. Temperature")
                print("5. Vibration")
                print("6. Operating Hours")
                print("7. Save Changes")
                print("8. Cancel")

                choice = operation_input("Enter your choice: ").strip()

                if choice in ["1", "2", "3"]:
                    # Checking that the required equipment text fields are not empty
                    fields = {
                        "1": ("name", "equipment name"),
                        "2": ("type", "equipment type"),
                        "3": ("location", "equipment location")
                    }

                    field, field_name = fields[choice]

                    while True:
                        new_value = operation_input(
                            f"Enter new {field_name}: "
                        ).strip()

                        if new_value == "":
                            print(f"{field_name.title()} cannot be empty.")
                            continue

                        updated_equipment[field] = new_value.title()
                        break

                elif choice in ["4", "5", "6"]:
                    # Storing missing readings as None and converting other entries to numbers
                    fields = {
                        "4": ("temperature", "temperature"),
                        "5": ("vibration", "vibration"),
                        "6": ("operating_hours", "operating hours")
                    }

                    field, field_name = fields[choice]

                    while True:
                        new_value = operation_input(
                            f"Enter new {field_name} (press Enter if unavailable): "
                        ).strip()

                        if new_value == "":
                            updated_equipment[field] = None
                            break

                        try:
                            updated_equipment[field] = float(new_value)
                            break

                        except ValueError:
                            print(f"Invalid {field_name}. Please enter a number.")

                elif choice == "7":
                    # Saving all equipment changes together in the JSON file
                    equipment.update(updated_equipment)

                    with open("equipment_data.json", "w") as file:
                        json.dump(equipment_list, file, indent=4)

                    print("Equipment details updated successfully!")
                    return

                elif choice == "8":
                    # Leaving the original equipment record unchanged when canceled
                    print("Update canceled. No changes were saved.")
                    return

                else:
                    print("Invalid choice. Please select 1 to 8.")

                print("\nCurrent changes:")
                print(updated_equipment)

            return

    print("Equipment not found. Please check the equipment ID.")   

# Checking for linked maintenance records before allowing equipment deletion
@cancellable
def delete_equipment():
    equipment_id = operation_input("Enter the equipment ID you want to delete: ").strip()
    found = False

    for equipment in equipment_list:
        if equipment["id"].casefold() == equipment_id.casefold():
            found = True
            print("Equipment found!")
            print(equipment)

            # Keeping track of work orders, schedules and history linked to the equipment
            has_work_order = False
            has_maintenance_schedule = False
            has_maintenance_history = False

            for work_order in work_order_list:
                if work_order["equipment_id"].casefold() == equipment["id"].casefold():
                    has_work_order = True
                    break

            for schedule in maintenance_schedule_list:
                if schedule["equipment_id"].casefold() == equipment["id"].casefold():
                    has_maintenance_schedule = True
                    break

            for history in maintenance_history_list:
                if history["equipment_id"].casefold() == equipment["id"].casefold():
                    has_maintenance_history = True
                    break

            # Preventing equipment deletion when linked maintenance records exist
            if has_work_order or has_maintenance_schedule or has_maintenance_history:
                print("This equipment cannot be deleted because:")

                if has_work_order:
                    print("- It has an existing work order.")

                if has_maintenance_schedule:
                    print("- It has an existing maintenance schedule.")

                if has_maintenance_history:
                    print("- It has an existing maintenance history.")

                return

            # Asking for confirmation before deleting the equipment
            confirmation = operation_input("Are you sure you want to delete this equipment? (yes/no): ")

            if confirmation.strip().lower() == "yes":
                equipment_list.remove(equipment)

                with open("equipment_data.json", "w") as file:
                    json.dump(equipment_list, file, indent=4)

                print("Equipment deleted successfully!")
            else:
                print("Deletion canceled.")

            break

    if found == False:
        print("Equipment not found. Please check the equipment ID.")


# Creating a work order for equipment that needs maintenance
@cancellable
def create_work_order():
    # Generating the next work order ID without changing the counter until saving
    work_order_number = id_counters["last_work_order_id"] + 1

    work_order_id = f"WO{work_order_number:03d}"

    print("Generated Work Order ID:", work_order_id)
    
    # Making sure the fault description is not left empty
    while True:
        fault_description = operation_input("Enter fault description: ").strip()
        if fault_description == "":
            print("Fault description cannot be empty. Please try again.")
            continue
        break

    # Checking that the equipment is registered before assigning a work order
    while True:
        equipment_id = operation_input("Enter equipment ID for the work order: ").strip().upper()
        if equipment_id == "":
            print("Equipment ID cannot be empty. Please try again.")
            continue
        found = False
        for equipment in equipment_list:
            if equipment["id"].casefold() == equipment_id.casefold():
                found = True
                break
        if found:
            break
        else:
            print("Equipment ID not found. Please enter a valid equipment ID.")

    # Accepting Low, Medium or High as the maintenance priority
    while True:
        priority = operation_input("Enter maintenance priority (Low/Medium/High): ").strip().title()
        if priority == "":
            print("Maintenance priority cannot be empty. Please try again.")
            continue
        if priority.casefold() not in ["low", "medium", "high"]:
            print("Invalid priority. Please enter Low, Medium, or High.")
            continue
        break

    # Setting the initial work order status to Pending
    status = "Pending"

    work_order = {
        "id": work_order_id,
        "fault_description": fault_description,
        "equipment_id": equipment_id,
        "priority": priority,
        "status": status
    }
    
    # Confirming and saving the new work order and its ID counter
    if not confirm_save(work_order):
        return

    id_counters["last_work_order_id"] = work_order_number
    work_order_list.append(work_order)

    with open("work_orders.json", "w") as file:
        json.dump(work_order_list, file, indent=4)

    with open("id_counters.json", "w") as file:
        json.dump(id_counters, file, indent=4)

# Searching for a work order using its ID
@cancellable
def search_work_order():
    search_id = operation_input("Enter work order ID to search: ").strip()
    found = False

    # Matching work order IDs regardless of letter case
    for work_order in work_order_list:
        if work_order["id"].casefold() == search_id.casefold():
            print("Work order found!")
            print(work_order)
            found = True

    if found == False:
        print("Work order not found. Please check the work order ID.")


# Automatically creating maintenance history when a work order is completed
def create_automatic_maintenance_history(work_order):
    # Checking for existing linked history to avoid duplicate records
    for history in maintenance_history_list:
        if (history.get("work_order_id") or "").casefold() == work_order["id"].casefold():
            print("Maintenance history already exists for this work order.")
            return

    # Generating a new maintenance history ID
    id_counters["last_history_id"] += 1

    history_number = id_counters["last_history_id"]

    history_id = f"MH{history_number:03d}"

    # Creating the history record using details from the completed work order
    maintenance_record = {
        "id": history_id,
        "work_order_id": work_order["id"],
        "equipment_id": work_order["equipment_id"].upper(),
        "maintenance_date": datetime.today().strftime("%Y-%m-%d"),
        "work_performed": "",
        "parts_replaced": "",
        "fault_description": work_order["fault_description"],
        "maintenance_cost_currency": None,
        "maintenance_cost": None
    }

    # Saving the history record and the last used history ID
    maintenance_history_list.append(maintenance_record)

    with open("maintenance_history.json", "w") as file:
        json.dump(maintenance_history_list, file, indent=4)

    with open("id_counters.json", "w") as file:
        json.dump(id_counters, file, indent=4)

    print("Maintenance history automatically created!")
    print("History ID:", history_id)
    print("Open Update Maintenance History to enter work performed, parts replaced, maintenance cost and currency.")

# Updating work order details before saving the changes
@cancellable
def update_work_order():
    work_order_id = operation_input("Enter the work order ID you want to update: ").strip()

    for work_order in work_order_list:
        if work_order["id"].casefold() == work_order_id.casefold():
            print("Work order found!")
            print(work_order)

            # Checking whether the work order already has linked maintenance history
            has_history = any(
                isinstance(history.get("work_order_id"), str)
                and history["work_order_id"].casefold() == work_order["id"].casefold()
                for history in maintenance_history_list
            )

            # Preventing changes to completed work orders with linked history
            if work_order["status"].casefold() == "completed" and has_history:
                print(
                    "This completed work order has linked maintenance "
                    "history and cannot be updated."
                )
                return

            # Using a copy to keep the original work order unchanged until saving
            updated_order = work_order.copy()

            while True:
                print("\nWhat would you like to update?")
                print("1. Fault Description")
                print("2. Equipment ID")
                print("3. Maintenance Priority")
                print("4. Status")
                print("5. Save Changes")
                print("6. Cancel")

                choice = operation_input("Enter your choice: ").strip()

                if choice == "1":
                    # Making sure the fault description is not left empty
                    while True:
                        new_value = operation_input(
                            "Enter new fault description: "
                        ).strip()

                        if not new_value:
                            print("Fault description cannot be empty.")
                            continue

                        updated_order["fault_description"] = new_value
                        break

                elif choice == "2":
                    # Checking that the new equipment ID belongs to registered equipment
                    while True:
                        new_value = operation_input(
                            "Enter new equipment ID: "
                        ).strip().upper()

                        if not new_value:
                            print("Equipment ID cannot be empty.")
                            continue

                        equipment_found = any(
                            equipment["id"].casefold() == new_value.casefold()
                            for equipment in equipment_list
                        )

                        if not equipment_found:
                            print("Equipment ID not found.")
                            continue

                        updated_order["equipment_id"] = new_value
                        break

                elif choice == "3":
                    # Accepting only Low, Medium or High as the priority
                    while True:
                        new_value = operation_input(
                            "Enter new priority (Low/Medium/High): "
                        ).strip().title()

                        if new_value not in ["Low", "Medium", "High"]:
                            print("Invalid priority.")
                            continue

                        updated_order["priority"] = new_value
                        break

                elif choice == "4":
                    # Checking that the new work order status is valid
                    while True:
                        new_value = operation_input(
                            "Enter new status (Pending/In Progress/Completed): "
                        ).strip().title()

                        if new_value not in [
                            "Pending", "In Progress", "Completed"
                        ]:
                            print("Invalid status.")
                            continue

                        updated_order["status"] = new_value
                        break

                elif choice == "5":
                    # Checking whether the status is changing to Completed before saving
                    completing_order = (
                        updated_order["status"] == "Completed"
                        and work_order["status"].casefold() != "completed"
                    )

                    work_order.update(updated_order)

                    with open("work_orders.json", "w") as file:
                        json.dump(work_order_list, file, indent=4)

                    # Creating maintenance history after saving the completed work order
                    if completing_order:
                        create_automatic_maintenance_history(work_order)

                    print("Work order updated successfully!")
                    return

                elif choice == "6":
                    # Discarding changes without modifying the original work order
                    print("Update canceled. No changes were saved.")
                    return

                else:
                    print("Invalid choice. Please select 1 to 6.")

                print("\nCurrent changes:")
                print(updated_order)

            return

    print("Work order not found. Please check the work order ID.")

# Deleting work orders only when they have no linked maintenance history
@cancellable
def delete_work_order():
    work_order_id = operation_input("Enter the work order ID you want to delete: ").strip()
    found = False

    for work_order in work_order_list:
        if work_order["id"].casefold() == work_order_id.casefold():
            found = True
            print("Work order found!")

            # Preventing deletion when linked maintenance history exists
            for history in maintenance_history_list:
                linked_id = history.get("work_order_id")
                if isinstance(linked_id, str) and linked_id.casefold() == work_order["id"].casefold():
                    print("Cannot delete this work order because it has linked maintenance history.")
                    return

            print(work_order)
            
            # Asking for confirmation before deleting the work order
            confirmation = operation_input("Are you sure you want to delete this work order? (yes/no): ")

            if confirmation.strip().lower() == "yes":
                work_order_list.remove(work_order)

                with open("work_orders.json", "w") as file:
                    json.dump(work_order_list, file, indent=4)

                print("Work order deleted successfully!")
            else:
                print("Deletion canceled.")
            break

    if found == False:
        print("Work order not found. Please check the work order ID.")


# Creating a schedule for equipment that needs regular maintenance
@cancellable
def create_maintenance_schedule():
    # Generating the next schedule ID without changing the counter until saving
    schedule_number = id_counters["last_schedule_id"] + 1

    schedule_id = f"MS{schedule_number:03d}"

    print("Generated Maintenance Schedule ID:", schedule_id)

    # Checking that the equipment is registered before scheduling maintenance
    while True:
        equipment_id = operation_input("Enter equipment ID for maintenance: ").strip().upper()

        if equipment_id == "":
            print("Equipment ID cannot be empty. Please try again.")
            continue

        equipment_found = False

        for equipment in equipment_list:
            if equipment["id"].casefold() == equipment_id.casefold():
                equipment_found = True
                equipment_name = equipment["name"]
                break

        if not equipment_found:
            print("Equipment ID not found. Please enter a valid equipment ID.")
            continue

        print("Equipment Name:", equipment_name)
        break

    # Making sure the maintenance task is not left empty
    while True:
        maintenance_task = operation_input("Enter maintenance task: ").strip()

        if maintenance_task == "":
            print("Maintenance task cannot be empty. Please try again.")
            continue

        break

    # Accepting different date formats and storing dates as year-month-day
    while True:
        last_maintenance_date = operation_input(
            "Enter last maintenance date (e.g. 19/11/2026 or 2026-11-19): "
        ).strip()

        date_formats = [
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%m-%d-%Y",
            "%Y/%m/%d",
            "%d/%m/%Y",
            "%m/%d/%Y"
        ]

        date = None

        for date_format in date_formats:
            try:
                date = datetime.strptime(last_maintenance_date, date_format)
                break

            except ValueError:
                continue

        if date is None:
            print("Invalid date. Please enter a valid date.")
            continue

        last_maintenance_date = date.strftime("%Y-%m-%d")
        break

    # Providing a choice of Days, Months or Years for recurring maintenance
    while True:
        print("\nSelect maintenance interval unit:")
        print("1. Days")
        print("2. Months")
        print("3. Years")

        interval_choice = operation_input("Enter your choice: ").strip()

        if interval_choice == "1":
            interval_unit = "Days"
            break

        elif interval_choice == "2":
            interval_unit = "Months"
            break

        elif interval_choice == "3":
            interval_unit = "Years"
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")

    # Accepting only whole-number intervals greater than zero
    while True:
        maintenance_interval = operation_input(
            f"Enter maintenance interval ({interval_unit}): "
        ).strip()

        try:
            maintenance_interval = int(maintenance_interval)

            if maintenance_interval <= 0:
                print("Maintenance interval must be greater than zero.")
                continue

            break

        except ValueError:
            print("Invalid interval. Please enter a whole number.")

    # Calculating the next maintenance date using the last date and selected interval
    last_date = datetime.strptime(last_maintenance_date, "%Y-%m-%d")

    if interval_unit == "Days":
        next_date = last_date + timedelta(days=maintenance_interval)

    elif interval_unit == "Months":
        next_date = last_date + relativedelta(months=maintenance_interval)

    elif interval_unit == "Years":
        next_date = last_date + relativedelta(years=maintenance_interval)

    next_maintenance_date = next_date.strftime("%Y-%m-%d")

    # Storing the maintenance schedule details in a dictionary
    maintenance_schedule = {
        "id": schedule_id,
        "equipment_id": equipment_id,
        "maintenance_task": maintenance_task,
        "last_maintenance_date": last_maintenance_date,
        "maintenance_interval": maintenance_interval,
        "interval_unit": interval_unit,
        "next_maintenance_date": next_maintenance_date
    }

    # Confirming and saving the schedule and its ID counter
    if not confirm_save(maintenance_schedule):
        return

    id_counters["last_schedule_id"] = schedule_number
    maintenance_schedule_list.append(maintenance_schedule)

    with open("maintenance_schedule.json", "w") as file:
        json.dump(maintenance_schedule_list, file, indent=4)

    with open("id_counters.json", "w") as file:
        json.dump(id_counters, file, indent=4)

    print("Maintenance schedule created successfully!")
    print("Next maintenance date:", next_maintenance_date)

# Displaying all maintenance schedules with their current status
def view_maintenance_schedules():
    if not maintenance_schedule_list:
        print("No maintenance schedules found.")
        return

    print("Maintenance Schedules:")
    for schedule in maintenance_schedule_list:
        print("------------------------------")
        print("Schedule ID:", schedule["id"])
        print("Equipment ID:", schedule["equipment_id"])
        print("Maintenance Task:", schedule["maintenance_task"])
        print("Last Maintenance Date:", schedule["last_maintenance_date"])
        print("Maintenance Interval:", schedule["maintenance_interval"], schedule["interval_unit"])
        print("Next Maintenance Date:", schedule["next_maintenance_date"])
        print("Maintenance Status:", check_maintenance_status(schedule["next_maintenance_date"]))
        print("------------------------------")


# Comparing the next maintenance date with today's date to determine its status
def check_maintenance_status(next_maintenance_date):
    today = datetime.today().date()
    next_date = datetime.strptime(next_maintenance_date, "%Y-%m-%d").date()

    if next_date < today:
        return "Overdue"

    elif next_date == today:
        return "Due Today"

    else:
        return "Upcoming"

# Searching for a maintenance schedule using its ID
@cancellable
def search_maintenance_schedule():
    search_id = operation_input("Enter maintenance schedule ID to search: ").strip()
    found = False

    # Displaying the matching schedule with its maintenance status
    for schedule in maintenance_schedule_list:
        if schedule["id"].casefold() == search_id.casefold():
            print("Maintenance schedule found!")
            print("------------------------------")
            print("Schedule ID:", schedule["id"])
            print("Equipment ID:", schedule["equipment_id"])
            print("Maintenance Task:", schedule["maintenance_task"])
            print("Last Maintenance Date:", schedule["last_maintenance_date"])
            print("Maintenance Interval:", schedule["maintenance_interval"], schedule["interval_unit"])
            print("Next Maintenance Date:", schedule["next_maintenance_date"])
            print("Maintenance Status:", check_maintenance_status(schedule["next_maintenance_date"]))
            print("------------------------------")
            found = True
            break

    if not found:
        print("Maintenance schedule not found. Please check the schedule ID.")

# Updating maintenance schedule details before saving the changes
@cancellable
def update_maintenance_schedule():
    schedule_id = operation_input("Enter maintenance schedule ID to update: ").strip()

    for schedule in maintenance_schedule_list:
        if schedule["id"].casefold() == schedule_id.casefold():
            print("Maintenance schedule found!")
            print(schedule)

            # Using a copy to keep the original schedule unchanged until saving
            updated_schedule = schedule.copy()

            while True:
                print("\nWhat would you like to update?")
                print("1. Maintenance Task")
                print("2. Last Maintenance Date")
                print("3. Maintenance Interval and Unit")
                print("4. Save Changes")
                print("5. Cancel")

                choice = operation_input("Enter your choice: ").strip()

                if choice == "1":
                    # Making sure the maintenance task is not left empty
                    while True:
                        new_task = operation_input(
                            "Enter new maintenance task: "
                        ).strip()

                        if not new_task:
                            print("Maintenance task cannot be empty.")
                            continue

                        updated_schedule["maintenance_task"] = new_task
                        break

                elif choice == "2":
                    # Accepting the same date formats used when creating a schedule
                    date_formats = [
                        "%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y",
                        "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y"
                    ]

                    while True:
                        new_date = operation_input(
                            "Enter new last maintenance date: "
                        ).strip()

                        parsed_date = None

                        for date_format in date_formats:
                            try:
                                parsed_date = datetime.strptime(
                                    new_date, date_format
                                )
                                break
                            except ValueError:
                                continue

                        if parsed_date is None:
                            print("Invalid date. Please try again.")
                            continue

                        updated_schedule["last_maintenance_date"] = (
                            parsed_date.strftime("%Y-%m-%d")
                        )
                        break

                elif choice == "3":
                    # Providing a choice of interval units for recurring maintenance
                    while True:
                        print("\nSelect maintenance interval unit:")
                        print("1. Days")
                        print("2. Months")
                        print("3. Years")

                        unit_choice = operation_input("Enter your choice: ").strip()

                        units = {
                            "1": "Days",
                            "2": "Months",
                            "3": "Years"
                        }

                        if unit_choice in units:
                            interval_unit = units[unit_choice]
                            break

                        print("Invalid choice. Please select 1, 2 or 3.")

                    # Accepting only whole-number intervals greater than zero
                    while True:
                        new_interval = operation_input(
                            f"Enter maintenance interval ({interval_unit}): "
                        ).strip()

                        try:
                            new_interval = int(new_interval)

                            if new_interval <= 0:
                                print("Maintenance interval must be greater than zero.")
                                continue

                            break

                        except ValueError:
                            print("Invalid interval. Please enter a whole number.")

                    updated_schedule["maintenance_interval"] = new_interval
                    updated_schedule["interval_unit"] = interval_unit

                elif choice == "4":
                    # Recalculating the next maintenance date before saving
                    last_date = datetime.strptime(
                        updated_schedule["last_maintenance_date"],
                        "%Y-%m-%d"
                    )

                    interval = updated_schedule["maintenance_interval"]
                    unit = updated_schedule["interval_unit"]

                    if unit == "Days":
                        next_date = last_date + timedelta(days=interval)

                    elif unit == "Months":
                        next_date = last_date + relativedelta(months=interval)

                    elif unit == "Years":
                        next_date = last_date + relativedelta(years=interval)

                    updated_schedule["next_maintenance_date"] = (
                        next_date.strftime("%Y-%m-%d")
                    )

                    # Saving the updated maintenance schedule to JSON
                    schedule.update(updated_schedule)

                    with open("maintenance_schedule.json", "w") as file:
                        json.dump(maintenance_schedule_list, file, indent=4)

                    print("Maintenance schedule updated successfully!")
                    print(
                        "Next maintenance date:",
                        schedule["next_maintenance_date"]
                    )
                    return

                elif choice == "5":
                    # Discarding changes without modifying the original schedule
                    print("Update canceled. No changes were saved.")
                    return

                else:
                    print("Invalid choice. Please select 1 to 5.")

                print("\nCurrent changes:")
                print(updated_schedule)

            return

    print("Maintenance schedule not found. Please check the schedule ID.")

# Deleting a maintenance schedule after confirmation
@cancellable
def delete_maintenance_schedule():
    schedule_id = operation_input("Enter maintenance schedule ID to delete: ").strip()
    found = False

    for schedule in maintenance_schedule_list:
        if schedule["id"].casefold() == schedule_id.casefold():
            found = True

            print("Maintenance schedule found!")
            print("Schedule ID:", schedule["id"])
            print("Equipment ID:", schedule["equipment_id"])
            print("Maintenance Task:", schedule["maintenance_task"])
            print("Next Maintenance Date:", schedule["next_maintenance_date"])

            # Asking for confirmation before removing the schedule from the saved records
            confirmation = operation_input("Are you sure you want to delete this maintenance schedule? (yes/no): ").strip().lower()

            if confirmation == "yes":
                maintenance_schedule_list.remove(schedule)

                with open("maintenance_schedule.json", "w") as file:
                    json.dump(maintenance_schedule_list, file, indent=4)

                print("Maintenance schedule deleted successfully!")

            else:
                print("Deletion canceled.")

            return

    if not found:
        print("Maintenance schedule not found. Please check the schedule ID.")


# Displaying all saved maintenance history records
def view_maintenance_history():
    # Showing a message when no maintenance history records exist
    if not maintenance_history_list:
        print("No maintenance history records found.")
        return

    print("\nMaintenance History Records:")

    # Displaying the saved details of each maintenance history record
    for history in maintenance_history_list:
        print("------------------------------")
        print("History ID:", history["id"])
        print("Work Order ID:", history.get("work_order_id", "N/A"))
        print("Equipment ID:", history["equipment_id"])
        print("Maintenance Date:", history["maintenance_date"])
        print("Fault Description:", history.get("fault_description", "N/A"))
        print("Work Performed:", history["work_performed"])
        print("Parts Replaced:", history["parts_replaced"])

        currency = history.get("maintenance_cost_currency")
        cost = history.get("maintenance_cost")

        # Displaying missing costs as not recorded rather than zero
        if cost is None:
            print("Maintenance Cost: Not recorded")
        elif currency is None:
            print("Maintenance Cost:", cost, "(currency not recorded)")
        else:
            print("Maintenance Cost:", cost, currency)

        print("------------------------------")

# Searching for a maintenance history record using its ID
@cancellable
def search_maintenance_history():
    history_id = operation_input("Enter maintenance history ID to search: ").strip()
    for history in maintenance_history_list:
        if history["id"].casefold() == history_id.casefold():
            print("Maintenance history found!")
            print(history)
            return
    print("Maintenance history not found. Please check the history ID.")


# Updating maintenance history details before saving the changes
@cancellable
def update_maintenance_history():
    history_id = operation_input("Enter maintenance history ID to update: ").strip()

    for history in maintenance_history_list:
        if history["id"].casefold() == history_id.casefold():
            print("Maintenance history found!")
            print(history)

            # Using a copy to keep the original history record unchanged until saving
            updated_history = history.copy()

            while True:
                print("\nWhat would you like to update?")
                print("1. Maintenance Date")
                print("2. Fault Description")
                print("3. Work Performed")
                print("4. Parts Replaced")
                print("5. Maintenance Cost Currency")
                print("6. Maintenance Cost")
                print("7. Save Changes")
                print("8. Cancel")

                choice = operation_input("Enter your choice: ").strip()

                if choice == "1":
                    # Checking the maintenance date before updating it
                    date_formats = [
                        "%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y",
                        "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y"
                    ]

                    while True:
                        new_date = operation_input(
                            "Enter new maintenance date: "
                        ).strip()

                        parsed_date = None

                        for date_format in date_formats:
                            try:
                                parsed_date = datetime.strptime(
                                    new_date, date_format
                                )
                                break
                            except ValueError:
                                continue

                        if parsed_date is None:
                            print("Invalid date. Please try again.")
                            continue

                        updated_history["maintenance_date"] = (
                            parsed_date.strftime("%Y-%m-%d")
                        )
                        break

                elif choice == "2":
                    # Allowing the fault description to be left empty
                    updated_history["fault_description"] = operation_input(
                        "Enter fault description (press Enter if none): "
                    ).strip()

                elif choice == "3":
                    # Making sure the work description is not left empty when updated
                    while True:
                        new_value = operation_input(
                            "Enter work performed: "
                        ).strip()

                        if not new_value:
                            print("Work description cannot be empty.")
                            continue

                        updated_history["work_performed"] = new_value
                        break

                elif choice == "4":
                    # Allowing the parts replaced field to be left empty
                    updated_history["parts_replaced"] = operation_input(
                        "Enter parts replaced (press Enter if none): "
                    ).strip()

                elif choice == "5":
                    # Providing GBP, USD or NGN as maintenance cost currency options
                    while True:
                        print("\nSelect maintenance cost currency:")
                        print("1. GBP (£)")
                        print("2. USD ($)")
                        print("3. NGN (₦)")

                        currency_choice = operation_input("Enter your choice: ").strip()

                        currencies = {
                            "1": "GBP",
                            "2": "USD",
                            "3": "NGN"
                        }

                        if currency_choice in currencies:
                            updated_history["maintenance_cost_currency"] = (
                                currencies[currency_choice]
                            )
                            break

                        print("Invalid currency. Please select 1, 2 or 3.")

                elif choice == "6":
                    currency = updated_history.get(
                        "maintenance_cost_currency"
                    )

                    # Checking that a currency has been selected before entering the cost
                    if currency is None:
                        print("Please select a maintenance cost currency first.")
                        continue

                    while True:
                        new_cost = operation_input(
                            f"Enter new maintenance cost ({currency}): "
                        ).strip()

                        try:
                            new_cost = float(new_cost)

                            if new_cost < 0:
                                print("Maintenance cost cannot be negative.")
                                continue

                            updated_history["maintenance_cost"] = new_cost
                            break

                        except ValueError:
                            print("Invalid cost. Please enter a number.")

                elif choice == "7":
                    # Saving maintenance history changes only when Save Changes is selected
                    history.update(updated_history)

                    with open("maintenance_history.json", "w") as file:
                        json.dump(maintenance_history_list, file, indent=4)

                    print("Maintenance history updated successfully!")
                    return

                elif choice == "8":
                    # Leaving the original history record unchanged when canceled
                    print("Update canceled. No changes were saved.")
                    return

                else:
                    print("Invalid choice. Please select 1 to 8.")

                print("\nCurrent changes:")
                print(updated_history)

            return

    print("Maintenance history not found. Please check the history ID.")
    
# Deleting maintenance history records that are not linked to completed work orders
@cancellable
def delete_maintenance_history():
    history_id = operation_input(
        "Enter maintenance history ID to delete: "
    ).strip()

    for history in maintenance_history_list:
        if history["id"].casefold() == history_id.casefold():

            print("Maintenance history found!")
            print(history)

            # Checking the work order ID linked to the history record
            work_order_id = history.get("work_order_id")

            # Preventing deletion of history linked to a completed work order
            if work_order_id and str(work_order_id).lower() != "null":
                for work_order in work_order_list:
                    if work_order["id"].casefold() == work_order_id.casefold():
                        if work_order["status"].casefold() == "completed":
                            print(
                                "This maintenance history cannot be deleted "
                                "because it is linked to a completed work order."
                            )
                            return

            # Asking for a valid yes or no response before deleting the record
            while True:
                confirmation = operation_input(
                    "Are you sure you want to delete this maintenance history? (yes/no): "
                ).strip().lower()

                if confirmation == "yes":
                    maintenance_history_list.remove(history)

                    with open("maintenance_history.json", "w") as file:
                        json.dump(maintenance_history_list, file, indent=4)

                    print("Maintenance history deleted successfully!")
                    return

                elif confirmation == "no":
                    print("Deletion canceled.")
                    return

                else:
                    print("Invalid response. Please enter yes or no.")

    print("Maintenance history not found. Please check the history ID.")

# Providing the main menu for accessing the application features
def main_menu():
    choice = ""

    # Displaying the menu until the user chooses to exit
    while choice != "20":
        print("Welcome to the Equipment Management System")
        print("1. View Equipment List")
        print("2. Add New Equipment")
        print("3. Search Equipment")
        print("4. Update Equipment Details")
        print("5. Delete Equipment")
        print("6. Create Work Order")
        print("7. View Work Orders")
        print("8. Search Work Order")
        print("9. Update Work Order")
        print("10. Delete Work Order")
        print("11. Create Maintenance Schedule")
        print("12. View Maintenance Schedules")
        print("13. Search Maintenance Schedule")
        print("14. Update Maintenance Schedule")
        print("15. Delete Maintenance Schedule")
        print("16. View Maintenance History")
        print("17. Search Maintenance History")
        print("18. Update Maintenance History")
        print("19. Delete Maintenance History")
        print("20. Exit")

        choice = input("Enter your choice: ")

        # Running the function that matches the selected menu option
        if choice == "1":
            print(equipment_list)
        elif choice == "2":
            add_new_equipment()
        elif choice == "3":
            search_equipment()
        elif choice == "4":
            update_equipment_details()
        elif choice == "5":
            delete_equipment()
        elif choice == "6":
            create_work_order()
        elif choice == "7":
            print(work_order_list)
        elif choice == "8":
            search_work_order()
        elif choice == "9":
            update_work_order()
        elif choice == "10":
            delete_work_order()
        elif choice == "11":
            create_maintenance_schedule()
        elif choice == "12":
            view_maintenance_schedules()
        elif choice == "13":
            search_maintenance_schedule()
        elif choice == "14":
            update_maintenance_schedule()
        elif choice == "15":
            delete_maintenance_schedule()
        elif choice == "16":
            view_maintenance_history()
        elif choice == "17":
            search_maintenance_history()
        elif choice == "18":
            update_maintenance_history()
        elif choice == "19":
            delete_maintenance_history()
        elif choice == "20":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Starting the program with the main menu
main_menu()  