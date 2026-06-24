#!/usr/bin/env bash
# Raspberry Pi Verification Script
#
# This script verifies that the Raspberry Pi OS environment appears to have
# been configured correctly by the CS 350 setup script. It checks course files,
# system tools, Python packages, the virtual environment, direnv activation,
# script permissions, and cleanup results.
#
# Usage:
#   chmod +x scripts/verify_rpi.sh
#   ./scripts/verify_rpi.sh
#
# Source:
#   https://www.raspberrypi.com/documentation/computers/os.html
#
# AI Acknowledgment:
#   This script was developed and refined with the assistance of AI tools
#   to maintain parity with the setup and update scripts, including
#   standardized terminal output, defensive checks, and student-friendly
#   troubleshooting guidance.

set -u

# This script should be run as the normal user, not sudo.
# It verifies user-level course files and environment settings in the current
# user's home directory.
if [ "${EUID}" -eq 0 ]; then
    echo "❌ ERROR: Do not run this script with sudo."
    echo
    echo "Use:"
    echo "  ./verify_rpi.sh"
    echo
    echo "The script checks the normal user's course environment."
    exit 1
fi

# Script settings.
# These values match the setup and update scripts for disk-space checks.
RPI_USER="${USER}"
RPI_HOSTNAME="$(hostname)"
MIN_FREE_KB=1048576
FREE_SPACE_PERCENT=10

CS350_DIR="${HOME}/cs350"
RPILIB_DIR="${HOME}/rpilib"
SCRIPTS_DIR="${HOME}/scripts"
VENV_DIR="${CS350_DIR}/.venv"
REQUIREMENTS_FILE="${CS350_DIR}/requirements.txt"
BASHRC_FILE="${HOME}/.bashrc"
TMP_REPO_DIR="/tmp/cs350-rpi"

CHECKS_TOTAL=0
CHECKS_PASSED=0
WARNINGS=0
FAILURES=0

record_pass() {
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
    echo "✔ $1"
}

record_warning() {
    WARNINGS=$((WARNINGS + 1))
    echo "⚠️  WARNING: $1"
}

record_fail() {
    FAILURES=$((FAILURES + 1))
    echo "❌ ERROR: $1"
}

begin_check() {
    CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
}

check_directory() {
    local path="$1"
    local description="$2"

    begin_check
    if [ -d "${path}" ]; then
        record_pass "${description} found: ${path}"
    else
        record_fail "${description} not found: ${path}"
    fi
}

check_file() {
    local path="$1"
    local description="$2"

    begin_check
    if [ -f "${path}" ]; then
        record_pass "${description} found: ${path}"
    else
        record_fail "${description} not found: ${path}"
    fi
}

check_absent_path() {
    local path="$1"
    local description="$2"

    begin_check
    if [ ! -e "${path}" ]; then
        record_pass "${description} is clean: ${path}"
    else
        record_warning "${description} still exists: ${path}"
    fi
}

check_executable_file() {
    local path="$1"
    local description="$2"

    begin_check
    if [ -x "${path}" ]; then
        record_pass "${description} is executable: ${path}"
    elif [ -f "${path}" ]; then
        record_fail "${description} exists but is not executable: ${path}"
    else
        record_fail "${description} not found: ${path}"
    fi
}

check_command() {
    local command_name="$1"
    local package_name="$2"

    begin_check
    if command -v "${command_name}" >/dev/null 2>&1; then
        record_pass "${package_name} command available: ${command_name}"
    else
        record_fail "${package_name} command is missing: ${command_name}"
    fi
}

check_apt_package() {
    local package_name="$1"

    begin_check
    if dpkg-query -W -f='${Status}' "${package_name}" 2>/dev/null | grep -q "install ok installed"; then
        record_pass "APT package installed: ${package_name}"
    else
        record_fail "APT package missing: ${package_name}"
    fi
}

