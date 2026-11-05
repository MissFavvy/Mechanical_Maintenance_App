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


def main_menu():
    choice = ""
    while choice != "3":
        print("Welcome to the Equipment Management System")
        print("1. View Equipment List")
        print("2. Add New Equipment")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            print(equipment_list)
        elif choice == "2":
            add_new_equipment()
        elif choice == "3":
            return
        else:
            print("Invalid choice. Please try again.")

main_menu()
  