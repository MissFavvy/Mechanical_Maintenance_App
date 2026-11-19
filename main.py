#AI PLUGIN WAS USED TO REVIEW THE CODE BLOCKS

import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

with open("equipment_data.json", "r") as file:
    equipment_list = json.load(file)

print(equipment_list)

with open("id_counters.json", "r") as file:
    id_counters = json.load(file)

print(id_counters)

with open("work_orders.json", "r") as file:
    work_order_list = json.load(file)

print(work_order_list)

with open("maintenance_schedule.json", "r") as file:
    maintenance_schedule_list = json.load(file)

print(maintenance_schedule_list)

with open("maintenance_history.json", "r") as file:
    maintenance_history_list = json.load(file)

print(maintenance_history_list)

def add_new_equipment():
    id_counters["last_equipment_id"] += 1

    equipment_number = id_counters["last_equipment_id"]

    equipment_id = f"EQ{equipment_number:03d}"

    print("Generated Equipment ID:", equipment_id)

    while True:
        equipment_name = input("Enter equipment name: ").strip().title()

        if equipment_name == "":
            print("Equipment name cannot be empty. Please try again.")
            continue
        break

    while True:
        equipment_type = input("Enter equipment type: ").strip().title()
        if equipment_type == "":
            print("Equipment type cannot be empty. Please try again.")
            continue
        break

    while True:
        equipment_location = input("Enter equipment location: ").strip().title()
        if equipment_location == "":
            print("Equipment location cannot be empty. Please try again.")
            continue
        break

    while True:
        temperature = input("Enter equipment temperature (press Enter if unavailable): ")
        if temperature == "":
            temperature = None
            break
        else:
            try:
                temperature = float(temperature)
                break
            except ValueError:
                print("Invalid temperature. Please enter a number.")
    while True:
        vibration = input("Enter equipment vibration (press Enter if unavailable): ")
        if vibration == "":
            vibration = None
            break
        else:
            try:
                vibration = float(vibration)
                break
            except ValueError:
                print("Invalid vibration. Please enter a number.")

    while True:
        operating_hours = input("Enter equipment operating hours (press Enter if unavailable): ")
        if operating_hours == "":
            operating_hours = None
            break
        else:
            try:
                operating_hours = float(operating_hours)
                break
            except ValueError:
                print("Invalid operating hours. Please enter a number.")

    new_equipment = {
         "id": equipment_id,
         "name": equipment_name,
         "type": equipment_type,
         "location": equipment_location,
         "temperature": temperature,
         "vibration": vibration,
         "operating_hours": operating_hours
    }

    equipment_list.append(new_equipment)

    with open("equipment_data.json", "w") as file:
        json.dump(equipment_list, file, indent=4)

    with open("id_counters.json", "w") as file:
        json.dump(id_counters, file, indent=4)

def search_equipment():
    search_id = input("Enter equipment ID to search: ").strip()
    found = False

    for equipment in equipment_list:
        if equipment["id"].casefold() == search_id.casefold():
            print("Equipment found!")
            print(equipment)
            found = True

    if found == False:
        print("Equipment not found. Please check the equipment ID.")


