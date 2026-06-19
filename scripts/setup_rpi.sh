#!/usr/bin/env bash
# Raspberry Pi Setup Script
#
# This script sets up a Raspberry Pi OS environment.
# It is intended for students in a Raspberry Pi course.
#
# Usage:
#   chmod +x scripts/setup_rpi.sh
#   ./scripts/setup_rpi.sh
#
# Source:
#   https://www.raspberrypi.com/documentation/computers/os.html#update-software

# Script settings.
# These values are used for disk-space checks and SSH reconnect instructions.
RPI_USER="${USER}"
RPI_HOSTNAME="$(hostname)"
MIN_FREE_KB=1048576
FREE_SPACE_PERCENT=10

echo "========================================"
echo " Raspberry Pi System Setup"
echo "========================================"
echo
echo "This script will:"
echo "  1. Remove unnecessary files"
echo "  2. Update the package list"
echo "  3. Check available disk space"
echo "  4. Install command-line tools"
echo "  5. Install Python packages"
echo "  6. Create a Python virtual environment"
echo "  7. Remove package files that are no longer needed"
echo "  8. Reboot, shut down, or return to the command prompt"
echo

printf "Do you wish to continue with the setup? (y/N): "
read -r continue_setup
echo

if [[ "${continue_setup,,}" != "y" ]]; then
    echo "Setup cancelled by user."
    exit 0
fi

# Ask for the sudo password near the beginning.
echo "Checking administrator access..."
sudo -v
echo "Administrator access confirmed."
echo

# Step 1: Remove old files and stage fresh course directories.
echo "Step 1 of 8: Staging fresh course files and cleaning up..."
available_kb=$(df --output=avail / | tail -n 1 | awk '{print $1}')
available_mb=$((available_kb / 1024))
echo "Available space before cleaning: ${available_mb} MB"
echo

# Clean up any leftover temporary files from previous runs
rm -rf /tmp/cs350-rpi
rm -rf ~/assets
rm -f ~/README.md
rm -f ~/.gitignore

# Ensure git is installed so we can fetch the repository
if ! command -v git &> /dev/null; then
    echo "Installing git to fetch course repository..."
    sudo apt-get update
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y git
fi

echo "Fetching the latest course files from GitHub..."
git clone https://github.com/GC-STEM/cs350-rpi.git /tmp/cs350-rpi

# Safely copy directories to the home folder
echo "Setting up course folders (~/cs350, ~/rpilib, ~/scripts)..."
mkdir -p ~/cs350 ~/rpilib ~/scripts
cp -a /tmp/cs350-rpi/cs350 ~/
cp -a /tmp/cs350-rpi/rpilib ~/
cp -a /tmp/cs350-rpi/scripts ~/

# Clean up the temporary clone repository
rm -rf /tmp/cs350-rpi

# Clear apt cache to save space
sudo DEBIAN_FRONTEND=noninteractive apt-get clean

available_kb=$(df --output=avail / | tail -n 1 | awk '{print $1}')
available_mb=$((available_kb / 1024))
echo "Available space after cleaning:  ${available_mb} MB"
echo "Done staging course files and cleaning up."
echo

# Step 2: Update the package list.
echo "Step 2 of 8: Updating package list..."
sudo apt-get update
echo "Done updating package list."
echo

# Step 3: Check available disk space before upgrading.
echo "Step 3 of 8: Checking available disk space..."

total_kb=$(df --output=size / | tail -n 1 | awk '{print $1}')
available_kb=$(df --output=avail / | tail -n 1 | awk '{print $1}')

total_mb=$((total_kb / 1024))
available_mb=$((available_kb / 1024))
free_percent=$((available_kb * 100 / total_kb))
percent_recommended_kb=$((total_kb * FREE_SPACE_PERCENT / 100))

# Use the larger recommendation: 1 GB free or 10% free space.
if [ "$percent_recommended_kb" -gt "$MIN_FREE_KB" ]; then
    recommended_kb="$percent_recommended_kb"
else
    recommended_kb="$MIN_FREE_KB"
fi

recommended_mb=$((recommended_kb / 1024))

printf "%-22s %d MB\n" "Total space on /:"     "$total_mb"
printf "%-22s %d MB\n" "Available space on /:" "$available_mb"
printf "%-22s %d%%\n"  "Free space:"           "$free_percent"
printf "%-22s %d MB\n" "Recommended minimum:"  "$recommended_mb"
echo