check_bashrc_text() {
    local search_text="$1"
    local description="$2"

    begin_check
    if [ -f "${BASHRC_FILE}" ] && grep -Fq "${search_text}" "${BASHRC_FILE}"; then
        record_pass "${description} found in ~/.bashrc"
    else
        record_fail "${description} not found in ~/.bashrc"
    fi
}

check_pip_package() {
    local package_name="$1"

    begin_check
    if "${VENV_DIR}/bin/python" -m pip show "${package_name}" >/dev/null 2>&1; then
        record_pass "Python package installed in .venv: ${package_name}"
    else
        record_fail "Python package missing from .venv: ${package_name}"
    fi
}

print_version() {
    local label="$1"
    shift

    if "$@" >/dev/null 2>&1; then
        printf "%-18s %s\n" "${label}:" "$("$@" 2>/dev/null | head -n 1)"
    fi
}

echo "========================================"
echo " Raspberry Pi Setup Verification"
echo "========================================"
echo
echo "This script will:"
echo "  1. Verify course files and temporary cleanup"
echo "  2. Verify the package list state"
echo "  3. Check available disk space"
echo "  4. Verify command-line tools"
echo "  5. Verify system Python packages"
echo "  6. Verify the Python virtual environment"
echo "  7. Verify automatic virtual environment activation"
echo "  8. Verify script permissions and show a summary"
echo

echo "Current user: ${RPI_USER}"
echo "Hostname:     ${RPI_HOSTNAME}"
echo

printf "Do you wish to continue with verification? (y/N): "
read -r continue_verify
echo

if [[ "${continue_verify,,}" != "y" ]]; then
    echo "✔ Verification cancelled by user."
    exit 0
fi

# Step 1: Verify course files and temporary cleanup.
echo "Step 1 of 8: Verifying course files and temporary cleanup..."
check_directory "${CS350_DIR}" "Course materials directory"
check_directory "${RPILIB_DIR}" "Shared course library directory"
check_directory "${SCRIPTS_DIR}" "Scripts directory"

for module_dir in m1 m2 m3 m4 m5 m6 m7; do
    check_directory "${CS350_DIR}/${module_dir}" "Course module directory ${module_dir}"
done

check_file "${REQUIREMENTS_FILE}" "Course requirements file"
check_file "${RPILIB_DIR}/__init__.py" "rpilib package initializer"
check_file "${RPILIB_DIR}/config.py" "rpilib shared configuration module"
check_file "${RPILIB_DIR}/timing.py" "rpilib shared timing module"

for library_dir in comms displays gpio sensors testing; do
    check_directory "${RPILIB_DIR}/${library_dir}" "rpilib package directory ${library_dir}"
done

check_absent_path "${HOME}/assets" "Temporary home assets directory"
check_absent_path "${HOME}/README.md" "Temporary home README file"
check_absent_path "${HOME}/.gitignore" "Temporary home .gitignore file"
check_absent_path "${TMP_REPO_DIR}" "Temporary repository clone"
echo "✔ Done verifying course files and temporary cleanup."
echo

# Step 2: Verify package list state.
echo "Step 2 of 8: Verifying package list state..."
begin_check
if find /var/lib/apt/lists -type f 2>/dev/null | grep -q .; then
    record_pass "APT package lists are present."
else
    record_fail "APT package lists are missing. Run: sudo apt-get update"
fi
echo "✔ Done verifying package list state."
echo

# Step 3: Check available disk space.
echo "Step 3 of 8: Checking available disk space..."

total_kb=$(df --output=size / | tail -n 1 | awk '{print $1}')
available_kb=$(df --output=avail / | tail -n 1 | awk '{print $1}')

total_mb=$((total_kb / 1024))
available_mb=$((available_kb / 1024))
free_percent=$((available_kb * 100 / total_kb))
percent_recommended_kb=$((total_kb * FREE_SPACE_PERCENT / 100))

# Use the larger recommendation: 1 GB free or 10% free space.
if [ "${percent_recommended_kb}" -gt "${MIN_FREE_KB}" ]; then
    recommended_kb="${percent_recommended_kb}"