def update_equipment_details():
    equipment_id = input("Enter the equipment ID you want to update: ").strip()
    found = False

    for equipment in equipment_list:
        if equipment["id"].casefold() == equipment_id.casefold():
            found = True

            print("Equipment found!")
            print(equipment)

            print("\nWhat would you like to update?")
            print("1. Equipment Name")
            print("2. Equipment Type")
            print("3. Equipment Location")
            print("4. Temperature")
            print("5. Vibration")
            print("6. Operating Hours")

            choice = input("Enter your choice: ")

            if choice == "1":
                while True:
                    new_value = input("Enter new equipment name: ").strip().title()

                    if new_value == "":
                        print("Equipment name cannot be empty. Please try again.")
                        continue

                    equipment["name"] = new_value
                    break   

            elif choice == "2":
                while True:
                    new_value = input("Enter new equipment type: ").strip().title()

                    if new_value == "":
                        print("Equipment type cannot be empty. Please try again.")
                        continue

                    equipment["type"] = new_value
                    break

            elif choice == "3":
                while True:
                    new_value = input("Enter new equipment location: ").strip().title()

                    if new_value == "":
                        print("Equipment location cannot be empty. Please try again.")
                        continue

                    equipment["location"] = new_value
                    break

            elif choice in ["4", "5", "6"]:

                    if choice == "4":
                        field = "temperature"
                        field_name = "temperature"

                    elif choice == "5":
                        field = "vibration"
                        field_name = "vibration"

                    else:
                        field = "operating_hours"
                        field_name = "operating hours"

                    while True:
                        new_value = input(
                            f"Enter new equipment {field_name} (press Enter if unavailable): "
                        ).strip()

                        if new_value == "":
                            equipment[field] = None
                            break

                        try:
                            equipment[field] = float(new_value)
                            break

                        except ValueError:
                            print(f"Invalid {field_name}. Please enter a number.")
            
            else:
                print("Invalid choice. Please select an option from 1 to 6.")
                return

            with open("equipment_data.json", "w") as file:
                json.dump(equipment_list, file, indent=4)

            print("Equipment details updated successfully!")
            return

    if found == False:
        print("Equipment not found. Please check the equipment ID.")    

def delete_equipment():
    equipment_id = input("Enter the equipment ID you want to delete: ").strip()
    found = False

    for equipment in equipment_list:
        if equipment["id"].casefold() == equipment_id.casefold():
            found = True
            print("Equipment found!")
            print(equipment)

            has_work_order = False
            has_maintenance_schedule = False

            for work_order in work_order_list:
                if work_order["equipment_id"].casefold() == equipment["id"].casefold():
                    has_work_order = True
                    break

            for schedule in maintenance_schedule_list:
                if schedule["equipment_id"].casefold() == equipment["id"].casefold():
                    has_maintenance_schedule = True
                    break

            if has_work_order or has_maintenance_schedule:
                print("This equipment cannot be deleted because:")

                if has_work_order:
                    print("- It has an existing work order.")

                if has_maintenance_schedule:
                    print("- It has an existing maintenance schedule.")

                return

            confirmation = input("Are you sure you want to delete this equipment? (yes/no): ")

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

def create_work_order():
    id_counters["last_work_order_id"] += 1

    work_order_number = id_counters["last_work_order_id"]

    work_order_id = f"WO{work_order_number:03d}"

    print("Generated Work Order ID:", work_order_id)
    
    while True:
        fault_description = input("Enter fault description: ").strip()
        if fault_description == "":
            print("Fault description cannot be empty. Please try again.")
            continue
        break

    while True:
        equipment_id = input("Enter equipment ID for the work order: ").strip().upper()
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

    while True:
        priority = input("Enter maintenance priority (Low/Medium/High): ").strip().title()
        if priority == "":
            print("Maintenance priority cannot be empty. Please try again.")
            continue
        if priority.casefold() not in ["low", "medium", "high"]:
            print("Invalid priority. Please enter Low, Medium, or High.")
            continue
        break

    status = "Pending"

    work_order = {
        "id": work_order_id,
        "fault_description": fault_description,
        "equipment_id": equipment_id,
        "priority": priority,
        "status": status
    }
    
    work_order_list.append(work_order)

    with open("work_orders.json", "w") as file:
        json.dump(work_order_list, file, indent=4)

    with open("id_counters.json", "w") as file:
        json.dump(id_counters, file, indent=4)

def search_work_order():
    search_id = input("Enter work order ID to search: ").strip()
    found = False

    for work_order in work_order_list:
        if work_order["id"].casefold() == search_id.casefold():
            print("Work order found!")
            print(work_order)
            found = True

    if found == False:
        print("Work order not found. Please check the work order ID.")


def create_automatic_maintenance_history(work_order):
    for history in maintenance_history_list:
        if (history.get("work_order_id") or "").casefold() == work_order["id"].casefold():
            print("Maintenance history already exists for this work order.")
            return

    id_counters["last_history_id"] += 1

    history_number = id_counters["last_history_id"]

    history_id = f"MH{history_number:03d}"

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

    maintenance_history_list.append(maintenance_record)

    with open("maintenance_history.json", "w") as file:
        json.dump(maintenance_history_list, file, indent=4)

    with open("id_counters.json", "w") as file:
        json.dump(id_counters, file, indent=4)

    print("Maintenance history automatically created!")
    print("History ID:", history_id)

