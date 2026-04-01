#!/usr/bin/env python3
"""
Dice roller for podcast host personality generation.
Generates truly random host personalities for article-pack podcast transcripts.
"""

import random
import sys
import json
from typing import Optional

# Personality dimensions - each is a d6 roll
DIMENSIONS = {
    "energy": [
        "Chill & laid-back",
        "Thoughtful",
        "Warm",
        "Enthusiastic",
        "Hyped",
        "Chaotic gremlin"
    ],
    "expertise": [
        "Total newbie",
        "Curious learner",
        "Informed amateur",
        "Knowledgeable",
        "Expert",
        "World authority"
    ],
    "style": [
        "Analytical",
        "Storyteller",
        "Comedian",
        "Philosopher",
        "Skeptic",
        "Devil's advocate"
    ],
    "quirk": [
        "Loves analogies",
        "Goes on tangents",
        '"But why though?"',
        "Pop culture refs",
        "Personal anecdotes",
        "Conspiracy brain"
    ],
    "vibe": [
        "NPR host",
        "Joe Rogan energy",
        "Tech bro",
        "Academic",
        "Your smart friend",
        "Unhinged genius"
    ]
}

# Quick archetype presets (combines multiple dimensions into one roll)
ARCHETYPES = [
    {"name": "Grumpy professor", "traits": "Chill + Expert + Skeptic + 'But why though?' + Academic"},
    {"name": "Caffeinated intern", "traits": "Hyped + Curious learner + Storyteller + Pop culture refs + Your smart friend"},
    {"name": "Tired scientist", "traits": "Chill + World authority + Analytical + Goes on tangents + Academic"},
    {"name": "Overeager journalist", "traits": "Enthusiastic + Informed amateur + Storyteller + Personal anecdotes + NPR host"},
    {"name": "Devil's advocate", "traits": "Thoughtful + Knowledgeable + Devil's advocate + 'But why though?' + Philosopher"},
    {"name": "Tech optimist", "traits": "Hyped + Expert + Storyteller + Pop culture refs + Tech bro"},
    {"name": "Data purist", "traits": "Chill + Expert + Analytical + 'But why though?' + Academic"},
    {"name": "Fresh convert", "traits": "Enthusiastic + Curious learner + Storyteller + Personal anecdotes + Your smart friend"},
    {"name": "Industry veteran", "traits": "Warm + World authority + Philosopher + Personal anecdotes + NPR host"},
    {"name": "Pattern-finder", "traits": "Thoughtful + Knowledgeable + Analytical + Loves analogies + Philosopher"},
    {"name": "Contrarian researcher", "traits": "Chill + Expert + Devil's advocate + Conspiracy brain + Unhinged genius"},
    {"name": "Enthusiastic explainer", "traits": "Warm + Knowledgeable + Storyteller + Loves analogies + Your smart friend"},
]


def roll_d6() -> int:
    """Roll a single d6."""
    return random.randint(1, 6)


def roll_dimension(dimension: str) -> tuple[int, str]:
    """Roll for a specific dimension, returns (roll, result)."""
    if dimension not in DIMENSIONS:
        raise ValueError(f"Unknown dimension: {dimension}")
    roll = roll_d6()
    return roll, DIMENSIONS[dimension][roll - 1]


def roll_full_personality() -> dict:
    """Roll all dimensions for a complete personality."""
    personality = {}
    for dim in DIMENSIONS:
        roll, result = roll_dimension(dim)
        personality[dim] = {"roll": roll, "value": result}
    return personality


def roll_archetype() -> tuple[int, dict]:
    """Roll for a quick archetype (d12)."""
    roll = random.randint(1, len(ARCHETYPES))
    return roll, ARCHETYPES[roll - 1]


def format_personality(personality: dict, name: str = "Host") -> str:
    """Format a personality for display."""
    lines = [f"🎲 {name}:"]
    for dim, data in personality.items():
        lines.append(f"  [{data['roll']}] {dim.capitalize()}: {data['value']}")
    return "\n".join(lines)


def format_archetype(roll: int, archetype: dict, name: str = "Host") -> str:
    """Format an archetype for display."""
    return f"🎲 {name}: [{roll}] {archetype['name']}\n   Traits: {archetype['traits']}"


def main():
    """CLI interface for dice rolling."""
    import argparse

    parser = argparse.ArgumentParser(description="Roll dice for podcast host personalities")
    parser.add_argument("--hosts", type=int, default=2, help="Number of hosts to generate (default: 2)")
    parser.add_argument("--mode", choices=["full", "archetype"], default="archetype",
                       help="full = roll all 5 dimensions, archetype = quick preset (default: archetype)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    results = []
    host_names = ["Host A", "Host B", "Host C", "Host D"][:args.hosts]

    print("=" * 50)
    print("🎲 PODCAST HOST PERSONALITY GENERATOR 🎲")
    print("=" * 50)
    print()

    for i, name in enumerate(host_names):
        if args.mode == "full":
            personality = roll_full_personality()
            if args.json:
                results.append({"name": name, "mode": "full", "personality": personality})
            else:
                print(format_personality(personality, name))
                print()
        else:
            roll, archetype = roll_archetype()
            if args.json:
                results.append({"name": name, "mode": "archetype", "roll": roll, "archetype": archetype})
            else:
                print(format_archetype(roll, archetype, name))
                print()

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("=" * 50)
        print("Use these personalities to shape your podcast dialogue!")
        print("=" * 50)


if __name__ == "__main__":
    main()
