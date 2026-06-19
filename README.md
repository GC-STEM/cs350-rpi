# CS 350 – Raspberry Pi Repository

<!-- To see this file in a clean, formatted view, right-click on the filename and choose “Open Preview.” -->

## ⚠️ Under Construction

This repository is incomplete and under active development. Code, documentation, structure, and features may change frequently. Use with caution, and check back for updates.

## Repository Overview

### Repository Structure

The course repository is organized so the main folders are placed directly in your Raspberry Pi home folder (`~/`). After you download or clone the repository files, you should see the folders shown below in your home directory. The `cs350` folder contains the course activity files, `rpilib` contains reusable Raspberry Pi Python code, and `scripts` contains helper scripts used to set up, test, or update your Raspberry Pi environment.

```text
~/
│
├── cs350/               # Course materials for CS 350
│   ├── m1/              # Module 1 | Assignment: Prepare Your Raspberry Pi
│   ├── m2/              # Module 2 | Milestone 1: PWM Lab
│   ├── m3/              # Module 3 | Milestone 2: UART Lab
│   ├── m4/              # Module 4 | Assignment: Wiring LCD
│   ├── m5/              # Module 5 | Milestone 3: Button Input Lab
│   ├── m6/              # Module 6 | Assignment: Add Sensor
│   └── m7/              # Module 7 | Final Project: Thermostat Lab
│
├── rpilib/              # Reusable Python library for Raspberry Pi
│   ├── <package>/       # Package(s) for related Raspberry Pi helper modules
│   │   ├── __init__.py  # Initialize the package
│   │   └── <module>.py  # Module(s) for specific functionality
│   └── __init__.py      # Initialize the library
│
├── scripts/             # Reusable Raspberry Pi shell scripts
│   ├── setup.sh         # Set up Raspberry Pi environment
│   ├── smoke.sh         # Run smoke tests on Raspberry Pi
│   └── update.sh        # Update Raspberry Pi environment
│
├── .gitignore           # Excludes local/generated files from version control
├── README.md            # Repository overview
└── requirements.txt     # Course Python dependencies
```

*Note.* This repository may include additional files and folders not listed in the main repository structure. These files support repository maintenance, documentation, testing, or version control. Unless your instructor tells you otherwise, do not modify those files. Focus on the course folders and files listed above.


```text
~/
│
├── cs350/               # Course materials for CS 350
│   ├── m1/              # Module 1 | Assignment: Prepare your Raspberry Pi
│   ├── m2/              # Module 2 | Milestone 1: PWM Lab
│   ├── m3/              # Module 3 | Milestone 2: UART Lab
│   ├── m4/              # Module 4 | Assignment: Wiring LCD
│   ├── m5/              # Module 5 | Milestone 3: Button input Lab
│   ├── m6/              # Module 6 | Assignment: Add sensor
│   └── m7/              # Module 7 | Final Project: Thermostat Lab
│
├── rpilib/              # Reusable Python library for Raspberry Pi
│   ├── <package>        # Package(s) for related Raspberry Pi helper modules
│   │   ├── __init__.py  # Initialize the package
│   │   └── <module>.py  # Module(s) for specific functionality
│   └── __init__.py      # Initialize the library
│
├── scripts/             # Reusable Raspberry Pi shell scripts
│   ├── setup.sh         # Set up RPi environment
│   ├── smoke.sh         # Run smoke tests on RPi
│   └── update.sh        # Update RPi environment
│
├── .gitignore           # Excludes local/generated files from version control
├── README.md            # Repository overview (not copied to Raspberry Pi)
└── requirements.txt     # Course Python dependencies

```

*Note*. This repository may include additional files and folders not listed in the main repository structure. These folders and files are essential for maintaining a well-organized and high-quality codebase, but they are not meant to be modified by students. Just ignore these as you work and focus on the main repository files listed above.
