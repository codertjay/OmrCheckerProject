import os
import cv2
from pdf2image import convert_from_path

answer_regions = {
    "regions": {
        "region1": {
            "region": (427, 312, 84, 144),
            "region_questions": range(10),
        },
        "region2": {
            "region": (427, 484, 84, 144),
            "region_questions": range(10),
        },
        "region3": {
            "region": (583, 315, 84, 144),
            "region_questions": range(10),
        },
        "region4": {
            "region": (583, 483, 84, 144),
            "region_questions": range(10),
        }, "region5": {
            "region": (731, 313, 84, 144),
            "region_questions": range(10),
        },
        "region6": {
            "region": (731, 483, 84, 144),
            "region_questions": range(10),
        },
        "region7": {
            "region": (879, 312, 84, 144),
            "region_questions": range(10),
        },
        "region8": {
            "region": (879, 482, 84, 144),
            "region_questions": range(10),
        },
        "region9": {
            "region": (1029, 312, 84, 144),
            "region_questions": range(10),
        },
        "region10": {
            "region": (1031, 482, 84, 144),
            "region_questions": range(10),
        },

    },
    "total_questions": 100
}

answers = {
    1: "a",
    2: "a",
    3: "b",
    4: "b",
    5: "b",
    6: "b",
    7: "b",
    8: "b",
    9: "b",
    10: "b"
}


def extract_images_from_pdf(pdf_path, output_dir):
    """
    This is used to extract pages from a PDF and convert them to images.
    :param pdf_path: Path to the PDF file.
    :param output_dir: Directory to save the extracted images.
    :return: None
    """
    images = convert_from_path(pdf_path, poppler_path="C:\\tools\\poppler-23.05.0\\Library\\bin")

    for i, image in enumerate(images):
        image_path = os.path.join(output_dir, f"page_{i + 1}.jpg")
        image.save(image_path, 'JPEG')


def mark_sheet_base_on_region(image, region, region_range, answer_count):
    """

    This is used to  make mark on the exam sheet an return the image
    :return:
    """
    x, y, width, height = region
    column_width = width // 5
    column_height = height // 10

    region_image = image[y:y + height, x:x + width]  # Extract the region of interest

    boxes = []

    for row_index in region_range:
        # this is used to track the highest box
        highest_box = None
        highest_count = 0

        for col_index in range(5):
            # Get the top left and top right of each column in a row
            box_x = x + col_index * column_width
            box_y = y + row_index * column_height

            box = region_image[row_index * column_height:(row_index + 1) * column_height,
                  col_index * column_width:(col_index + 1) * column_width]
            # Convert the box array into an image
            box_image = cv2.cvtColor(box, cv2.COLOR_BGR2GRAY)
            # Apply a threshold to the box to obtain a binary image
            box_thresh = cv2.threshold(box_image, 200, 255, cv2.THRESH_BINARY_INV)[1]

            # Count the number of non-zero pixels in the threshold box
            count = cv2.countNonZero(box_thresh)
            # Append the box image to the list of box images
            boxes.append(box_thresh)
            # Check if the current box has a higher count than the previous highest
            if count > highest_count:
                highest_count = count
                highest_box = (box_x, box_y, column_width, column_height)

            # Append the threshold box image to the list of box images
            boxes.append(box_thresh)

            # Color the highest box in the row with a different color
        if highest_box is not None:
            box_x, box_y, box_width, box_height = highest_box
            cv2.rectangle(image, (box_x, box_y), (box_x + box_width, box_y + box_height), (0, 0, 255), 2)
        # for every row index we increase the ans counter
        answer_count += 1
    return image, boxes


def mark_exam(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Resize the image to 700 by 700 for processing
    resized_image = cv2.resize(image, (1200, 700))
    user_mark_sheets = []
    answer_count = 0
    for item in answer_regions.get("regions"):
        region = answer_regions["regions"][item]["region"]
        region_range = answer_regions["regions"][item]["region_questions"]
        resized_image, mark_sheet = mark_sheet_base_on_region(resized_image, region, region_range, answer_count)

    cv2.imshow("Original", resized_image)
    cv2.waitKey(0)


pdf_path = "./sheet.pdf"
output_dir = "./output"
extract_images_from_pdf(pdf_path, output_dir)

image_path = os.path.join(output_dir, "page_3.jpg")
mark_exam(image_path)
