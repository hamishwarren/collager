import os
from pathlib import Path
from PIL import Image
import math


def get_image_files(input_paths):
    image_files = []
    for input_path in input_paths:
        if os.path.isdir(input_path):
            # If the input is a directory, get all files and filter only PNG files
            for file in os.listdir(input_path):
                if file.lower().endswith((".png", ".jpg", ".jpeg")):
                    image_files.append(os.path.join(input_path, file))
        elif input_path.lower().endswith((".png", ".jpg", ".jpeg")):
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
    page_width, page_height = 2560, 1564

    # Calculate a scaling factor based on the page size and combined image sizes
    total_area = sum(image.width * image.height for image_file in image_files for image in [Image.open(image_file)])
    page_area = page_width * page_height

    scaling_factor = math.sqrt(page_area / total_area) * 0.9
    print(scaling_factor)

    # Create a new blank image for the PDF
    pdf_image = Image.new("RGB", (page_width, page_height), "white")

    current_x, current_y = 0, 0
    max_height_in_row = 0
    for image_file in image_files:
        image = Image.open(image_file)

        # Resize the image based on the scaling factor
        width = int(image.width * scaling_factor)
        height = int(image.height * scaling_factor)
        image = image.resize((width, height))

        # If the image doesn't fit in the current row, move to the next row
        if current_x + width > page_width:
            current_x = 0
            current_y += max_height_in_row
            max_height_in_row = height

        # If the image doesn't fit on the page, stop adding images
        if current_y + height > page_height:
            break

        # Paste the image onto the PDF image
        pdf_image.paste(image, (current_x, current_y))

        # Update the current x position and the maximum height in the current row
        current_x += width
        max_height_in_row = max(max_height_in_row, height)

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
