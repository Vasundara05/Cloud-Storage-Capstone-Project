import cv2
import numpy as np
import os
import time
import psutil  

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Load the authorized face image
authorized_face_path = r"C:\Users\derpt\OneDrive\Desktop\Varsha\CSA31\authorized_face.jpg"
authorized_face = cv2.imread(authorized_face_path, cv2.IMREAD_GRAYSCALE)

if authorized_face is None:
    print("No authorized face found! Run the capture script first.")
    exit()

# Function to check if a USB device is connected
def is_usb_connected():
    usb_detected = False
    for device in psutil.disk_partitions():
        if "removable" in device.opts:
            usb_detected = True
            break
    return usb_detected

# Function to authenticate user based on face recognition
def authenticate_face():
    cap = cv2.VideoCapture(0)
    print("Press SPACE to authenticate...")

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Authentication", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 32:  # Press SPACE to capture and compare
            if len(faces) > 0:
                (x, y, w, h) = faces[0]
                detected_face = gray[y:y+h, x:x+w]
                detected_face = cv2.resize(detected_face, (400, 400))

                # Compare faces using Histogram
                hist1 = cv2.calcHist([authorized_face], [0], None, [256], [0, 256])
                hist2 = cv2.calcHist([detected_face], [0], None, [256], [0, 256])

                hist1 = cv2.normalize(hist1, hist1).flatten()
                hist2 = cv2.normalize(hist2, hist2).flatten()

                similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
                print(f"🔍 Match Score: {similarity:.2f}")

                cap.release()
                cv2.destroyAllWindows()

                if similarity > 0.80:  
                    print("Face recognized! Access granted.")
                    return True
                else:
                    print("Face not recognized! Access denied.")
                    return False

        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return False

# Function to grant access to cloud storage
def grant_cloud_access():
    secure_folder = r"C:\Users\derpt\OneDrive\SecureFolder"  # Change this to your actual folder

    # Grant access to the folder (remove restrictions)
    os.system(f'icacls "{secure_folder}" /grant Everyone:(OI)(CI)F')
    print("🔓 SecureFolder is now unlocked!")

    # Open the folder
    os.startfile(secure_folder)
    time.sleep(5)

    # Re-lock the folder after 30 seconds
    print("Locking SecureFolder after 30 seconds...")
    time.sleep(30)
    os.system(f'icacls "{secure_folder}" /deny Everyone:(OI)(CI)F')
    print("SecureFolder is locked again.")

# Main Function
if __name__ == "__main__":
    print("🔌 Checking USB device...")

    if is_usb_connected():
        print("USB detected! Proceeding with authentication...")
        if authenticate_face():
            grant_cloud_access()
        else:
            print("Access denied. USB storage remains locked.")
    else:
        print("No USB device detected! Insert a USB drive to continue.")
