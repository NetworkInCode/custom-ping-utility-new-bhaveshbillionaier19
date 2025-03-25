#!/bin/bash

# This script is a placeholder for testing the functionality of the custom ping utility.
# Tests will be added later.
#!/bin/bash

# Root check
if [ "$(id -u)" -ne 0 ]; then
    echo "Error: This script must be run as root (use sudo)"
    exit 1
fi

echo "Root check passed."

# Test counters
total_tests=0
passed_tests=0
failed_tests=0

# Function to run a test
run_test() {
    local test_name="$1"
    local command="$2"
    local expected_status="${3:-0}"

    echo -e "\nRunning test: ${test_name}..."
    echo "Command: ${command}"
    ((total_tests++))

    # Execute the command and capture the output
    if output=$($command 2>&1); then
        actual_status=$?
    else
        actual_status=$?
    fi

    echo "Output:"
    echo "${output}"
    echo "Exit status: ${actual_status}"

    # Check the exit status
    if [ "$actual_status" -eq "$expected_status" ]; then
        echo "PASSED"
        ((passed_tests++))
    else
        echo "FAILED (Expected: $expected_status, Got: $actual_status)"
        ((failed_tests++))
    fi
}

# Print Python environment info (debugging purpose)
# echo "Python Path: $(which python3)"
# echo "Python Version: $(python3 --version)"

# Test cases
run_test "Basic IPv4 ping" "python3 -u src/main.py 8.8.8.8 -c 2"
run_test "IPv6 ping" "python3 -u src/main.py 2001:4860:4860::8888 -6 -c 2"
run_test "Custom TTL" "python3 -u src/main.py 8.8.8.8 -t 128 -c 2"
run_test "Interface specification" "python3 -u src/main.py 127.0.0.1 -I lo -c 2"
run_test "Invalid IP address" "python3 -u src/main.py invalid.ip.address" 1
run_test "Help message" "python3 -u src/main.py -h"

# Summary
echo -e "\nTest Results:"
echo "Total: ${total_tests}"
echo "Passed: ${passed_tests}"
echo "Failed: ${failed_tests}"

# Exit with failure status if any tests failed
exit $((failed_tests > 0 ? 1 : 0))