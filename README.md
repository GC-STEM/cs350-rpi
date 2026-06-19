# CS 350 – Raspberry Pi Repository

<!-- To see this file in a clean, formatted view, right-click on the filename and choose “Open Preview.” -->

## ⚠️ Under Construction

This repository is incomplete and under active development. Code, documentation, structure, and features may change frequently. Use with caution, and check back for updates.

## Prerequisites

Before you can use the repository, you need to have completed the following tasks:

1. Assembled your Raspberry Pi
2. Created the bootable microSD card
3. Powered on your Raspberry Pi
4. Connected your Raspberry Pi to the same network as your computer

## Getting Started

On your main computer, follow the steps below. You will perform all these steps in a terminal window on your main computer that is connected to the same network as your Raspberry Pi. After you complete these steps, your Raspberry Pi will be ready to help you complete all course activities.

1. **Connect to your Raspberry Pi**. Open a terminal on your computer and run the following command to connect to your Raspberry Pi via Secure Shell (SSH). Replace `username` with your actual username on the Raspberry Pi, and `hostname` with the hostname of your Raspberry Pi. If this is your first time connecting, you may be prompted to accept the Raspberry Pi's SSH key.

```bash
ssh username@hostname
```

*Note*. Use set username and hostname values when you ran the **Raspberry Pi Imager** to create the bootable microSD card. If you are unsure of your Raspberry Pi's hostname, you can use the `hostname` command on the Raspberry Pi terminal to find it.

2. **Download the repository**. Copy the following commands and paste them into your terminal window to copy this repository directly into your home directory (`~/`) on your Raspberry Pi. Make sure you copy and paste the commands exactly as shown. :

```bash
sudo apt update && sudo apt install -y git
git clone https://github.com/GC-STEM/cs350-rpi.git /tmp/cs350-rpi && cp -a /tmp/cs350-rpi/. ~/
ls ~/
```

These commands will will perform the following actions on your Raspberry Pi:
    1. Update the package list and install Git version control;
    2. Create a temporary directory (`/tmp/cs350-rpi`) to hold the repository;
    3. Copy all the files from that temporary directory to your home directory;
    4. Display the contents of your home directory. You should see the `cs350`, `rpilib`, and `scripts` directories.

3. **Run the setup script**. After downloading the repository, run the following command to execute the setup script. This script will install necessary dependencies and perform any required configuration for the course activities.

```bash
chmod +x setup_rpi.sh
./setup_rpi.sh
```

## Repository Overview

### Repository Structure

The course repository is organized so the main directories are placed directly in your Raspberry Pi home folder (`~/`). After you download the repository files, you should see the directories shown below in your home directory. The `cs350` folder contains the course activity files, `rpilib` contains reusable Raspberry Pi Python code, and `scripts` contains helper scripts used to set up, test, or update your Raspberry Pi environment.

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
│   ├── setup_rpi.sh     # Set up Raspberry Pi environment
│   ├── smoke_rpi.sh     # Run smoke tests on Raspberry Pi
│   └── update_rpi.sh    # Update Raspberry Pi environment
│
├── README.md            # Repository overview
└── requirements.txt     # Course Python dependencies
```

*Note.* This repository may include additional files and directories not listed in the main repository structure. These files support repository maintenance, documentation, testing, or version control. Unless your instructor tells you otherwise, do not modify those files. Focus on the course directories and files listed above.

## Troubleshooting

{{TODO: Add troubleshooting tips for common issues.}}

## AI Acknowledgment

{{TODO: Add SNHU standard AI acknowledgment statement.}}
