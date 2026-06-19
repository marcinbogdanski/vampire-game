"""Generate an image-gen prompt for a random medieval village character.

Peasant-tier portraits only: muted earth palette, plain wool/linen, no jewelry.
Each field rolls independently from a small closed set of popular values.

Run: python -m vassetgen.character
"""

import random

# A few popular values per field. Closed sets, all RNG-safe.
FIELDS = {
    "sex": ["woman", "man"],
    "attractiveness": ["attractive", "average", "unattractive"],
    "age": ["young", "adult", "middle_aged", "old"],
    "build": ["slight", "average", "sturdy", "heavyset"],
    "skin_tone": ["fair", "olive", "tan", "brown", "weathered"],
    "face_shape": ["round", "oval", "square", "long", "heart"],
    "hair_color": ["black", "chestnut", "dark_brown", "ash_blonde", "copper_red", "grey"],
    "hairstyle": ["loose", "braided", "tied_back", "bun", "under_covering"],
    "eyebrows": ["thick", "thin"],
    "eye_color": ["brown", "hazel", "green", "blue", "grey"],
    # Muted, undyed peasant palette only — bright dyes read as "wrong" for a peasant.
    "garment_color": ["undyed_cream", "dirty_brown", "russet", "ochre", "faded_green", "dusty_blue", "charcoal"],
    "head_covering": ["none", "linen_coif", "kerchief", "simple_hood", "straw_hat"],
}


def roll_character() -> dict[str, str]:
    """Roll one random character: a dict of field -> value."""
    char = {field: random.choice(values) for field, values in FIELDS.items()}
    if char["hairstyle"] == "under_covering" and char["head_covering"] == "none":
        # A hidden hairstyle needs something to hide under.
        char["head_covering"] = random.choice(["linen_coif", "kerchief", "simple_hood"])
    return char


def build_prompt(char: dict[str, str]) -> str:
    """Turn a rolled character into a short image-gen prompt."""
    return (
        f"Generate an image of a medieval village {char['sex']}. "
        f"Waist-up portrait, neutral background. Plain wool/linen clothing. "
        f"Ensure these characteristics:\n"
        f"- attractiveness: {char['attractiveness']}\n"
        f"- age: {char['age']}\n"
        f"- build: {char['build']}\n"
        f"- skin: {char['skin_tone']}\n"
        f"- face shape: {char['face_shape']}\n"
        f"- hair: {char['hair_color']}, {char['hairstyle']}\n"
        f"- eyebrows: {char['eyebrows']}\n"
        f"- eyes: {char['eye_color']}\n"
        f"- clothing: {char['garment_color']}\n"
        f"- head covering: {char['head_covering']}\n"
        f"Neutral expression. Muted, realistic peasant palette."
    )


def main() -> None:
    char = roll_character()
    print(build_prompt(char))


if __name__ == "__main__":
    main()
