#!/usr/bin/env bash
# Raspberry Pi Update Script
#
# This script updates Raspberry Pi OS system packages. It is intended for
# students in a Raspberry Pi course, but it can be used by anyone who wants to
# update their Raspberry Pi.
#
# Usage:
#   chmod +x scripts/update_rpi.sh
#   ./scripts/update_rpi.sh
#
# Source:
#   https://www.raspberrypi.com/documentation/computers/os.html#update-software
#
# AI Acknowledgment:
#   This script was refined with the assistance of AI tools to maintain
#   parity with the environment configuration script, ensuring optimized
#   terminal execution, automated sudo persistence loops, and standardized logging.

set -e

# This script should be run as the normal user, not sudo.
# It uses sudo only for commands that need administrator access.
if [ "$EUID" -eq 0 ]; then
    echo "❌ ERROR: Do not run this script with sudo."
    echo
    echo "Use:"
    echo "  ./update_rpi.sh"
    echo
    echo "The script will ask for your password when administrator access is needed."
    exit 1
fi

# Script settings.
# These values are used for disk-space checks and SSH reconnect instructions.
RPI_USER="${USER}"
RPI_HOSTNAME="$(hostname)"
MIN_FREE_KB=1048576
FREE_SPACE_PERCENT=10

echo "========================================"
echo " Raspberry Pi System Update"
echo "========================================"
echo
echo "This script will:"
echo "  1. Remove old downloaded package files"
echo "  2. Update the package list"
echo "  3. Check available disk space"
echo "  4. Upgrade installed system packages"
echo "  5. Remove packages and files that are no longer needed"
echo "  6. Reboot, shut down, or return to the command prompt"
echo

printf "Do you wish to continue with the update? (y/N): "
read -r continue_update
echo

if [[ "${continue_update,,}" != "y" ]]; then
    echo "✔ Update cancelled by user."
    exit 0
fi

# Ask for the sudo password near the beginning.
echo "➜ Checking administrator access..."
sudo -v
echo "✔ Administrator access confirmed."
echo

# --- KEEP-ALIVE LOOP FOR SUDO ---
# Update the existing sudo timestamp every 60 seconds in the background.
while true; do
    sudo -n true
    sleep 60
    kill -0 "$$" 2>/dev/null || exit
done &
SUDO_LOOP_PID=$!

# Ensure the background loop is terminated when the script exits or is interrupted
trap 'kill -0 "$SUDO_LOOP_PID" 2>/dev/null && kill "$SUDO_LOOP_PID"' EXIT
# --------------------------------

# Step 1: Remove old downloaded package files.
echo "Step 1 of 6: Cleaning old downloaded package files..."
available_kb=$(df --output=avail / | tail -n 1 | awk '{print $1}')
available_mb=$((available_kb / 1024))
echo "➜ Available space before cleaning: ${available_mb} MB"
echo

sudo apt-get clean

available_kb=$(df --output=avail / | tail -n 1 | awk '{print $1}')
available_mb=$((available_kb / 1024))
echo "➜ Available space after cleaning:  ${available_mb} MB"
echo "✔ Done cleaning old downloaded package files."
echo

# Step 2: Update the package list.
echo "Step 2 of 6: Updating package list..."
sudo apt-get update
echo "✔ Done updating package list."
echo

# Step 3: Check available disk space before upgrading.
echo "Step 3 of 6: Checking available disk space..."

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
    echo "⚠️  WARNING: This Raspberry Pi has less free space than recommended."
    echo
    echo "The upgrade may still work, but it could fail if the system runs out of space."
    echo "If you are unsure, choose 'n' and ask for help."
    echo

    printf "Do you want to continue with the upgrade? (y/N): "
    read -r continue_upgrade_anyway
    echo

    if [[ "${continue_upgrade_anyway,,}" != "y" ]]; then
        echo "✔ Update process cancelled by user. No packages were upgraded."
        exit 0
    fi
fi

echo "✔ Disk space check complete."
echo

# Step 4: Upgrade installed packages.
# apt-get dist-upgrade is the script-friendly form of a full system upgrade.
echo "Step 4 of 6: Upgrading installed packages..."
echo "➜ This step may take several minutes. Please wait..."
sudo DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y
echo "✔ Done upgrading packages."
echo

# Step 5: Remove packages and downloaded package files that are no longer needed.
echo "Step 5 of 6: Cleaning up system packages and temporary files..."
echo "➜ Removing unnecessary software dependencies..."
sudo DEBIAN_FRONTEND=noninteractive apt-get autoremove -y
echo "✔ Done removing unnecessary packages."
echo

echo "➜ Purging downloaded package caches..."
sudo DEBIAN_FRONTEND=noninteractive apt-get clean
echo "✔ Done cleaning up temporary files."
echo

# Show available disk space after finishing.
available_kb=$(df --output=avail / | tail -n 1 | awk '{print $1}')
available_mb=$((available_kb / 1024))

echo "========================================"
echo " Update Complete"
echo "========================================"
echo "Available space on /: ${available_mb} MB"
echo

# Step 6: Let the student choose what to do next.
echo "Step 6 of 6: Choose what to do next."
echo
echo "   1. Reboot the Raspberry Pi"
echo "   2. Shut down the Raspberry Pi"
echo "   3. Return to the command prompt"
echo

printf "Enter 1, 2, or 3: "
read -r choice
echo

case "$choice" in
    1)
        echo "➜ The Raspberry Pi will reboot now."
        echo
        echo "⚠️  If you are connected by SSH, this connection will close."
        echo "Wait until the Raspberry Pi has fully restarted, then reconnect with:"
        echo
        printf "  ssh %s@%s.local\n\n" "$RPI_USER" "$RPI_HOSTNAME"
        sudo reboot
        ;;
    2)
        echo "➜ The Raspberry Pi will shut down now."
        echo
        echo "⚠️  If you are connected by SSH, this connection will close."
        echo "To use the Raspberry Pi again, you may need to unplug and reconnect power."
        echo
        sudo shutdown -h now
        ;;
    3|*)
        echo "✔ Returning to the command prompt."
        echo "No reboot or shutdown was started."
        ;;
esac