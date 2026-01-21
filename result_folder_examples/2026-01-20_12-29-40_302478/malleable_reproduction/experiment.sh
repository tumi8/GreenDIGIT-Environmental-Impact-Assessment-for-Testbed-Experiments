#!/bin/bash

# The hosts are allocated, rebooted, and the experiment scripts are deployed
# The experiment prepares the loadgen and dut nodes for MoonGen experiments

# exit on error
set -e
# log every command


# Specify experiment parameters
loadgen=$1
test_name="gpu-stress"
dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to display usage information
display_usage() {
    echo "Usage: $0 <loadgen> <dut> [--publish]"
    echo "   - loadgen: Name of the load generator node"
}

# Check the number of arguments
if [ "$#" -lt 1 ]; then
    echo "Error: Incorrect number of arguments."
    display_usage
    exit 1
fi

# SETUP
image=debian-trixie-nvidia-cuda-toolkit@2025-09-05T08:34:48+00:00

echo -e "\n### Freeing host ###"
pos allocations free "$loadgen"

echo -e "\n### Allocating host ###"
pos allocations allocate "$loadgen"

echo -e "\n### Setting experiment variables ###"
pos allocations set_variables "$loadgen" --as-global "$dir/variables/global.yml"
pos allocations set_variables "$loadgen" --as-loop "$dir/variables/loop.yml"

echo -e "\n### Setting images to $image ###"
pos nodes image "$loadgen" "$image" --staging

echo -e "\n### Setting boot parameters ###"
pos nodes bootparameter "$loadgen" "iommu=pt"

echo -e "\n### Rebooting experiment hosts: $loadgen ###"
pos nodes reset "$loadgen" --non-blocking

echo -e "\n### Deploying and running setup scripts ###"
command_loadgen_id=$(pos commands launch --infile "$dir/loadgen/setup.sh" "$loadgen" --queued --name loadgen_setup_"$test_name")

echo -e "\n### Waiting for setup to finish ###"
pos commands await "$command_loadgen_id"

# EXPERIMENT
# Start the commands and store their IDs
echo -e "\n### Deploying and running experiment $test_name ###"

# wait
pos commands launch --infile "$dir/loadgen/loadgen.sh" "$loadgen" --queued --blocking --loop --name loadgen_exp_"$test_name"

RESULT_FOLDER=$(pos allocations show $loadgen | jq -r ".result_folder")
ALLOCATION_ID=$(pos allocations show $loadgen | jq -r ".id")

echo -e "\n### Experiment completed successfully ###"
echo "RESULT_FOLDER: $RESULT_FOLDER"
echo "ALLOCATION_ID: $ALLOCATION_ID"
