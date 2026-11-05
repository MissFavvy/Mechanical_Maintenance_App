#AI PLUGIN WAS USED TO REVIEW THE CODE BLOCKS

equipment_list = []

equipment = {
    "id": "EQ001",
    "name": "Centrifugal Pump",
    "type": "Pump",
    "location": "Plant Room",
    "temperature": 65,
    "vibration": 4.2,
    "operating_hours": 1200
}

equipment_list.append(equipment)

print(equipment_list)

def add_new_equipment():
    while True:
        equipment_id = input("Enter equipment ID: ")
        duplicate = False
        for existing_equipment in equipment_list:
            if existing_equipment["id"] == equipment_id:
                 duplicate = True
                 print("This equipment ID has already been registered. Please enter another equipment ID.")
        if duplicate == False:
            break
    equipment_name = input("Enter equipment name: ")
    equipment_type = input("Enter equipment type: ")
    equipment_location = input("Enter equipment location: ")

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

def main_menu():
    choice = ""
    while choice != "4":
        print("Welcome to the Equipment Management System")
        print("1. View Equipment List")
        print("2. Add New Equipment")
        print("3. Search Equipment")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            print(equipment_list)
        elif choice == "2":
            add_new_equipment()
        elif choice == "3":
            search_equipment()
        elif choice == "4":
            return
        else:
            print("Invalid choice. Please try again.")

main_menu()
  