def update_work_order():
    work_order_id = input("Enter the work order ID you want to update: ").strip()
    found = False

    for work_order in work_order_list:
        if work_order["id"].casefold() == work_order_id.casefold():
            found = True

            print("Work order found!")
            print(work_order)

            print("\nWhat would you like to update?")
            print("1. Fault Description")
            print("2. Equipment ID")
            print("3. Maintenance Priority")
            print("4. Status")

            choice = input("Enter your choice: ")

            if choice == "1":
                while True:
                    new_value = input("Enter new fault description: ").strip()

                    if new_value == "":
                        print("Fault description cannot be empty. Please try again.")
                        continue

                    work_order["fault_description"] = new_value
                    break   

            elif choice == "2":
                while True:
                    new_value = input("Enter new equipment ID: ").strip().upper()

                    if new_value == "":
                        print("Equipment ID cannot be empty. Please try again.")
                        continue

                    found_equipment = False
                    for equipment in equipment_list:
                        if equipment["id"].casefold() == new_value.casefold():
                            found_equipment = True
                            break

                    if not found_equipment:
                        print("Equipment ID not found. Please enter a valid equipment ID.")
                        continue

                    work_order["equipment_id"] = new_value
                    break

            elif choice == "3":
                while True:
                    new_value = input("Enter new maintenance priority (Low/Medium/High): ").strip().title()

                    if new_value == "":
                        print("Maintenance priority cannot be empty. Please try again.")
                        continue

                    if new_value.casefold() not in ["low", "medium", "high"]:
                        print("Invalid priority. Please enter Low, Medium, or High.")
                        continue

                    work_order["priority"] = new_value
                    break

            elif choice == "4":
                while True:
                    new_value = input("Enter new status (Pending/In Progress/Completed): ").strip().title()

                    if new_value == "":
                        print("Status cannot be empty. Please try again.")
                        continue

                    if new_value.casefold() not in ["pending", "in progress", "completed"]:
                        print("Invalid status. Please enter Pending, In Progress, or Completed.")
                        continue

                    work_order["status"] = new_value
                    if new_value.casefold() == "completed":
                        create_automatic_maintenance_history(work_order)
                    break
            
            else:
                print("Invalid choice. Please try again.")
                return

            with open("work_orders.json", "w") as file:
                json.dump(work_order_list, file, indent=4)
            
            print("Work order updated successfully!")
            return
    if found == False:
        print("Work order not found. Please check the work order ID.")

def delete_work_order():
    work_order_id = input("Enter the work order ID you want to delete: ").strip()
    found = False

    for work_order in work_order_list:
        if work_order["id"].casefold() == work_order_id.casefold():
            found = True
            print("Work order found!")
            print(work_order)
            
            confirmation = input("Are you sure you want to delete this work order? (yes/no): ")

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