else
    recommended_kb="${MIN_FREE_KB}"
fi

recommended_mb=$((recommended_kb / 1024))

printf "%-22s %d MB\n" "Total space on /:"     "${total_mb}"
printf "%-22s %d MB\n" "Available space on /:" "${available_mb}"
printf "%-22s %d%%\n"  "Free space:"           "${free_percent}"
printf "%-22s %d MB\n" "Recommended minimum:"  "${recommended_mb}"
echo

begin_check
if [ "${available_kb}" -ge "${recommended_kb}" ]; then
    record_pass "Disk space meets the recommended minimum."
else
    record_warning "Disk space is below the recommended minimum."
fi

echo "✔ Disk space check complete."
echo

# Step 4: Verify command-line tools.
echo "Step 4 of 8: Verifying command-line tools..."
check_apt_package "direnv"
check_apt_package "gh"
check_apt_package "git"
check_apt_package "shellcheck"
check_apt_package "tree"

check_command "direnv" "direnv"
check_command "gh" "GitHub CLI"
check_command "git" "Git"
check_command "shellcheck" "ShellCheck"
check_command "tree" "tree"
echo "✔ Done verifying command-line tools."
echo

# Step 5: Verify system Python packages.
echo "Step 5 of 8: Verifying system Python packages..."
check_apt_package "python3-full"
check_apt_package "python3-venv"
check_apt_package "python3-pip"
check_apt_package "python3-rpi.gpio"
check_apt_package "python3-serial"
check_apt_package "python3-smbus"

check_command "python3" "Python 3"

begin_check
if python3 -m pip --version >/dev/null 2>&1; then
    record_pass "System pip is available through python3 -m pip."
else
    record_fail "System pip is not available through python3 -m pip."
fi
echo "✔ Done verifying system Python packages."
echo

# Step 6: Verify the Python virtual environment.
echo "Step 6 of 8: Verifying Python virtual environment..."
check_directory "${VENV_DIR}" "Course virtual environment"
check_executable_file "${VENV_DIR}/bin/python" "Virtual environment Python interpreter"
check_executable_file "${VENV_DIR}/bin/pip" "Virtual environment pip command"

begin_check
if [ -x "${VENV_DIR}/bin/python" ] && [ "$("${VENV_DIR}/bin/python" -c 'import sys; print(sys.prefix)' 2>/dev/null)" = "${VENV_DIR}" ]; then
    record_pass "Virtual environment Python prefix matches ${VENV_DIR}."
else
    record_fail "Virtual environment Python prefix does not match ${VENV_DIR}."
fi

begin_check
if [ -f "${REQUIREMENTS_FILE}" ] && [ -x "${VENV_DIR}/bin/python" ]; then
    if "${VENV_DIR}/bin/python" -m pip check >/dev/null 2>&1; then
        record_pass "Installed Python packages passed pip dependency checks."
    else
        record_fail "pip dependency check failed. Run: ${VENV_DIR}/bin/python -m pip check"
    fi
else
    record_fail "Cannot run pip dependency checks because requirements.txt or .venv Python is missing."
fi

if [ -f "${REQUIREMENTS_FILE}" ] && [ -x "${VENV_DIR}/bin/python" ]; then
    while IFS= read -r requirement_line || [ -n "${requirement_line}" ]; do
        clean_requirement="${requirement_line%%#*}"
        package_name="$(printf "%s" "${clean_requirement}" | sed -E 's/[[:space:]]+//g; s/\[.*\]//; s/[<>=!~].*$//')"

        if [ -z "${package_name}" ] || [[ "${package_name}" == -* ]]; then
            continue
        fi

        check_pip_package "${package_name}"
    done < "${REQUIREMENTS_FILE}"
fi

echo "✔ Done verifying Python virtual environment."
echo

# Step 7: Verify automatic virtual environment activation.
echo "Step 7 of 8: Verifying automatic virtual environment activation..."
check_file "${CS350_DIR}/.envrc" "direnv project configuration"

