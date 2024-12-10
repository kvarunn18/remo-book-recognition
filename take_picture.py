import cv2
import numpy as np
import requests 
import imutils 


def detect_book_in_rectangle(frame, x1, y1, x2, y2):
    """
    Detects if a book (rectangle-shaped object) is within the given coordinates.
    """
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check for the largest contour that fits within the rectangle
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Check if the contour has four sides (potentially a rectangle)
        if len(approx) == 4:
            # check if the contour is a rectangle
            if not cv2.isContourConvex(approx):
                continue
            

            # Get the bounding box of the contour
            x, y, w, h = cv2.boundingRect(approx)

            # Check if the bounding box fits within the rectangle
            if x1-5 <= x <= x1+70 and y1-5 <= y <= y1+70 and x2-70 <= x + w <= x2+5 and y2-70 <= y + h <= y2+5:
                # draw with x, y, w, h
                cv2.drawContours(frame, [approx], 0, (0, 0, 255), 2)
                return True
            

    return False


def crop_to_rectangle(frame, x1, y1, x2, y2):
    """
    Crops the frame to the exact rectangle coordinates.
    """
    return frame[y1:y2, x1:x2]


def take_picture(url, save_path):

    step = 0

    countdown = -1

    while True:
        # Exit if the user presses 'q' or all frames are captured
        if step > 1 or (cv2.waitKey(1) & 0xFF == ord('q')):
            break
        img_resp = requests.get(url) 
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8) 
        img = cv2.imdecode(img_arr, -1) 
        img = imutils.resize(img, width=1000, height=1800)

        frame = img
        frame2 = frame.copy()

        height, width, _ = frame.shape

        # Define rectangle coordinates for each step
        if step == 0 and countdown == -1:
            x1, y1, x2, y2 = width // 4, 50, width // 2 + width // 5, height - 1000
            color = (0, 255, 0)
            text = "Place book front here"
        elif step == 1 and countdown == -1:
            x1, y1, x2, y2 = width // 4 - width // 10, 50, width // 2 + width // 10, height - 1000
            color = (0, 255, 0)
            text = "Place book back here"

        # Draw rectangle on the frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        if(countdown > 0):
            countdown -= 1
        elif(countdown == 0):
            step += 1
            countdown = -1

        # Check for book detection
        if detect_book_in_rectangle(frame2, x1, y1, x2, y2) and countdown == -1:
            # Save the cropped rectangle region
            cropped_frame = crop_to_rectangle(frame, x1, y1, x2, y2)
            cv2.imwrite(f"{save_path}/frame{step + 1}.jpg", cropped_frame)
            print(f"Saved frame{step + 1} with exact rectangle dimensions.")
            countdown = 10
            text = "Registering..."

        # Display the resulting frame
        cv2.imshow('Place the book', frame)

    # Release the camera and close windows
    cv2.destroyAllWindows()