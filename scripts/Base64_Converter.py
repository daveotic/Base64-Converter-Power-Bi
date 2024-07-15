"""
Base 64_Converter.py

This script encodes JPEG and PNG images to Base64 format and stores the encodes as formatted data in a JSON file.

"""

import subprocess
import sys

# Test if pip is instaleld before continuing wih script.

try:
    import pip
except ImportError:
    print(
        " Error: 'pip' is not installed please install pipi manually before running script"
    )


def pip_install_packages():
    """
    Install packages listed in def.

    Returns:
    - calls executable to uinstall packages needed.
    """
    packages = ["Pillow"]
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


print("Checking installed packages")

# Test if Pillow is installed and if not prompt users if they want to install it.
while True:
    try:
        import PIL

        print("No packages needed.")
        break
    except ImportError:
        print("The package 'Pillow' is not installed")
        install_dependencies = input(
            "Would you like to install 'Pillow' for image handling? (y/n): "
        )
        if install_dependencies.lower() == "y":
            print("Installing packages...")
            pip_install_packages()
        elif install_dependencies.lower() == "n":
            print("Exiting script packages not installed")
            sys.exit()
        else:
            print("Invalid input. Please enter 'y' or 'n'")

from PIL import Image
import os
import base64
import json


def encode_image_to_base64(image_path):
    """
    Encode an image file to Base64 format.

    Parameters:
    - image_path(str): The path to the image file to be encoded.

    Returns:
    - str: The Base64-encoded string.
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")


def convert_jpeg_to_png(jpeg_path, png_path):
    """
    Converts any JPEG to PNG.

    Parameters:
    - jpeg_path: path to the JPEG file
    - png_path: path to save location of the PNG file

    Returns:
    - str: The Base64-encoded string.
    """
    try:
        image = Image.open(jpeg_path)
        image.save(png_path, "PNG")
        return True
    except Exception as e:
        print(f"Error converting {jpeg_path} to PNG", e)
        return False


# The directory where the script us located used to get an accurate file paath for pictures and JSON
script_directory = os.path.dirname(os.path.abspath(__file__))

# Folder path for all PNG/JPEG needing to be converted.
image_folder_path = os.path.abspath(
    os.path.join(script_directory, "../convert_pictures")
)

# Folder path to the JSON output file.
json_file_path = os.path.abspath(
    os.path.join(script_directory, "../resources/image_base64.json")
)

# Check to see if the JSON file exsists.
check_for_json_file = os.path.exists(json_file_path)

# Checks if image_folder_path contains .png or .jpeg files.
image_in_folder = [
    image
    for image in os.listdir(image_folder_path)
    if image.endswith(".png") or image.endswith(".jpeg") or image.endswith(".jpg")
]
# If the JSON file does not exist it checks the image_folder directory for PNG/JPEG files and exits the script if there is none.
if not check_for_json_file and not image_in_folder:
    print(
        "No JPEG or PNG files found in the 'convert_pictures' folder and no JSON file found. Exiting script"
    )
    exit()
# If the JSON file exists then open the JSON file and read if the data is realitive data.
elif check_for_json_file:
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)
    # There is no data in the json file and there is no images.
    if not data or (isinstance(data, dict) and not data) and not image_in_folder:
        print(
            "No JPEG or PNG file found in the 'convert_pictures' folder and no relative data found in JSON file. Exiting script."
        )
        exit()
    # There is data in the JSON file and there is no images.
    else:
        print(
            "No JPEG or PNG files found in the 'convert_pictures' folder, but data found in JSON file. Continuing script..."
        )

# Create or lod exsisting JSON file.
image_data = {}
if check_for_json_file:
    with open(json_file_path, "r") as json_file:
        image_data = json.load(json_file)

# list all JPEG and PNG file in folder.
jpeg_files = [
    f
    for f in os.listdir(image_folder_path)
    if f.endswith(".jpeg") or f.endswith(".jpg")
]
png_files = [f for f in os.listdir(image_folder_path) if f.endswith(".png")]

# Convert JPEG files to PNG files and removes .JPEG from file to get the PNG name.
for jpeg_file in jpeg_files:
    image_name = os.path.splittext(jpeg_file)[0]
    png_file = f"{image_name}.png"
    jpeg_path = os.path.join(image_folder_path, jpeg_file)
    png_path = os.path.join(image_folder_path, png_file)
    # Prevents overwritting PNG file if it already exists.
    if png_file not in png_files and convert_jpeg_to_png(jpeg_path, png_path):
        print("Converting JPEG to PNG...")
        png_files.append(png_file)
        print("Done!")
        # Prompt the user if they would like to delete the old JPEG files.
        while True:
            user_response_delete_jpeg = input(
                "Would you like to delete the old jpeg/jpg files? (y/n): "
            )
            if user_response_delete_jpeg.lower() == "y":
                os.remove(jpeg_path)
                print("Deleted jpeg/jpg files")
                break
            elif user_response_delete_jpeg.lower() == "n":
                print("Deleted jpeg files")
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

# Processses all png files withn the image_folder_path to Base64 and sets to specific JSON format.
for png_file in png_files:
    image_name = os.path.splitext(png_file)[0]
    image_path = os.path.join(image_folder_path, png_file)
    base64_string = encode_image_to_base64(image_path)
    image_data[image_name] = {"description": png_file, "url": base64_string}

# Delete JSON entries from list if the image was removed from image_folder_path
existing_images = set(image_data.keys())
current_images = set(os.path.splitext(f)[0] for f in png_files)
delete_images = existing_images.difference(current_images)
if delete_images:
    # Prompt the user if they want to delete image data from JSON file.
    while True:
        print("The following images have been deleted from the 'convert_png' fodler:")
        print("\n".join(delete_images))
        user_response = input(
            "Would you like to remove the corresponding Base64 codes from the json file? (y/n): "
        )
        if user_response.lower() == "y":
            for deleted_image in delete_images:
                del image_data[deleted_image]
                print(",".join(delete_images), "was deleted.")
            break
        elif user_response.lower() == "n":
            print("Continuuing without removing Base64 codes.")
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

# Write updated image_data to JSON file.
with open(json_file_path, "w") as json_file:
    json.dump(image_data, json_file, indent=2)

print("Base64 codes saved to", json_file_path)