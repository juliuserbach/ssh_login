#!/usr/bin/env python3
import os
import sys
import random
import argparse
from PIL import Image

# ASCII characters arranged from darkest to lightest.
ASCII_CHARS = "@%#*+=-:. "


def resize_image(image, new_width):
    """
    Resizes the image while maintaining the aspect ratio.
    The factor (0.55) compensates for the typical console character's height vs. width.
    """
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)
    return image.resize((new_width, new_height))


def grayify(image):
    """Converts the image to grayscale."""
    return image.convert("L")


def pixels_to_ascii(image):
    """
    Maps each pixel to an ASCII char based on its intensity.
    Darker pixels use characters from the beginning of ASCII_CHARS.
    """
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        index = pixel * (len(ASCII_CHARS) - 1) // 255
        ascii_str += ASCII_CHARS[index]
    return ascii_str


def image_to_ascii(image, width):
    """Converts an image to its ASCII art representation."""
    image = resize_image(image, width)
    image = grayify(image)
    ascii_str = pixels_to_ascii(image)
    ascii_art = ""
    for i in range(0, len(ascii_str), image.width):
        ascii_art += ascii_str[i : i + image.width] + "\n"
    return ascii_art


def main():
    parser = argparse.ArgumentParser(
        description="Display a random sci‑fi ASCII art login screen."
    )
    parser.add_argument(
        "--art-dir",
        type=str,
        default="sci_fi_art",
        help="Directory containing your sci‑fi art images (default: sci_fi_art)",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=100,
        help="Width (in characters) for the ASCII art (default: 100)",
    )
    args = parser.parse_args()

    # Mapping of expected image file names to custom welcome messages.
    welcome_mapping = {
        "image1.png": "Welcome, traveler. The digital realm awaits you.",
        "cyber_trench.png": "Greetings, cyber renegade. Dive into the code.",
        "image2.png": "Hello, dreamer. Reality is what you make of it.",
        "neon_night.png": "Welcome, night walker. Let the neon lights guide you.",
        "matrix_code.png": "Hello, Neo. Follow the code.",
        "space_dock.png": "Greetings, explorer. The cosmos beckons.",
        "virtual_landscape.png": "Welcome, architect of dreams. Build your world.",
        "cyber_face.png": "Hello, visionary. See the future through digital eyes.",
        "futuristic_skyline.png": "Greetings, skybound wanderer. Your journey begins here.",
        "rebel_hideout.png": "Welcome, rebel. The resistance awaits your command.",
    }

    # Suggested DALL·E prompts (if you haven't generated images yet).
    prompts = [
        "A futuristic cityscape with neon lights in a rainy cyberpunk style reminiscent of The Matrix.",
        "An abstract digital landscape with glitch effects and holographic elements, cyberpunk art.",
        "A lone figure in a trench coat walking down a rain-soaked street illuminated by neon signs, cyber noir.",
        "A dystopian future control room with holographic interfaces and futuristic architecture.",
        "A digital matrix code falling in a green cascade over a dark futuristic cityscape.",
        "An alien spaceship docking at a space station, with vibrant cosmic colors and futuristic design.",
        "A virtual reality landscape with surreal geometric patterns and neon colors.",
        "A cybernetic humanoid face with glowing circuitry and digital overlays in a high-tech style.",
        "A futuristic skyline with flying cars and towering skyscrapers bathed in neon light.",
        "A cyberpunk rebel hideout with graffiti, neon lights, and a mysterious digital aura.",
    ]

    # Check that the art directory exists.
    if not os.path.isdir(args.art_dir):
        print(f"Art directory '{args.art_dir}' not found.\n")
        print(
            "Please generate sci‑fi images using one of the following DALL·E prompts and place them in the directory:"
        )
        for i, prompt in enumerate(prompts, 1):
            print(f"{i}. {prompt}")
        sys.exit(1)

    # Gather image files from the art directory.
    valid_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
    image_files = [
        f for f in os.listdir(args.art_dir) if f.lower().endswith(valid_extensions)
    ]
    if not image_files:
        print(f"No images found in '{args.art_dir}'.\n")
        print(
            "Please generate sci‑fi images using one of the following DALL·E prompts and place them in the directory:"
        )
        for i, prompt in enumerate(prompts, 1):
            print(f"{i}. {prompt}")
        sys.exit(1)

    # Randomly select one image.
    image_file = random.choice(image_files)
    image_path = os.path.join(args.art_dir, image_file)

    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Failed to open image '{image_file}': {e}")
        sys.exit(1)

    # Convert the image to ASCII art.
    ascii_art = image_to_ascii(image, args.width)
    # Retrieve the welcome message if it exists in the mapping; otherwise, use a default.
    welcome_message = welcome_mapping.get(
        image_file, "Welcome, futuristic wanderer. Enjoy the view of tomorrow."
    )

    # Print the final login screen.
    separator = "=" * args.width
    print(separator)
    print(welcome_message.center(args.width))
    print(separator)
    print(ascii_art)


if __name__ == "__main__":
    main()
