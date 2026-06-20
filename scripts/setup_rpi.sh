#!/usr/bin/env bash
# Raspberry Pi Setup Script
#
# This script sets up a Raspberry Pi OS environment.
# It is intended for students in a Raspberry Pi course.
#
# Usage (Run directly from the temporary clone location):
#   chmod +x /tmp/cs350-rpi/scripts/setup_rpi.sh
#   /tmp/cs350-rpi/scripts/setup_rpi.sh
#
# Source:
#   https://www.raspberrypi.com/documentation/computers/os.html#update-software
#
# AI Acknowledgment:
#   This script was developed and refined with the assistance of AI tools
#   to ensure robust error handling, automated backup solutions,
#   and deterministic configuration of virtual development environments.

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
echo "  1. Stage course files and clean temporary directories"
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
    echo "✔ Setup cancelled by user."
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

# Step 1: Remove old files and stage fresh course directories.
echo "Step 1 of 8: Staging course files and cleaning up..."
available_kb=$(df --output=avail / | tail -n 1 | awk '{print $1}')
available_mb=$((available_kb / 1024))
echo "➜ Available space before cleaning: ${available_mb} MB"
echo

# Clean up any generic leftover temporary files from outside our repo clone
rm -rf ~/assets
rm -f ~/README.md
rm -f ~/.gitignore

# --- CRITICAL STUDENT SAFETY CHECK ---
overwrite_course_files="y"

if [ -d ~/cs350 ] || [ -d ~/rpilib ] || [ -d ~/scripts ]; then
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    echo " ⚠️  WARNING: Existing course folders found in your home directory."
    echo " If you have already started working on assignments, proceeding"
    echo " may OVERWRITE and DELETE your progress!"
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    echo
    echo " How would you like to proceed?"
    echo "   1) Create a backup of my work, then deploy fresh files."
    echo "   2) Keep my existing work (Only install/repair tools & environment)."
    echo "   3) Cancel setup entirely."
    echo
    printf "Enter 1, 2, or 3: "
    read -r safety_choice
    echo

    case "$safety_choice" in
        1)
            # Resolve tilde expansion correctly in variables using $HOME
            backup_dir="${HOME}/cs350_backup_$(date +%Y%m%d_%H%M%S)"
            echo "➜ Creating a backup of your current folders to ${backup_dir}..."
            mkdir -p "$backup_dir"
            [ -d ~/cs350 ] && cp -a ~/cs350 "$backup_dir/"
            [ -d ~/rpilib ] && cp -a ~/rpilib "$backup_dir/"
            [ -d ~/scripts ] && cp -a ~/scripts "$backup_dir/"
            echo "✔ Backup complete. Proceeding with fresh file deployment."
            echo
            rm -rf ~/cs350 ~/rpilib ~/scripts
            ;;
        2)
            echo "➜ Skipping file deployment. Your existing code will not be touched."
            echo "➜ Proceeding with tool installation and environment verification..."
            echo
            overwrite_course_files="n"
            ;;
        3|*)
            echo "✔ Setup cancelled to protect your existing work."
            exit 0
            ;;
    esac
fi
# --- END SAFETY CHECK ---

# Only move files out of /tmp/ if the student wanted to overwrite/fresh-install
if [ "$overwrite_course_files" = "y" ]; then
    echo "➜ Deploying fresh course folders from /tmp/cs350-rpi to home directory (~/)..."

    # Double check the clone actually exists where it belongs before modifying anything
    if [ -d /tmp/cs350-rpi ]; then
        cp -a /tmp/cs350-rpi/cs350 ~/
        cp -a /tmp/cs350-rpi/rpilib ~/
        cp -a /tmp/cs350-rpi/scripts ~/
    else
        echo "❌ ERROR: Source repository files not found in /tmp/cs350-rpi."
        echo "Please verify the git clone step completed successfully."
        exit 1
    fi
else
    echo "➜ Maintaining current course directories."
fi

# Clear apt cache to save space
sudo DEBIAN_FRONTEND=noninteractive apt-get clean

available_kb=$(df --output=avail / | tail -n 1 | awk '{print $1}')
available_mb=$((available_kb / 1024))
echo "➜ Available space after cleaning:  ${available_mb} MB"
echo "✔ Done staging course files and cleaning up."
echo

