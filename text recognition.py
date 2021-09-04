import cv2import numpy as npimport pytesseract# Load image, create mask, grayscale, Otsu's thresholdimage = cv2.imread('/Users/shreyashrivastava/Desktop/sample.png')mask = np.zeros(image.shape, dtype=np.uint8)gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]# Filter for ROI using contour area and aspect ratiocnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)cnts = cnts[0] if len(cnts) == 2 else cnts[1]custom_config = r'--oem 3 --psm 6'details = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT, config=custom_config, lang='eng')total_boxes = len(details['text'])for i in range(total_boxes):    if int(details['conf'][i])>5:        (x, y, w, h) = (details['left'][i], details['top'][i],                        details['width'][i],  details['height'][i])        thresh = cv2.rectangle(thresh, (x, y), (x + w, y + h), (0, 255, 0), 2)        cv2.imshow('captured text', thresh)        cv2.waitKey(0)        cv2.destroyAllWindows()        cv2.waitKey(1)for c in cnts:    area = cv2.contourArea(c)    peri = cv2.arcLength(c, True)    approx = cv2.approxPolyDP(c, 0.05 * peri, True)    x,y,w,h = cv2.boundingRect(approx)    aspect_ratio = w / float(h)    if area > 2000 and aspect_ratio > .5:        mask[y:y+h, x:x+w] = image[y:y+h, x:x+w]       data = pytesseract.image_to_string(mask, lang='eng', config='--psm 6')print(data)with open('result_text.txt',  'w', newline="") as file:    file.write(data)