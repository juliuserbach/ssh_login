#!/usr/bin/env python3
import sys
import argparse
import random
import time
from PIL import Image
import threading
import termios
import tty
import select

running = True


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="ASCII art animation")
    parser.add_argument("image_path", help="Path to the image file")
    args = parser.parse_args()

    # Define brightness groups with corresponding ASCII characters
    characters = ".-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@■"
    characters = characters[::2]
    num_bins = 6
    bin_size = len(characters) // num_bins

    # Create bins by slicing the character list
    brightness_groups = [
        characters[i * bin_size : (i + 1) * bin_size] for i in range(num_bins)
    ]
    brightness_groups.insert(
        0, [" "] * bin_size
    )  # Add an empty group for 0% brightness
    num_bins = len(brightness_groups)
    # brightness_groups = {
    #     0: [" ", " "],  # 0% brightness (empty space)
    #     1: [".", ",", " "],
    #     2: ["-", "_", "'"],
    #     3: ["o", "O", "*", ":"],
    #     4: ["#", "@", "%", "&"],
    #     5: ["■", "#"],  # 100% brightness (solid block)
    # }
    # select line to use for the message box
    message_line = 25
    message_width = 20
    message = "  Welcome to Work  "
    message_width = len(message)

    # Load and process the image
    try:
        img = Image.open(args.image_path).convert("L")  # Convert to grayscale
        width, height = img.size

        # Resize to fit terminal (you can adjust these values)
        scale_factor_h = 0.075
        scale_factor_w = 0.15
        new_width = int(100)
        new_height = int(50)
        img = img.resize((new_width, new_height))

        # Convert image to brightness levels
        pixels = list(img.getdata())
    except Exception as e:
        print(f"Error loading image: {e}")
        sys.exit(1)

    def check_key():
        """Non-blocking check for key presses using termios and select."""
        global running
        fd = sys.stdin.fileno()
        # Save the current terminal settings
        old_settings = termios.tcgetattr(fd)
        try:
            # Set the terminal to cbreak mode (non-canonical, no echo)
            tty.setcbreak(fd)
            while running:
                # Use select to check if input is available
                dr, dw, de = select.select([sys.stdin], [], [], 0.1)
                if dr:
                    ch = sys.stdin.read(1)  # read one character
                    if ch:
                        running = False
                        break
        finally:
            # Restore original terminal settings
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    # Create and start the thread for checking key presses
    key_thread = threading.Thread(target=check_key)
    key_thread.daemon = True  # This makes the thread exit when the main program exits
    key_thread.start()

    while running:
        output_lines = []
        k = 0  # index to count message lines
        # Process each pixel and map to ASCII characters
        for y in range(new_height):
            line = []
            for x in range(new_width):
                if (
                    y in (message_line - 1, message_line, message_line + 1)
                    and x >= new_width // 2 - message_width // 2
                    and x < new_width // 2 + message_width // 2
                ):
                    if k != 1:
                        line.append(" ")
                    else:
                        line.append(message[x - (new_width // 2 - message_width // 2)])
                    continue
                brightness = pixels[y * new_width + x]
                # Map brightness (0-255) to predefined groups
                bin_index = int(brightness // (256 / num_bins))
                group = brightness_groups[bin_index]

                # Randomly select a character from the group
                line.append(random.choice(group))
            if y in (message_line - 1, message_line, message_line + 1):
                k += 1
            output_lines.append("".join(line))

        # Print the ASCII art with some animation effects
        sys.stdout.write("\n" * new_height)  # Clear previous frame
        sys.stdout.write("\x1b[32m")  # Set text color to green
        sys.stdout.write("\n".join(output_lines))
        sys.stdout.write("\x1b[0m\n")  # Reset text color

        # Control animation speed (adjust this value as needed)
        time.sleep(0.1)


if __name__ == "__main__":
    main()
