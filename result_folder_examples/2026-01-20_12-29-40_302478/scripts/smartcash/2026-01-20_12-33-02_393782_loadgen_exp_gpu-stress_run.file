#!/bin/bash
set -euo pipefail

# =========================
# GPU Stress Test (Option A)
# Duty-cycle gpu_burn ON/OFF to emulate load levels (25/50/75/100%)
# =========================

test_name="gpu-burn-dutycycle"
sleep_duration_before_test=2

# Loop variable gpu_load_percent - {25,50,75,100}
gpu_load_percent="$(pos_get_variable gpu_load_percent --from-loop)"

# Global variables (must be provided by POS globals)
# window: total measurement window per load level (seconds)
# burn_mem: e.g. "90%" or "4096" (MB). Defaults to "90%" if not set.
# burn_extra_args: optional flags like "-tc" or "-d"
window="$(pos_get_variable window --from-global)"

# Validate load percent
case "$gpu_load_percent" in
  25|50|75|100) ;;
  *)
    echo "ERROR: gpu_load_percent must be one of 25, 50, 75, 100 (got: $gpu_load_percent)"
    exit 1
    ;;
esac

# Compute ON/OFF durations (integer seconds)
burn_on=$(( window * gpu_load_percent / 100 ))
burn_off=$(( window - burn_on ))

# Basic sanity checks
if [[ "$window" -le 0 ]]; then
  echo "ERROR: window must be > 0 (got: $window)"
  exit 1
fi

cd gpu-burn

# Ensure gpu_burn is available
if ! command -v ./gpu_burn >/dev/null 2>&1 && ! command -v gpu_burn >/dev/null 2>&1; then
  echo "ERROR: gpu_burn binary not found. Put ./gpu_burn next to this script or ensure gpu_burn is in PATH."
  exit 1
fi

# Choose gpu_burn command path
GPU_BURN_BIN="./gpu_burn"
if ! [[ -x "$GPU_BURN_BIN" ]]; then
  GPU_BURN_BIN="gpu_burn"
fi

# Optional: ensure NVIDIA tooling exists (helps fail early on non-GPU nodes)
if ! command -v nvidia-smi >/dev/null 2>&1; then
  echo "ERROR: nvidia-smi not found. This node likely has no NVIDIA GPU / driver."
  exit 1
fi

echo "Starting test '$test_name' for load=${gpu_load_percent}% (window=${window})"

sleep "$sleep_duration_before_test"

# Start energy measurement for this loop iteration (produces measurement_runXX.csv)
pos_energy_start --loop --filename "measurement"

# ON phase: run gpu_burn for burn_on seconds (if > 0)
if [[ "$burn_on" -gt 0 ]]; then
  echo "GPU ON phase: gpu_burn for ${burn_on}s"
  # run as loop-tagged process so POS can track it
  pos_run --loop "loadgen-$test_name" -- "$GPU_BURN_BIN" "$burn_on"
else
  echo "GPU ON phase skipped (0s)"
fi

# If we started gpu_burn, it should end by itself after burn_on seconds.
# Still, if POS returns immediately, we ensure we cover the timing window.
sleep "$burn_on"

# OFF phase: idle for burn_off seconds (if > 0)
if [[ "$burn_off" -gt 0 ]]; then
  echo "GPU OFF phase: idle for ${burn_off}s"
  sleep "$burn_off"
fi

# Stop energy measurement
pos_energy_stop

echo "Completed test '$test_name' for load=${gpu_load_percent}%"
