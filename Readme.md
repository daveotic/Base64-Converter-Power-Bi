# Base64 Image Converter

This python script converts JPEG to PNG and encodes all PNG files to base64. All base64 encodes are formatted and put into a JSON file for each image that a Power BI Theme File can use to import custum icons. Any Image removed from the convert folder can also be removed from the JSON file using the script.

## Usage:

1. Place all JPEG and PNG images in the [convert_pictures](<convert_pictures/>) folder.
2. Run rhw  script [Base64_Convert.py](<scripts/Base64_converter.py>) in the terminal.
3. Follow the prompt to install packages and proceed with the enconding process.

### Installation:
1. Ensure python and pip are installed on machine.
2. Install the required packages using the command below in the terminal.
    - cd into main git repository before running the command below.
    - The python script also checks if packages are installed

~~~ bash
    cd "/Base64_Converter"
    pip install -r requirments.txt
~~~

## File Structure:

~~~ bash
Base64_Converter
├── convert_pictures # Folder for all PNG and JPEG images.
│   └── .gitkeep
│   # Files in this folder are not tracked by git except for .gitkeep
├── resources
│   └── .gitkeep
│   # Files in this folder are not tracked by git except for .gitkeep
├── scripts
│   └── Base64_Converter.py # Main script
├── Readme.md
└── Requirements.txt
~~~