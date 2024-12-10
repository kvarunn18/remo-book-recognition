import take_picture as tp
import enhance_img as ei
import text_recog as tr
import get_book_data as gbd
from dotenv import load_dotenv
import os
import cv2

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Get the camera IP address
    camera_ip = os.getenv("CAMERA_IP")

    image_name = "frame1.jpg"
    input_path = r"scanned"

    url = f"http://{camera_ip}:8080//shot.jpg"

    # Scan front and back of the book
    tp.take_picture(url, input_path)

    image = cv2.imread(os.path.join(input_path, image_name))

    # Resize and enhance the image
    image = cv2.resize(image, (450, 727))
    enhanced_img = ei.enhance_image(image)

    # Perform OCR on the enhanced image
    text = tr.text_recog(enhanced_img)

    print("Recognized text:", text)

    # Use recognized text to get book data
    book_data = gbd.get_book_data(text)
    
    if type(book_data) == dict:
        print("Book data:")
        for key, value in book_data.items():
            print(f"{key}: {value}")
    else:
        print(book_data)

