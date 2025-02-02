# ASCII Art Animation

This repository contains a Python script that creates an animated ASCII art representation of an image. The script loads an image and outputs an ASCII art animation to the terminal. It also includes instructions for automatically running the script when you log in via SSH.

![ASCII Art Demo](demo.png)

> **Note:** Replace `demo.png` with your own screenshot image of the ASCII art output. Add the image to your repository or update the URL accordingly.

## Features

- Converts images into ASCII art using brightness mapping.
- Animates the ASCII art in the terminal.
- Uses a non-blocking key-detection thread to gracefully exit when any key is pressed.
- Can be automatically launched on SSH login by updating your shell startup scripts.

## Prerequisites

- Python 3.x
- [Pillow](https://pypi.org/project/Pillow/) (Install via `pip install pillow`)

## Usage

1. **Clone the repository:**

```bash
git clone https://github.com/juliuserbach/ssh_login.git
cd ssh_login
```

2. **Make Executable**

```
chmod +x login_image.py
```

3. **Run Scipt**
```
./script.py ./images/image2.png
```

## Automatic Launch on SSH Login

If you want the script to run automatically whenever you log in via SSH, follow these steps:

1. Edit Your Shell Startup File

For Bash, you can add the following snippet to your ~/.bash_profile or ~/.profile. (If your system only sources ~/.bashrc for interactive shells, make sure ~/.bash_profile sources ~/.bashrc.)

Open your ~/.bash_profile in your favorite text editor:
```
nano ~/.bash_profile
```
Then add the following lines at the top:
```
# Run ASCII Art Animation on SSH login
if [ -n "$SSH_CONNECTION" ]; then
    /full/path/to/ascii-art-animation/script.py /full/path/to/your/image.jpg
    exit 0
fi
```


