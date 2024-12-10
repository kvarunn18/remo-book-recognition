import cv2
import os
import numpy as np

def enhance_image(original_image):
    # contrast
    lab = cv2.cvtColor(original_image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    enhanced_lab = cv2.merge((cl, a, b))

    enhanced_img =  cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

    # denoise
    enhanced_img = cv2.bilateralFilter(enhanced_img, 9, 75, 75)
    return enhanced_img
    
    # shadow removal
    # rgb_planes = cv2.split(enhanced_img)
    # result_planes = []
    # for plane in rgb_planes:
    #     dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
    #     bg_img = cv2.medianBlur(dilated_img, 21)
    #     diff_img = 255 - cv2.absdiff(plane, bg_img)
    #     result_planes.append(diff_img)
    # enhanced_img = cv2.merge(result_planes)

    # # edge enhancement
    #     # gray = cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2GRAY)
    #     # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    #     # enahnced_img = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)

    # # edge detection
    # enhanced_img = cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2GRAY)
    # enhanced_img = cv2.GaussianBlur(enhanced_img, (3, 3), 0)

    # edges = cv2.Canny(enhanced_img, 100, 200)
    # enhanced_img = cv2.bitwise_and(enhanced_img, enhanced_img, mask=edges)

    # enhanced_img = cv2.cvtColor(enhanced_img, cv2.COLOR_GRAY2BGR)


