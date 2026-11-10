#AI PLUGIN WAS USED TO REVIEW THE CODE BLOCKS

import json

with open("equipment_data.json", "r") as file:
    equipment_list = json.load(file)

print(equipment_list)

def add_new_equipment():
    while True:
        equipment_id = input("Enter equipment ID: ").strip()
        if equipment_id == "":
            print("Equipment ID cannot be empty. Please try again.")
            continue
        duplicate = False
        for existing_equipment in equipment_list:
            if existing_equipment["id"] == equipment_id:
                 duplicate = True
                 print("This equipment ID has already been registered. Please enter another equipment ID.")
        if duplicate == False:
            break

    while True:
        equipment_name = input("Enter equipment name: ").strip()
        if equipment_name == "":
            print("Equipment name cannot be empty. Please try again.")
            continue
        break

    while True:
        equipment_type = input("Enter equipment type: ").strip()
        if equipment_type == "":
            print("Equipment type cannot be empty. Please try again.")
            continue
        break

    while True:
        equipment_location = input("Enter equipment location: ").strip()
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
    search_id = input("Enter equipment ID to search: ")
    found = False

    for equipment in equipment_list:
        if equipment["id"] == search_id:
            print("Equipment found!")
            print(equipment)
            found = True

    if found == False:
        print("Equipment not found. Please check the equipment ID.")


def update_equipment_details():
    equipment_id = input("Enter the equipment ID you want to update: ")
    found = False

    for equipment in equipment_list:
        if equipment["id"] == equipment_id:
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
                equipment["name"] = input("Enter new equipment name: ")

            elif choice == "2":
                equipment["type"] = input("Enter new equipment type: ")

            elif choice == "3":
                equipment["location"] = input("Enter new equipment location: ")

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
                    )

                    if new_value == "":
                        equipment[field] = None
                        break

                    try:
                        equipment[field] = float(new_value)
                        break

                    except ValueError:
                        print(f"Invalid {field_name}. Please enter a number.")

            else:
                print("Invalid update choice.")
                return

            print("Equipment details updated successfully!")

            with open("equipment_data.json", "w") as file:
                json.dump(equipment_list, file, indent=4)

            print(equipment)
            break

    if found == False:
        print("Equipment not found. Please check the equipment ID.")

def delete_equipment():
    equipment_id = input("Enter the equipment ID you want to delete: ")
    found = False

    for equipment in equipment_list:
        if equipment["id"] == equipment_id:
            found = True
            print("Equipment found!")
            print(equipment)

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

def main_menu():
    choice = ""

    while choice != "6":
        print("Welcome to the Equipment Management System")
        print("1. View Equipment List")
        print("2. Add New Equipment")
        print("3. Search Equipment")
        print("4. Update Equipment Details")
        print("5. Delete Equipment")
        print("6. Exit")

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
            return
        else:
            print("Invalid choice. Please try again.")

main_menu()
  