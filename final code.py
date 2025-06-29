import cv2
import numpy as np
import matplotlib.pyplot as plt

def biggest_black_hole(image_path):
    # Calibration
    microns_per_pixel = 500 / 580  # µm/pixel
    area_per_pixel = microns_per_pixel ** 2  # µm²/pixel

    # Step 1: Load grayscale
    gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if gray is None:
        raise IOError("Image not found")
    

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    


    # Step 2: Adaptive thresholding
    adaptive = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        blockSize=11,
        C=5
    )

    # extra try 
    #midian = cv2.medianBlur(adaptive, 5)
    # Apply erosion and dilation
    #dilated = cv2.dilate(midian, kernel, iterations=1)
    #eroded = cv2.erode(dilated, kernel, iterations=1)
    
    # Step 2.1: Remove small noise
    eroded = cv2.morphologyEx(
        adaptive,
        cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    )
    
    # Step 3: Morphological closing
    closed = cv2.morphologyEx(
        adaptive,
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    )

    # Step 4: Isolate largest component
    num_labels, labels = cv2.connectedComponents(closed)
    if num_labels > 1:
        max_label = 1 + np.argmax(np.bincount(labels.flat)[1:])
        wound_only = (labels == max_label).astype(np.uint8) * 255
    else:
        wound_only = closed

    # Step 5: Find contours on inverted mask
    inverted = cv2.bitwise_not(wound_only)
    _, hole_mask = cv2.threshold(inverted, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(
        hole_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    h, w = gray.shape
    best_contour, best_area_px = None, 0
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        if x == 0 or y == 0 or x+cw == w or y+ch == h:
            continue  # skip border contours
        area = cv2.contourArea(cnt)
        if area > best_area_px:
            best_area_px = area
            best_contour = cnt

    if best_contour is None:
        print("❌ No valid wound contour found.")
        return

    # Compute area in µm²
    best_area_um2 = best_area_px * area_per_pixel

    # Step 6: Draw contour and label
    vis = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(vis, [best_contour], -1, (0, 255, 0), 2)

    M = cv2.moments(best_contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        cv2.putText(vis, "1", (cx, cy),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Step 7: Show original and annotated images
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.imshow(gray, cmap='gray')
    plt.title("Original Image")
    plt.axis("off")


    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB))
    plt.title(f"Wound Area ≈ {best_area_um2:.0f} μm²")
    plt.axis("off") 

    plt.tight_layout()
    plt.show()

    print(f"✅ Wound Area = {best_area_px:.0f} px² ≈ {best_area_um2:.2f} μm²")

if __name__ == "__main__":
    image_path = "/Users/nadavcohen/Desktop/Universuty/final_project/phyton_code/images 18.5/4.1 0.tif"
    biggest_black_hole(image_path)