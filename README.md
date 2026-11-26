# Mechanical Maintenance Management System

## Project Overview

The Mechanical Maintenance Management System is a Python application developed to manage industrial equipment, maintenance work orders, preventive maintenance schedules and maintenance history.

The project was developed as part of the CSC-44102 Foundations of Programming and Software Engineering module at Keele University.

The application has two versions:

- Command-Line Interface (CLI)
- Graphical User Interface (GUI) using Tkinter

Both versions use JSON files to store and retrieve maintenance records.

## Project Aims

The project aims to:

- Provide a central system for managing equipment records.
- Record equipment faults and track maintenance work orders.
- Schedule preventive maintenance and identify overdue maintenance tasks.
- Maintain records of completed repairs, replaced parts and maintenance costs.
- Provide both text-based and graphical interfaces for managing maintenance activities.
- Retain saved records after closing and restarting the application.

## Application Features

### 1. Equipment Management

- Register new equipment with automatically generated equipment IDs.
- View, search, update and delete equipment records.
- Record equipment name, type, location, temperature, vibration and operating hours.
- Prevent the deletion of equipment with linked maintenance records.

### 2. Maintenance Work Orders

- Create work orders for registered equipment.
- Record equipment faults and assign priority levels.
- Track work order status as Pending, In Progress or Completed.
- View, search, update and delete work orders.
- Automatically create a maintenance history record when a work order is completed.
- Prevent completed work orders with linked maintenance history from being updated or deleted.

### 3. Preventive Maintenance Scheduling

- Create maintenance schedules for registered equipment.
- Set maintenance intervals in days, months or years.
- Automatically calculate the next maintenance date.
- Identify maintenance tasks as Upcoming, Due Today or Overdue.
- View, search, update and delete maintenance schedules.

### 4. Maintenance History

- View and search completed maintenance records.
- Record maintenance dates, faults, work performed and parts replaced.
- Record maintenance costs in GBP, USD or NGN.
- Update maintenance history records.
- Protect records linked to completed work orders from deletion.

### 5. Data Storage and Input Validation

- Automatically save records in JSON files.
- Retain records after restarting the application.
- Generate unique IDs for each record.
- Validate user inputs.
- Allow users to cancel operations without saving unwanted changes.

## Technologies and Libraries Used

### Programming Language

- Python – Used to develop both the command-line and graphical versions of the application.

### Python Libraries

- JSON – Used to store, load and update maintenance records.
- Tkinter – Used to develop the graphical user interface.
- ttk – Used to create GUI tables, buttons and selection fields.
- messagebox – Used to display confirmation, success and error messages.
- datetime – Used to handle maintenance dates.
- timedelta – Used to calculate maintenance intervals in days.
- python-dateutil – Used to calculate maintenance intervals in months and years.

### Development Tools

- Visual Studio Code – Used for writing, editing and testing the application.
- Git – Used for version control and tracking changes during development.
- GitHub – Used to store and manage the project repository.

## Installation Requirements

Before running the application, ensure that the following are available:

- Python 3
- pip (Python package installer)
- Tkinter
- Git (if cloning the repository)

### Step 1: Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/MissFavvy/Mechanical_Maintenance_App.git
```

### Step 2: Open the Project Directory

```bash
cd Mechanical_Maintenance_App
```

### Step 3: Install the Required Dependency

```bash
python -m pip install -r requirements.txt
```

For Windows users using the Python launcher:

```bash
py -m pip install -r requirements.txt
```

The requirements.txt file contains the external library (python-dateutil) required for maintenance date calculations.

## Running the Application

Ensure that the terminal is open in the project directory before running either version of the application.

### Command-Line Interface (CLI)

To launch the text-based version, run:

```bash
python main.py
```

Alternatively, on Windows:

```bash
py main.py
```

The application displays a numbered menu containing the equipment management, maintenance work orders, preventive maintenance scheduling and maintenance history options.

Enter the number corresponding to the required operation. Select option 20 to exit the application.

### Graphical User Interface (GUI)

To launch the graphical version, run:

```bash
python gui.py
```

Alternatively, on Windows:

```bash
py gui.py
```

The main window provides access to four sections:

- Equipment Management
- Maintenance Work Orders
- Preventive Maintenance Scheduling
- Maintenance History

Users can navigate through the application using buttons, input fields, selection menus and tables.

Both versions use the same JSON files, allowing saved records to be accessed from either interface.

## Project File Structure

```text
Mechanical_Maintenance_App/
│
├── main.py
├── gui.py
├── equipment_data.json
├── work_orders.json
├── maintenance_schedule.json
├── maintenance_history.json
├── id_counters.json
├── requirements.txt
├── .gitignore
└── README.md
```

| File | Description |
| --- | --- |
| main.py | Contains the command-line version of the application. |
| gui.py | Contains the graphical version of the application. |
| equipment_data.json | Stores registered equipment details. |
| work_orders.json | Stores maintenance work orders, faults, priorities and statuses. |
| maintenance_schedule.json | Stores preventive maintenance schedules and maintenance dates. |
| maintenance_history.json | Stores maintenance history, repairs, replaced parts and costs. |
| id_counters.json | Keeps track of the last generated IDs for each record type. |
| requirements.txt | Lists the external Python dependency required to run the application. |
| .gitignore | Excludes unnecessary Python cache files from version control. |
| README.md | Provides project documentation and instructions for running the application. |

## Data Storage

The application uses JSON files for persistent data storage.

Both the CLI and GUI versions access the same JSON files. Records are saved when users confirm additions, updates or permitted deletions.

Previously saved records are loaded when the application is restarted.

The id_counters.json file keeps track of generated IDs to prevent duplicate IDs and the reuse of deleted record IDs.

## Sample Data Disclaimer

The equipment types used in this application reflect equipment commonly found in industrial environments.

However, the equipment details, operating readings, maintenance work orders, schedules, maintenance history and costs are fictional records created for application development, testing and demonstration purposes.

The data was not obtained from any company and does not contain confidential company information.

## GenAI Acknowledgement

I acknowledge the use of ChatGPT (GPT-6.2, OpenAI, https://chatgpt.com/) to assist with writing and structuring this README and providing guidance on Git and GitHub.