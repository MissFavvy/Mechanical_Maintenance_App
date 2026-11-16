#AI PLUGIN WAS USED TO REVIEW THE CODE BLOCKS

import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

with open("equipment_data.json", "r") as file:
    equipment_list = json.load(file)

print(equipment_list)

with open("work_orders.json", "r") as file:
    work_order_list = json.load(file)

print(work_order_list)

with open("maintenance_schedule.json", "r") as file:
    maintenance_schedule_list = json.load(file)

print(maintenance_schedule_list)

def add_new_equipment():
    while True:
        equipment_id = input("Enter equipment ID: ").strip().upper()
        if equipment_id == "":
            print("Equipment ID cannot be empty. Please try again.")
            continue
        duplicate = False
        for existing_equipment in equipment_list:
            if existing_equipment["id"].casefold() == equipment_id.casefold():
                 duplicate = True
                 print("This equipment ID has already been registered. Please enter another equipment ID.")
        if duplicate == False:
            break

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
    while True:
        work_order_id = input("Enter work order ID: ").strip().upper()
        if work_order_id == "":
            print("Work order ID cannot be empty. Please try again.")
            continue
        duplicate = False
        for existing_work_order in work_order_list:
            if existing_work_order["id"].casefold() == work_order_id.casefold():
                 duplicate = True
                 print("This work order ID has already been registered. Please enter another work order ID.")
        if duplicate == False:
            break
    
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
    while True:
        schedule_id = input("Enter maintenance schedule ID: ").strip().upper()

        if schedule_id == "":
            print("Maintenance schedule ID cannot be empty. Please try again.")
            continue

        duplicate = False

        for schedule in maintenance_schedule_list:
            if schedule["id"].casefold() == schedule_id.casefold():
                duplicate = True
                print("This maintenance schedule ID already exists. Please enter another ID.")
                break

        if not duplicate:
            break

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
        last_maintenance_date = input("Enter last maintenance date (YYYY-MM-DD or DD-MM-YYYY): ").strip()

        try:
            date = datetime.strptime(last_maintenance_date, "%Y-%m-%d")

        except ValueError:
            try:
                date = datetime.strptime(last_maintenance_date, "%d-%m-%Y")

            except ValueError:
                print("Invalid date. Please use YYYY-MM-DD or DD-MM-YYYY.")
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
        maintenance_interval = input(f"Enter maintenance interval ({interval_unit}): ").strip()

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

def main_menu():
    choice = ""

    while choice != "13":
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
        print("13. Exit")

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
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

main_menu()       

    