if [ "$available_kb" -lt "$recommended_kb" ]; then
    echo "WARNING: This Raspberry Pi has less free space than recommended."
    echo
    echo "The upgrade may still work, but it could fail if the system runs out of space."
    echo "If you are unsure, choose 'n' and ask for help."
    echo

    printf "Do you want to continue with the upgrade? (y/N): "
    read -r continue_update
    echo

    if [[ "${continue_update,,}" != "y" ]]; then
        echo "Update process cancelled by user."
        echo "No packages were upgraded."
        exit 0
    fi
fi

echo "Disk space check complete."
echo

# Step 4: Install command-line tools
echo "Step 4 of 8: Installing command-line tools..."
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y direnv gh git shellcheck tree
echo "Done installing command-line tools."

# Step 5: Install Python packages
echo "Step 5 of 8: Installing Python packages..."
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3-full python3-venv python3-pip
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3-rpi.gpio python3-serial python3-smbus
echo "Done installing Python packages."

# Step 6: Create a Python virtual environment in ~/cs350/.
echo "Step 6 of 8: Creating Python virtual environment..."

mkdir -p ~/cs350
python3 -m venv ~/cs350/.venv
~/cs350/.venv/bin/python -m pip install --upgrade pip

# Double check that requirements.txt exists; use raw fallback if missing
if [ ! -f ~/cs350/requirements.txt ]; then
    echo "requirements.txt not found locally. Fetching backup from GitHub..."
    curl -sSLo ~/cs350/requirements.txt "https://raw.githubusercontent.com/GC-STEM/cs350-rpi/5c2a6695dcc843d0f43220b1a12d09b5d9942868/cs350/requirements.txt"
fi

echo "Installing pip dependencies (this may take a few minutes)..."
~/cs350/.venv/bin/python -m pip install -r ~/cs350/requirements.txt

echo "Configuring automatic virtual environment activation..."

# Add the direnv hook to ~/.bashrc if it is not already present.
if ! grep -q 'direnv hook bash' ~/.bashrc; then
    echo '' >> ~/.bashrc
    echo '# Enable direnv for project-specific environment settings.' >> ~/.bashrc
    echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
fi

# Create the direnv configuration file for the CS 350 directory.
cat > ~/cs350/.envrc <<'EOF'
source .venv/bin/activate
EOF

# Approve the .envrc file so direnv can use it.
cd ~/cs350 || { echo "ERROR: Could not navigate to ~/cs350"; exit 1; }
direnv allow

echo "Done creating Python virtual environment."
echo

# Step 7: Remove packages and downloaded package files that are no longer needed.
echo "Step 7 of 8: Removing packages that are no longer needed..."
sudo DEBIAN_FRONTEND=noninteractive apt-get autoremove -y
echo "Done removing unnecessary packages."
echo

echo "Cleaning up downloaded package files..."
sudo DEBIAN_FRONTEND=noninteractive apt-get clean
echo "Done cleaning up downloaded package files."
echo

# Show available disk space after finishing.
available_kb=$(df --output=avail / | tail -n 1 | awk '{print $1}')
available_mb=$((available_kb / 1024))

echo "========================================"
echo " Setup Complete"
echo "========================================"
echo "Available space on /: ${available_mb} MB"
echo

# Step 8: Let the student choose what to do next.
echo "Step 8 of 8: Choose what to do next."
echo
echo "  1. Reboot the Raspberry Pi"
echo "  2. Shut down the Raspberry Pi"
echo "  3. Return to the command prompt"
echo

printf "Enter 1, 2, or 3: "
read -r choice
echo

case "$choice" in
    1)
        echo "The Raspberry Pi will reboot now."
        echo
        echo "If you are connected by SSH, this connection will close."
        echo "Wait until the Raspberry Pi has fully restarted, then reconnect with:"
        echo
        printf "  ssh %s@%s.local\n\n" "$RPI_USER" "$RPI_HOSTNAME"
        sudo reboot
        ;;
    2)
        echo "The Raspberry Pi will shut down now."
        echo
        echo "If you are connected by SSH, this connection will close."
        echo "To use the Raspberry Pi again, you may need to unplug and reconnect power."
        echo
        sudo shutdown -h now
        ;;
    3|*)
        echo "Returning to the command prompt."
        echo "No reboot or shutdown was started."
        ;;
esac
