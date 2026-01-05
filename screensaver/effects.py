"""Effect management for screensaver."""

import random
from typing import List, Type
from terminaltexteffects.effects import (
    effect_matrix,
    effect_rain,
    effect_beams,
    effect_decrypt,
    effect_fireworks,
    effect_waves,
    effect_slide,
    effect_pour,
    effect_swarm,
    effect_rings,
    effect_blackhole,
    effect_bubbles,
    effect_burn,
    effect_colorshift,
    effect_crumble,
    effect_expand,
    effect_middleout,
    effect_orbittingvolley,
    effect_scattered,
    effect_spotlights,
    effect_spray,
    effect_sweep,
    effect_synthgrid,
)


# Map effect names to their classes
EFFECT_MAP = {
    "matrix": effect_matrix.Matrix,
    "rain": effect_rain.Rain,
    "beams": effect_beams.Beams,
    "decrypt": effect_decrypt.Decrypt,
    "fireworks": effect_fireworks.Fireworks,
    "waves": effect_waves.Waves,
    "slide": effect_slide.Slide,
    "pour": effect_pour.Pour,
    "swarm": effect_swarm.Swarm,
    "rings": effect_rings.Rings,
    "blackhole": effect_blackhole.Blackhole,
    "bubbles": effect_bubbles.Bubbles,
    "burn": effect_burn.Burn,
    "colorshift": effect_colorshift.ColorShift,
    "crumble": effect_crumble.Crumble,
    "expand": effect_expand.Expand,
    "middleout": effect_middleout.MiddleOut,
    "orbittingvolley": effect_orbittingvolley.OrbittingVolley,
    "scattered": effect_scattered.Scattered,
    "spotlights": effect_spotlights.Spotlights,
    "spray": effect_spray.Spray,
    "sweep": effect_sweep.Sweep,
    "synthgrid": effect_synthgrid.SynthGrid,
}


# Default effects that work well for screensavers
DEFAULT_EFFECTS = [
    "matrix",
    "rain",
    "decrypt",
    "fireworks",
    "waves",
    "beams",
    "pour",
    "swarm",
    "rings",
]


class EffectManager:
    """Manages effect selection and cycling."""

    def __init__(
        self,
        enabled_effects: List[str] = None,
        excluded_effects: List[str] = None,
        cycle_mode: str = "random"
    ):
        """
        Initialize the effect manager.

        Args:
            enabled_effects: List of effect names to use (None = use defaults)
            excluded_effects: List of effect names to exclude
            cycle_mode: "random" or "sequential"
        """
        self.cycle_mode = cycle_mode

        # Determine which effects to use
        if enabled_effects:
            self.effects = [e for e in enabled_effects if e in EFFECT_MAP]
        else:
            self.effects = DEFAULT_EFFECTS.copy()

        # Remove excluded effects
        if excluded_effects:
            self.effects = [e for e in self.effects if e not in excluded_effects]

        if not self.effects:
            raise ValueError("No effects enabled. At least one effect must be available.")

        self.current_index = 0
        self.recent_effects = []  # Track recently used effects for random mode

    def get_next_effect(self) -> Type:
        """
        Get the next effect class to use.

        Returns:
            Effect class from TerminalTextEffects
        """
        if self.cycle_mode == "sequential":
            effect_name = self.effects[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.effects)
        else:  # random
            # Avoid immediate repetition by excluding recently used effects
            available = [e for e in self.effects if e not in self.recent_effects]

            # If we've used all effects, reset the recent list
            if not available:
                self.recent_effects = []
                available = self.effects

            effect_name = random.choice(available)

            # Track recently used effects (keep last 3)
            self.recent_effects.append(effect_name)
            if len(self.recent_effects) > min(3, len(self.effects) // 2):
                self.recent_effects.pop(0)

        return EFFECT_MAP[effect_name]

    def get_effect_name(self, effect_class: Type) -> str:
        """
        Get the name of an effect from its class.

        Args:
            effect_class: The effect class

        Returns:
            Name of the effect
        """
        for name, cls in EFFECT_MAP.items():
            if cls == effect_class:
                return name
        return "unknown"

    def list_available_effects(self) -> List[str]:
        """
        Get list of all available effect names.

        Returns:
            List of effect names
        """
        return list(EFFECT_MAP.keys())

    def list_enabled_effects(self) -> List[str]:
        """
        Get list of currently enabled effect names.

        Returns:
            List of enabled effect names
        """
        return self.effects.copy()
