import os
import random
from pathlib import Path
from PIL import Image


def get_image_files(input_paths):
    image_files = []
    for input_path in input_paths:
        if os.path.isdir(input_path):
            # If the input is a directory, get all files and filter only PNG files
            for file in os.listdir(input_path):
                if file.lower().endswith(".png"):
                    image_files.append(os.path.join(input_path, file))
        elif input_path.lower().endswith(".png"):
            # If the input is a single PNG file, add it to the list
            image_files.append(input_path)
        else:
            raise ValueError(f"Input '{input_path}' is not a valid PNG file or folder.")
    return image_files


def create_collage(input_paths, output_pdf):
    # Get the list of input PNG files
    image_files = get_image_files(input_paths)

    if not image_files:
        print("No PNG files found in the input.")
        return

    # Calculate the dimensions of the page
    page_width, page_height = 2560, 1664

    # Calculate a scaling factor based on the page size and combined image sizes
    total_width, total_height = 0, 0
    for image_file in image_files:
        image = Image.open(image_file)
        total_width += image.width
        total_height += image.height

    scaling_factor = min(page_width / total_width, page_height / total_height)

    # Create a new blank image for the PDF
    pdf_image = Image.new("RGB", (page_width, page_height), "white")

    # Shuffle the list of images
    random.shuffle(image_files)

    current_x, current_y = 0, 0
    for image_file in image_files:
        image = Image.open(image_file)

        # Resize the image based on the scaling factor
        width = int(image.width * scaling_factor)
        height = int(image.height * scaling_factor)
        image = image.resize((width, height), Image.LANCZOS)

        # Paste the image onto the PDF image at the current position
        pdf_image.paste(image, (current_x, current_y))

        # Update the current position for the next image
        current_x += width
        if current_x >= page_width:
            current_x = 0
            current_y += height

    # Save the collage as a PDF file
    pdf_image.save(output_pdf, "PDF", resolution=100.0)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a collage of PNG images and save as PDF")
    parser.add_argument("input", nargs="+", help="Input PNG files and/or folders containing PNG files")
    parser.add_argument("--output", "-o", help="Output PDF file name", default="collage.pdf")
    args = parser.parse_args()

    if args.input:
        # Check if the output file ends with '.pdf'
        if not args.output.endswith(".pdf"):
            args.output += ".pdf"

        create_collage(args.input, args.output)
        print(f"Collage saved as {args.output}")
    else:
        print("No input provided.")