# Step 2: Update the package list.
echo "Step 2 of 8: Updating package list..."
sudo apt-get update
echo "✔ Done updating package list."
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
    echo "⚠️  WARNING: This Raspberry Pi has less free space than recommended."
    echo
    echo "The upgrade may still work, but it could fail if the system runs out of space."
    echo "If you are unsure, choose 'n' and ask for help."
    echo

    printf "Do you want to continue with the upgrade? (y/N): "
    read -r continue_update
    echo

    if [[ "${continue_update,,}" != "y" ]]; then
        echo "✔ Update process cancelled by user. No packages were upgraded."
        exit 0
    fi
fi

echo "✔ Disk space check complete."
echo

# Step 4: Install command-line tools
echo "Step 4 of 8: Installing command-line tools..."
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y direnv
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y gh
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y git
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y shellcheck
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y tree
echo "✔ Done installing command-line tools."
echo

# Step 5: Install Python packages
echo "Step 5 of 8: Installing Python packages..."
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3-full
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3-venv
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3-rpi.gpio
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3-serial
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3-smbus
echo "✔ Done installing Python packages."
echo

# Step 6: Create a Python virtual environment in ~/cs350/.
echo "Step 6 of 8: Creating Python virtual environment..."

mkdir -p ~/cs350
python3 -m venv ~/cs350/.venv
echo "➜ Upgrading system pip infrastructure..."
~/cs350/.venv/bin/python -m pip install --upgrade pip

# Double check that requirements.txt exists; use raw fallback if missing
if [ ! -f ~/cs350/requirements.txt ]; then
    echo "⚠️  requirements.txt not found locally. Fetching backup from GitHub..."
    curl -sSLo ~/cs350/requirements.txt "https://raw.githubusercontent.com/GC-STEM/cs350-rpi/5c2a6695dcc843d0f43220b1a12d09b5d9942868/cs350/requirements.txt"
fi

echo "➜ Installing dependencies from requirements.txt (this may take a few minutes)..."
~/cs350/.venv/bin/python -m pip install -r ~/cs350/requirements.txt

echo "➜ Configuring automatic virtual environment activation..."

# Add the direnv hook to ~/.bashrc if it is not already present.
if ! grep -q 'direnv hook bash' ~/.bashrc; then
    echo '' >> ~/.bashrc
    echo '# Enable direnv for project-specific environment settings.' >> ~/.bashrc
    echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
fi

# Add the standalone prompt decorator to ~/.bashrc if it is not already present.
if ! grep -q 'set_venv_prompt' ~/.bashrc; then
    cat << 'EOF' >> ~/.bashrc

# Automatically prepend virtual environment status to prompt
set_venv_prompt() {
    if [ -n "$VIRTUAL_ENV" ]; then
        local venv_name=\$(basename "\$VIRTUAL_ENV")
        if [[ "\$PS1" != "(\$venv_name) "* ]]; then
            export PS1="(\$venv_name) \$PS1"
        fi
    else
        export PS1="\${PS1#\(*\) }"
    fi
}
if [[ ! "\$PROMPT_COMMAND" =~ set_venv_prompt ]]; then
    export PROMPT_COMMAND="set_venv_prompt;\$PROMPT_COMMAND"
fi
EOF
fi

# Create the direnv configuration file for the CS 350 directory.
cat > ~/cs350/.envrc <<'EOF'
source .venv/bin/activate
EOF

# Approve the .envrc file so direnv can use it.
if cd ~/cs350 2>/dev/null; then
    direnv allow
    cd - >/dev/null || true  # Return cleanly to the previous working directory
else
    echo "⚠️  WARNING: Could not navigate to ~/cs350. Automatic virtual"
    echo "   environment activation (direnv) could not be pre-approved."
    echo "   You may need to run 'cd ~/cs350 && direnv allow' manually later."
    echo
fi

echo "✔ Done creating Python virtual environment."
echo

# Make the scripts in ~/scripts/ executable.
echo "Making setup and update scripts executable..."
chmod +x ~/scripts/setup_rpi.sh
chmod +x ~/scripts/update_rpi.sh
chmod +x ~/scripts/smoke_rpi.sh
echo "✔ Done setting script permissions."
echo

# Step 7: Remove packages and downloaded package files that are no longer needed.
echo "Step 7 of 8: Cleaning up system packages and temporary files..."
echo "➜ Removing unnecessary software dependencies..."
sudo DEBIAN_FRONTEND=noninteractive apt-get autoremove -y
echo "✔ Done removing unnecessary packages."
echo

echo "➜ Purging downloaded package caches and repository clones..."
sudo DEBIAN_FRONTEND=noninteractive apt-get clean
rm -rf /tmp/cs350-rpi
echo "✔ Done cleaning up temporary files."
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
