import os
import cv2
from pdf2image import convert_from_path

answer_regions = {
    "regions": {
        "region1": {
            "region": (242, 314, 58, 142),
            "region_questions": range(1, 10),
        },
        "region2": {
            "region": (243, 483, 59, 142),
            "region_questions": range(11, 20),
        },
        "region3": {
            "region": (331, 312, 58, 142),
            "region_questions": range(21, 30),
        },
        "region4": {
            "region": (334, 483, 58, 142),
            "region_questions": range(31, 40),
        }, "region5": {
            "region": (421, 312, 58, 142),
            "region_questions": range(41, 50),
        },
        "region6": {
            "region": (421, 482, 58, 142),
            "region_questions": range(51, 60),
        },
        "region7": {
            "region": (508, 313, 58, 142),
            "region_questions": range(61, 70),
        },
        "region8": {
            "region": (507, 482, 58, 142),
            "region_questions": range(71, 80),
        },
        "region9": {
            "region": (594, 311, 58, 142),
            "region_questions": range(81, 90),
        },
        "region10": {
            "region": (593, 482, 58, 142),
            "region_questions": range(91, 100),
        },

    }
}

answers = {
    1: "a",
    2: "a",
    3: "b",
    4: "b",
    5: "b",
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


def mark_sheet_base_on_region(image, region, region_range):
    """

    This is used to  make mark on the exam sheet an return the image
    :return:
    """
    x, y, width, height = region
    column_width = width // 5
    column_height = height // 10

    region_image = image[y:y + height, x:x + width]  # Extract the region of interest

    boxes = []

    for row_index in range(10):
        for col_index in range(5):
            # Get the top left and top right of each column in a row
            box_x = x + col_index * column_width
            box_y = y + row_index * column_height

            box = region_image[row_index * column_height:(row_index + 1) * column_height,
                  col_index * column_width:(col_index + 1) * column_width]
            # Convert the box array into an image
            box_image = cv2.cvtColor(box, cv2.COLOR_BGR2GRAY)

            # Append the box image to the list of box images
            boxes.append(box_image)
            # count non zero
            print(cv2.countNonZero(box_image))

            # # Color the  column by making a rectangle
            cv2.rectangle(image, (box_x, box_y), (box_x + column_width, box_y + column_height), (0, 255, 0), 2)

    return image, boxes


def mark_exam(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Resize the image to 700 by 700 for processing
    resized_image = cv2.resize(image, (700, 700))
    user_mark_sheets = []
    answer_count = 1
    for item in answer_regions.get("regions"):
        region = answer_regions["regions"][item]["region"]
        region_range = answer_regions["regions"][item]["region_questions"]
        resized_image, mark_sheet = mark_sheet_base_on_region(resized_image, region, region_range)
        user_mark_sheets.append(user_mark_sheets)
        cv2.imshow("img", mark_sheet[0])
    cv2.imshow("Original", resized_image)
    cv2.waitKey(0)


pdf_path = "./sheet.pdf"
output_dir = "./output"
extract_images_from_pdf(pdf_path, output_dir)

image_path = os.path.join(output_dir, "page_2.jpg")
mark_exam(image_path)
