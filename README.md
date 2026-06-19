# CS 350 – Raspberry Pi Repository

<!-- To see this file in a clean, formatted view, right-click on the filename and choose “Open Preview.” -->

## Prerequisites

Before you use this repository, complete these tasks:

1. Assemble your Raspberry Pi.
2. Create the bootable microSD card.
3. Power on your Raspberry Pi.
4. Connect your Raspberry Pi to the same network as your main computer.

## Getting Started

Follow these steps from a terminal window on your main computer. First, you will connect to your Raspberry Pi using Secure Shell (SSH). SSH lets you use your Raspberry Pi command line from another computer on the same network. After you connect, the remaining commands will run on the Raspberry Pi.

**1. Connect to your Raspberry Pi.** Open a terminal on your main computer and run the command below. If you have not changed the default settings, copy the following command and paste it into your terminal. If you changed the recommended username or hostname, replace `stu` and `rpi` with your values and type the command accordingly:

```bash
ssh stu@rpi.local
```

![TODO: Add gif screenshot of SSH connection](./assets/images/TODO_add_filename.gif)

If this is your first time connecting to the Raspberry Pi, you may be asked to accept the Raspberry Pi SSH host key. Type `yes` to accept and continue. The host key helps your computer recognize that it is connecting to the same Raspberry Pi in the future.

You will then be prompted to enter the password for your Raspberry Pi user account. The cursor will not move as you type the password. After you enter the password, press `Enter` to continue. If the username, hostname, or password are incorrect, you will see an error message and will need to try again.

*Note.* Use the hostname, username, and password values you set in **Raspberry Pi Imager** when you created the bootable microSD card. If you do not have this information, open the **Raspberry Pi Imager** and follow the instructions to get to the Customization section. It should have saved your settings. If not, you will need to run the imager again to on your microSD card. Be sure to note the hostname, username, and password for future use.

**2. Download the repository files.** After you connect to your Raspberry Pi and have a prompt that looks like `stu@rpi:~$`, copy all the commands below to your clipboard. Then, paste the following commands into the Raspberry Pi terminal prompt. These commands perform the following actions on your Raspberry Pi:

1. Update the package list and install Git, a version control tool used to download files from GitHub.
2. Download the repository into a temporary directory named `/tmp/cs350-rpi`.
3. Copy the course files into your home directory (`~/`).
4. Remove the temporary repository copy.
5. Display the contents of your home directory.

```bash
sudo apt update && sudo apt install -y git tree
git clone https://github.com/GC-STEM/cs350-rpi.git /tmp/cs350-rpi
cp -a /tmp/cs350-rpi/cs350 ~/
cp -a /tmp/cs350-rpi/rpilib ~/
cp -a /tmp/cs350-rpi/scripts ~/
rm -rf /tmp/cs350-rpi
tree -L 2 ~/

```

After the commands finish, you should see these sub-directories and files in your home directory of your Raspberry Pi:

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
│   └── __init__.py      # Initialize the library
│
├── scripts/             # Reusable Raspberry Pi shell scripts
│   ├── setup_rpi.sh     # Set up Raspberry Pi environment
│   ├── smoke_rpi.sh     # Run smoke tests on Raspberry Pi
│   └── update_rpi.sh    # Update Raspberry Pi environment
│
└── requirements.txt     # Course Python dependencies
```
*Note.* This repository and your RPi home directory includes hidden files and directories not listed in this directory structure. These files support maintenance, documentation, testing, or version control. Do not modify those files or directories. Focus on the course directories and files listed above.

**3. Run the setup script.** After downloading the repository files, run the following commands to start the Raspberry Pi setup script.

```bash
chmod +x ~/scripts/setup_rpi.sh
~/scripts/setup_rpi.sh
```

The setup script installs required software packages and configures the Raspberry Pi environment for the course activities.

![TODO: Add gif screenshot of setup script](./assets/images/TODO_add_filename.gif)

## Troubleshooting

{{TODO: Add troubleshooting tips for common issues.}}

## AI Acknowledgment

{{TODO: Add SNHU standard AI acknowledgment statement.}}
