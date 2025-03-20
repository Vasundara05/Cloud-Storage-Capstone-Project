import cv2
import os

# Define the save path
save_path = "C:/Users/derpt/OneDrive/Desktop/Varsha/CSA31/authorized_face.jpg"

# Ensure the directory exists
os.makedirs(os.path.dirname(save_path), exist_ok=True)

# Initialize the webcam
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

print("Press SPACE to capture your face.")

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    for (x, y, w, h) in faces:
        padding = 50  # Increase the face region by 50 pixels
        x, y = max(0, x - padding), max(0, y - padding)
        w, h = min(frame.shape[1] - x, w + 2 * padding), min(frame.shape[0] - y, h + 2 * padding)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw rectangle around face

    cv2.imshow("Capture Face", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 32:  # Spacebar key
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            x, y = max(0, x - padding), max(0, y - padding)
            w, h = min(frame.shape[1] - x, w + 2 * padding), min(frame.shape[0] - y, h + 2 * padding)

            face = gray[y:y + h, x:x + w]  # Extract the expanded face region
            face = cv2.resize(face, (400, 400))  # Save at a larger size
            cv2.imwrite(save_path, face)  # Save the image
            print(f"Face saved at: {save_path}")
            break  # Exit after capturing

        else:
            print("No face detected. Try again.")

    elif key == ord("q"):  # Press 'Q' to exit
        break

# Release webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