begin_check
if [ -f "${CS350_DIR}/.envrc" ] && grep -Fq 'source "$HOME/cs350/.venv/bin/activate"' "${CS350_DIR}/.envrc"; then
    record_pass "~/${CS350_DIR#${HOME}/}/.envrc points to the course virtual environment."
else
    record_fail "~/${CS350_DIR#${HOME}/}/.envrc does not point to the course virtual environment."
fi

check_bashrc_text 'eval "$(direnv hook bash)"' "direnv Bash hook"
check_bashrc_text '# >>> CS 350 virtual environment prompt >>>' "CS 350 prompt block start marker"
check_bashrc_text '__cs350_venv_prompt' "CS 350 prompt helper function"
check_bashrc_text 'PS1="${PS1#(.venv) }"' "CS 350 prompt cleanup command"
check_bashrc_text '# <<< CS 350 virtual environment prompt <<<' "CS 350 prompt block end marker"

begin_check
if command -v direnv >/dev/null 2>&1 && [ -f "${CS350_DIR}/.envrc" ]; then
    if (cd "${CS350_DIR}" && direnv export bash 2>/tmp/cs350_direnv_error.$$ | grep -q 'VIRTUAL_ENV'); then
        record_pass "direnv can export the course virtual environment."
        rm -f "/tmp/cs350_direnv_error.$$"
    else
        record_fail "direnv cannot export the course virtual environment. Run: cd ~/cs350 && direnv allow"
        rm -f "/tmp/cs350_direnv_error.$$"
    fi
else
    record_fail "Cannot verify direnv export because direnv or .envrc is missing."
fi

echo "✔ Done verifying automatic virtual environment activation."
echo

# Step 8: Verify script permissions and show summary.
echo "Step 8 of 8: Verifying script permissions and cleanup state..."
check_executable_file "${SCRIPTS_DIR}/setup_rpi.sh" "Setup script"
check_executable_file "${SCRIPTS_DIR}/update_rpi.sh" "Update script"
check_executable_file "${SCRIPTS_DIR}/smoke_rpi.sh" "Smoke-test script"

if [ -f "${SCRIPTS_DIR}/verify_rpi.sh" ]; then
    check_executable_file "${SCRIPTS_DIR}/verify_rpi.sh" "Verification script"
fi

begin_check
if find /var/cache/apt/archives -maxdepth 1 -type f -name '*.deb' 2>/dev/null | grep -q .; then
    record_warning "Downloaded APT package files are still present in /var/cache/apt/archives."
else
    record_pass "Downloaded APT package cache is clean."
fi

echo "✔ Done verifying script permissions and cleanup state."
echo

echo "========================================"
echo " Verification Summary"
echo "========================================"
printf "%-18s %d\n" "Checks run:" "${CHECKS_TOTAL}"
printf "%-18s %d\n" "Passed:"     "${CHECKS_PASSED}"
printf "%-18s %d\n" "Warnings:"   "${WARNINGS}"
printf "%-18s %d\n" "Errors:"     "${FAILURES}"
echo

echo "Tool versions detected:"
print_version "python3" python3 --version
print_version "venv python" "${VENV_DIR}/bin/python" --version
print_version "git" git --version
print_version "gh" gh --version
print_version "direnv" direnv version
print_version "tree" tree --version
print_version "shellcheck" shellcheck --version
echo

if [ "${FAILURES}" -eq 0 ]; then
    echo "✔ Verification complete. No required setup problems were found."

    if [ "${WARNINGS}" -gt 0 ]; then
        echo "⚠️  Review the warnings above. They may not block course work, but they are worth checking."
    fi

    exit 0
else
    echo "❌ Verification found one or more required setup problems."
    echo
    echo "Suggested next steps:"
    echo "  1. Re-run the setup script to repair missing tools or files."
    echo "  2. If direnv failed, run: cd ~/cs350 && direnv allow"
    echo "  3. If Python packages failed, run: ~/cs350/.venv/bin/python -m pip install -r ~/cs350/requirements.txt"
    echo
    exit 1
fi