def create_maintenance_schedule():
    id_counters["last_schedule_id"] += 1

    schedule_number = id_counters["last_schedule_id"]

    schedule_id = f"MS{schedule_number:03d}"

    print("Generated Maintenance Schedule ID:", schedule_id)

    while True:
        equipment_id = input("Enter equipment ID for maintenance: ").strip().upper()

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

    while True:
        maintenance_task = input("Enter maintenance task: ").strip()

        if maintenance_task == "":
            print("Maintenance task cannot be empty. Please try again.")
            continue

        break

    while True:
        last_maintenance_date = input(
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

    while True:
        print("\nSelect maintenance interval unit:")
        print("1. Days")
        print("2. Months")
        print("3. Years")

        interval_choice = input("Enter your choice: ").strip()

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

    while True:
        maintenance_interval = input(
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

    last_date = datetime.strptime(last_maintenance_date, "%Y-%m-%d")

    if interval_unit == "Days":
        next_date = last_date + timedelta(days=maintenance_interval)

    elif interval_unit == "Months":
        next_date = last_date + relativedelta(months=maintenance_interval)

    elif interval_unit == "Years":
        next_date = last_date + relativedelta(years=maintenance_interval)

    next_maintenance_date = next_date.strftime("%Y-%m-%d")

    maintenance_schedule = {
        "id": schedule_id,
        "equipment_id": equipment_id,
        "maintenance_task": maintenance_task,
        "last_maintenance_date": last_maintenance_date,
        "maintenance_interval": maintenance_interval,
        "interval_unit": interval_unit,
        "next_maintenance_date": next_maintenance_date
    }

    maintenance_schedule_list.append(maintenance_schedule)

    with open("maintenance_schedule.json", "w") as file:
        json.dump(maintenance_schedule_list, file, indent=4)

    with open("id_counters.json", "w") as file:
        json.dump(id_counters, file, indent=4)

    print("Maintenance schedule created successfully!")
    print("Next maintenance date:", next_maintenance_date)

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


def check_maintenance_status(next_maintenance_date):
    today = datetime.today().date()
    next_date = datetime.strptime(next_maintenance_date, "%Y-%m-%d").date()

    if next_date < today:
        return "Overdue"

    elif next_date == today:
        return "Due Today"

    else:
        return "Upcoming"

def search_maintenance_schedule():
    search_id = input("Enter maintenance schedule ID to search: ").strip()
    found = False

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

def update_maintenance_schedule():
    schedule_id = input("Enter maintenance schedule ID to update: ").strip()
    found = False

    for schedule in maintenance_schedule_list:
        if schedule["id"].casefold() == schedule_id.casefold():
            found = True

            print("Maintenance schedule found!")
            print("Schedule ID:", schedule["id"])
            print("Equipment ID:", schedule["equipment_id"])
            print("Maintenance Task:", schedule["maintenance_task"])
            print("Last Maintenance Date:", schedule["last_maintenance_date"])
            print("Maintenance Interval:", schedule["maintenance_interval"], schedule["interval_unit"])

            print("\nWhat would you like to update?")
            print("1. Maintenance Task")
            print("2. Last Maintenance Date")
            print("3. Maintenance Interval and Unit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                while True:
                    new_task = input("Enter new maintenance task: ").strip()

                    if new_task == "":
                        print("Maintenance task cannot be empty.")
                        continue

                    schedule["maintenance_task"] = new_task
                    break

            elif choice == "2":
                while True:
                    new_date = input(
                        "Enter new last maintenance date (e.g. 19/11/2026 or 2026-11-19): "
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
                            date = datetime.strptime(new_date, date_format)
                            break

                        except ValueError:
                            continue

                    if date is None:
                        print("Invalid date. Please enter a valid date.")
                        continue

                    schedule["last_maintenance_date"] = date.strftime("%Y-%m-%d")
                    break

            elif choice == "3":
                while True:
                    print("\nSelect maintenance interval unit:")
                    print("1. Days")
                    print("2. Months")
                    print("3. Years")

                    unit_choice = input("Enter your choice: ").strip()

                    if unit_choice == "1":
                        interval_unit = "Days"
                        break
                    elif unit_choice == "2":
                        interval_unit = "Months"
                        break
                    elif unit_choice == "3":
                        interval_unit = "Years"
                        break
                    else:
                        print("Invalid choice. Please select 1, 2, or 3.")

                while True:
                    new_interval = input(
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

                schedule["maintenance_interval"] = new_interval
                schedule["interval_unit"] = interval_unit

            else:
                print("Invalid choice. Please try again.")
                return

            last_date = datetime.strptime(
                schedule["last_maintenance_date"], "%Y-%m-%d"
            )

            interval = schedule["maintenance_interval"]
            unit = schedule["interval_unit"]

            if unit == "Days":
                next_date = last_date + timedelta(days=interval)

            elif unit == "Months":
                next_date = last_date + relativedelta(months=interval)

            elif unit == "Years":
                next_date = last_date + relativedelta(years=interval)

            schedule["next_maintenance_date"] = next_date.strftime("%Y-%m-%d")

            with open("maintenance_schedule.json", "w") as file:
                json.dump(maintenance_schedule_list, file, indent=4)

            print("Maintenance schedule updated successfully!")
            print("Next maintenance date:", schedule["next_maintenance_date"])
            return

    if not found:
        print("Maintenance schedule not found. Please check the schedule ID.")

def delete_maintenance_schedule():
    schedule_id = input("Enter maintenance schedule ID to delete: ").strip()
    found = False

    for schedule in maintenance_schedule_list:
        if schedule["id"].casefold() == schedule_id.casefold():
            found = True

            print("Maintenance schedule found!")
            print("Schedule ID:", schedule["id"])
            print("Equipment ID:", schedule["equipment_id"])
            print("Maintenance Task:", schedule["maintenance_task"])
            print("Next Maintenance Date:", schedule["next_maintenance_date"])

            confirmation = input("Are you sure you want to delete this maintenance schedule? (yes/no): ").strip().lower()

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

def add_maintenance_history():
    history_number = id_counters["last_history_id"] + 1
    history_id = f"MH{history_number:03d}"

    print("Generated Maintenance History ID:", history_id)

    while True:
        equipment_id = input("Enter equipment ID: ").strip().upper()

        equipment_found = False

        for equipment in equipment_list:
            if equipment["id"].casefold() == equipment_id.casefold():
                equipment_found = True
                print("Equipment Name:", equipment["name"])
                break

        if equipment_found:
            break

        print("Equipment ID not found. Please enter a valid equipment ID.")

    while True:
        maintenance_date = input(
            "Enter maintenance date (e.g. 19/11/2026 or 2026-11-19): "
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
                date = datetime.strptime(maintenance_date, date_format)
                break

            except ValueError:
                continue

        if date is None:
            print("Invalid date. Please enter a valid date.")
            continue

        maintenance_date = date.strftime("%Y-%m-%d")
        break

    while True:
        work_performed = input(
            "Enter description of work performed: "
        ).strip()

        if work_performed == "":
            print("Work description cannot be empty.")
            continue

        break

    parts_replaced = input(
        "Enter parts replaced (press Enter if none): "
    ).strip()

    fault_description = input(
        "Enter fault description (press Enter if none): "
    ).strip()

    while True:
        print("\nSelect maintenance cost currency:")
        print("1. GBP (£)")
        print("2. USD ($)")
        print("3. NGN (₦)")

        currency_choice = input("Enter your choice: ").strip()

        if currency_choice == "1":
            maintenance_cost_currency = "GBP"
            break

        elif currency_choice == "2":
            maintenance_cost_currency = "USD"
            break

        elif currency_choice == "3":
            maintenance_cost_currency = "NGN"
            break

        else:
            print("Invalid maintenance cost currency. Please select 1, 2, or 3.")

    while True:
        maintenance_cost = input(
            f"Enter maintenance cost ({maintenance_cost_currency}): "
        ).strip()

        try:
            maintenance_cost = float(maintenance_cost)

            if maintenance_cost < 0:
                print("Maintenance cost cannot be negative.")
                continue

            break

        except ValueError:
            print("Invalid cost. Please enter a number.")

    maintenance_record = {
        "id": history_id,
        "work_order_id": None,
        "equipment_id": equipment_id,
        "maintenance_date": maintenance_date,
        "work_performed": work_performed,
        "parts_replaced": parts_replaced,
        "fault_description": fault_description,
        "maintenance_cost_currency": maintenance_cost_currency,
        "maintenance_cost": maintenance_cost
    }

    maintenance_history_list.append(maintenance_record)

    with open("maintenance_history.json", "w") as file:
        json.dump(maintenance_history_list, file, indent=4)

    id_counters["last_history_id"] = history_number

    with open("id_counters.json", "w") as file:
        json.dump(id_counters, file, indent=4)

    print("Maintenance history recorded successfully!")

def view_maintenance_history():
    if not maintenance_history_list:
        print("No maintenance history records found.")
        return

    print("\nMaintenance History Records:")

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

        if cost is None:
            print("Maintenance Cost: Not recorded")
        elif currency is None:
            print("Maintenance Cost:", cost, "(currency not recorded)")
        else:
            print("Maintenance Cost:", cost, currency)

        print("------------------------------")

def update_maintenance_history():
    history_id = input("Enter maintenance history ID to update: ").strip()

    for history in maintenance_history_list:
        if history["id"].casefold() == history_id.casefold():
            print("Maintenance history found!")
            print(history)

            while True:
                print("\nWhat would you like to update?")
                print("1. Maintenance Date")
                print("2. Fault Description")
                print("3. Work Performed")
                print("4. Parts Replaced")
                print("5. Maintenance Cost Currency")
                print("6. Maintenance Cost")
                print("7. Finish Updating")

                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    while True:
                        new_date = input(
                            "Enter new maintenance date (e.g. 19/11/2026 or 2026-11-19): "
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
                                date = datetime.strptime(new_date, date_format)
                                break

                            except ValueError:
                                continue

                        if date is None:
                            print("Invalid date. Please enter a valid date.")
                            continue

                        history["maintenance_date"] = date.strftime("%Y-%m-%d")
                        break

                elif choice == "2":
                    new_value = input(
                        "Enter fault description (press Enter if none): "
                    ).strip()
                    history["fault_description"] = new_value

                elif choice == "3":
                    while True:
                        new_value = input("Enter work performed: ").strip()

                        if new_value == "":
                            print("Work description cannot be empty.")
                            continue

                        history["work_performed"] = new_value
                        break

                elif choice == "4":
                    new_value = input(
                        "Enter parts replaced (press Enter if none): "
                    ).strip()
                    history["parts_replaced"] = new_value

                elif choice == "5":
                    while True:
                        print("\nSelect maintenance cost currency:")
                        print("1. GBP (£)")
                        print("2. USD ($)")
                        print("3. NGN (₦)")

                        currency_choice = input("Enter your choice: ").strip()

                        if currency_choice == "1":
                            history["maintenance_cost_currency"] = "GBP"
                            break
                        elif currency_choice == "2":
                            history["maintenance_cost_currency"] = "USD"
                            break
                        elif currency_choice == "3":
                            history["maintenance_cost_currency"] = "NGN"
                            break
                        else:
                            print("Invalid currency. Please select 1, 2, or 3.")

                elif choice == "6":
                    currency = history.get("maintenance_cost_currency")

                    if currency is None:
                        print("Please select a maintenance cost currency first.")
                        continue

                    while True:
                        new_cost = input(
                            f"Enter new maintenance cost ({currency}): "
                        ).strip()

                        try:
                            new_cost = float(new_cost)

                            if new_cost < 0:
                                print("Maintenance cost cannot be negative.")
                                continue

                            history["maintenance_cost"] = new_cost
                            break

                        except ValueError:
                            print("Invalid cost. Please enter a number.")

                elif choice == "7":
                    print("Finished updating maintenance history.")
                    return

                else:
                    print("Invalid choice. Please select an option from 1 to 7.")
                    continue

                with open("maintenance_history.json", "w") as file:
                    json.dump(maintenance_history_list, file, indent=4)

                print("Maintenance history updated successfully!")

    print("Maintenance history not found. Please check the history ID.")
    
def delete_maintenance_history():
    history_id = input(
        "Enter maintenance history ID to delete: "
    ).strip()

    for history in maintenance_history_list:
        if history["id"].casefold() == history_id.casefold():

            print("Maintenance history found!")
            print(history)

            work_order_id = history.get("work_order_id")

            if work_order_id and str(work_order_id).lower() != "null":
                for work_order in work_order_list:
                    if work_order["id"].casefold() == work_order_id.casefold():
                        if work_order["status"].casefold() == "completed":
                            print(
                                "This maintenance history cannot be deleted "
                                "because it is linked to a completed work order."
                            )
                            return

            while True:
                confirmation = input(
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

def main_menu():
    choice = ""

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
        print("16. Add Maintenance History")
        print("17. View Maintenance History")
        print("18. Update Maintenance History")
        print("19. Delete Maintenance History")
        print("20. Exit")

        choice = input("Enter your choice: ")

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
            add_maintenance_history()
        elif choice == "17":
            view_maintenance_history()
        elif choice == "18":
            update_maintenance_history()
        elif choice == "19":
            delete_maintenance_history()
        elif choice == "20":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

main_menu()       

    