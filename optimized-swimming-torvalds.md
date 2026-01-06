# Plan: Optimize Screensaver Effect Durations

## Problem Summary

1. **Matrix feels incomplete** - Stops abruptly at 30s, needs ~35-40s to feel complete
2. **Rings effect should be replaced** - Remove and add thunderstorm (18s natural duration)
3. **Inefficient timing** - All effects use 30s timeout regardless of natural duration (3s-25s range)

## Solution: Per-Effect Duration Optimization

Replace global `EFFECT_DURATION=30` with individual timeouts per effect based on empirical testing data from EFFECT_DEBUG_REPORT.md.

## Implementation Changes

### File: `/home/nick/screensaver/bin/screensaver`

#### Change 1: Rename global duration (Line 11)
```bash
# OLD:
EFFECT_DURATION=30  # seconds per effect

# NEW:
DEFAULT_EFFECT_DURATION=30  # fallback if effect not in EFFECT_DURATIONS
```

#### Change 2: Add duration mapping (After line 12, before EFFECTS array)
```bash
# Individual effect durations (seconds) - optimized based on natural animation cycles
declare -A EFFECT_DURATIONS=(
    # Very short effects - need generous buffer to be visible
    [slide]=10        # Natural: 3s  | Buffer: +7s
    [scattered]=10    # Natural: 4s  | Buffer: +6s

    # Short-to-medium effects
    [spray]=15        # Natural: 8s  | Buffer: +7s
    [pour]=15         # Natural: 9s  | Buffer: +6s
    [waves]=15        # Natural: 10s | Buffer: +5s
    [rain]=15         # Estimated (no test data)

    # Medium-to-long effects
    [beams]=20        # Natural: 15s | Buffer: +5s
    [decrypt]=25      # Natural: 17s | Buffer: +8s
    [bubbles]=25      # Natural: 18s | Buffer: +7s
    [thunderstorm]=25 # Natural: 18s | Buffer: +7s (NEW - replaces rings)

    # Long effects - need extra time to feel complete
    [fireworks]=30    # Natural: 23s | Buffer: +7s
    [matrix]=40       # Natural: 22s | Buffer: +18s (user reports needs more time)
)
```

**Rationale for durations:**
- Short effects (3-4s): 10s final = prevents "blink and miss"
- Medium effects (8-10s): 15s final = comfortable viewing
- Long effects (15-18s): 20-25s final = ensure completion
- Matrix: 40s = addresses user's "feels incomplete" feedback
- All durations = natural cycle + buffer to avoid abrupt cutoffs

#### Change 3: Replace rings with thunderstorm (Line 24)
```bash
# OLD:
    rings

# NEW:
    thunderstorm  # Replaces rings (18s natural duration, tested and working)
```

#### Change 4: Update effect count comment (Line 77)
```bash
# OLD:
    # Shuffle effects for this cycle (see all 13 before any repeat)

# NEW:
    # Shuffle effects for this cycle (see all 12 before any repeat)
```
*Note: Count is 12 (was 13 with swarm, then removed swarm and rings, added thunderstorm = net -1)*

#### Change 5: Dynamic duration lookup - First timeout (Before line 83)
```bash
# Add these 2 lines BEFORE the existing "timeout" line:
            # Get effect-specific duration, or use default fallback
            DURATION="${EFFECT_DURATIONS[$EFFECT]:-$DEFAULT_EFFECT_DURATION}"

# Then change line 83 from:
            timeout "$EFFECT_DURATION" tte \
# To:
            timeout "$DURATION" tte \
```

#### Change 6: Dynamic duration lookup - Second timeout (Before line 94)
```bash
# Add these 2 lines BEFORE the existing "timeout" line:
            # Get effect-specific duration, or use default fallback
            DURATION="${EFFECT_DURATIONS[$EFFECT]:-$DEFAULT_EFFECT_DURATION}"

# Then change line 94 from:
            timeout "$EFFECT_DURATION" tte \
# To:
            timeout "$DURATION" tte \
```

## Final Effect List (12 effects, alphabetical)

1. beams (20s)
2. bubbles (25s)
3. decrypt (25s)
4. fireworks (30s)
5. matrix (40s) ← longest
6. pour (15s)
7. rain (15s)
8. scattered (10s)
9. slide (10s) ← shortest
10. spray (15s)
11. thunderstorm (25s) ← NEW
12. waves (15s)

## Testing Plan

### 1. Syntax validation
```bash
bash -n bin/screensaver  # Check for syntax errors
```

### 2. Test critical effects
```bash
./test_single_effect.sh matrix 40        # Should feel complete now
./test_single_effect.sh thunderstorm 25  # New effect, verify it works
./test_single_effect.sh slide 10         # Short effect, verify not cut off
```

### 3. Integration test
```bash
./bin/screensaver  # Watch for 5+ minutes, verify smooth transitions
```

**Success criteria:**
- Matrix animation feels complete (no abrupt stop)
- Thunderstorm appears and works correctly
- No rings effect appears
- Short effects (slide/scattered) don't feel rushed
- All 12 effects cycle through before repeating

## Expected Improvements

1. **Matrix complete** - 40s duration allows full animation cycle
2. **Better variety** - Thunderstorm adds weather theme (complements rain/waves/pour)
3. **Efficiency** - Short effects finish faster (slide: 10s vs 30s = 20s saved)
4. **Smooth UX** - Each effect gets optimal viewing time, nothing feels rushed or dragging

## Risk Mitigation

- **Fallback safety**: `DEFAULT_EFFECT_DURATION=30` prevents crashes if effect not in map
- **Minimal changes**: Only 6 targeted changes, no architectural modifications
- **Backward compatible**: No breaking changes, preserves all existing functionality
- **Tested approach**: Duration values based on EFFECT_DEBUG_REPORT.md empirical data

## Files to Modify

1. `/home/nick/screensaver/bin/screensaver` - Primary implementation (all changes above)
