#!/bin/bash
# test_single_effect.sh - Test a single effect with proper error handling

if [ $# -eq 0 ]; then
    echo "Usage: $0 <effect_name> [duration]"
    echo "Available effects: matrix, rain, decrypt, beams, fireworks, waves, pour, swarm, rings, bubbles, spray, slide, scattered"
    echo "Duration: Optional, defaults to 30 seconds (same as screensaver)"
    exit 1
fi

EFFECT="$1"
DURATION="${2:-30}"  # Default to 30 seconds (same as main screensaver)

echo "Testing effect: $EFFECT for $DURATION seconds"
echo "Press Ctrl+C to interrupt"
echo ""

# Run the effect with timeout and capture output
start_time=$(date +%s)

# Use a subshell to handle the timeout properly
(
    timeout "$DURATION" tte \
        --canvas-width 0 \
        --canvas-height 0 \
        --anchor-canvas c \
        --anchor-text c \
        --no-eol \
        --no-restore-cursor \
        "$EFFECT" < config/ascii_art/ascii-text-art.txt 2>/dev/null
)

exit_code=$?
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo ""
echo "Result for $EFFECT:"

case $exit_code in
    0)
        echo "  ✓ SUCCESS: Completed naturally in $elapsed seconds"
        ;;
    124)
        echo "  ⚠ TIMEOUT: Ran for full $elapsed seconds (effect may be infinite)"
        ;;
    130)
        echo "  ⏏️  INTERRUPTED: User pressed Ctrl+C after $elapsed seconds"
        ;;
    *)
        echo "  ✗ ERROR: Failed after $elapsed seconds (exit code: $exit_code)"
        ;;
esac

echo ""
echo "Analysis:"
if [ $exit_code -eq 124 ]; then
    echo "  This effect appears to run indefinitely and was stopped by timeout"
    echo "  Consider shortening duration or removing from screensaver rotation"
elif [ $exit_code -eq 0 ] && [ $elapsed -lt $DURATION ]; then
    echo "  This effect completed its animation cycle in $elapsed seconds"
    echo "  The effect has a natural ending point"
else
    echo "  Effect behavior: $([ $exit_code -eq 0 ] && echo "Completed naturally" || echo "Unusual termination")"
fi

echo ""
echo "Exit codes:"
echo "  0 = Normal completion (effect finished naturally)"
echo "  124 = Timeout reached (effect ran for full duration)"
echo "  130 = Interrupted by user (Ctrl+C)"
echo "  Other = Error occurred"