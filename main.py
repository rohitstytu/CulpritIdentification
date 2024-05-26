import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import cv2
import face_recognition
import os
from datetime import datetime

#Speak out the Output printed texts
#import pyttsx3
#def print(word):
 ##  voices = engine.getProperty('voices')
   # engine.setProperty('voice', voices[1].id)
    #engine.setProperty('rate', 175)
    #engine.say(word)
    #engine.runAndWait()

class CustomDialog(simpledialog.Dialog):
    def buttonbox(self):
        box = tk.Frame(self)

        ok_button = tk.Button(box, text="Search", width=20, command=self.ok, default=tk.ACTIVE)
        ok_button.pack(side=tk.LEFT, padx=5, pady=5)

        cancel_button = tk.Button(box, text="Exit", width=5, command=self.cancel)
        cancel_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def apply(self):
        self.result = self.user_label_entry.get()

def get_user_label():
    root = tk.Tk()
    root.withdraw()
    root.title("Culprit Identification")

    class UserLabelDialog(CustomDialog):
        def body(self, master):
            culprit_label=tk.Label(master, text="Enter Culprit ID:", font=("Helvetica", 14)).grid(row=1, columnspan=2, pady=10)
            self.user_label_entry = tk.Entry(master, font=("Helvetica", 14))
            self.user_label_entry.grid(row=2, column=0, columnspan=2, pady=10)

            # Increase the size of the dialog window
            self.geometry("400x300")
            self.resizable(0,0)

            return self.user_label_entry

    dialog = UserLabelDialog(root)
    user_label = dialog.result

    return user_label

def load_user_images(directory_path):
    user_encodings = []
    labels = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            user_image_path = os.path.join(directory_path, filename)
            user_image = face_recognition.load_image_file(user_image_path)

            # Find face locations in the image
            face_locations = face_recognition.face_locations(user_image)

            if face_locations:
                # If at least one face is found, get the face encoding
                user_encoding = face_recognition.face_encodings(user_image, face_locations)[0]
                user_encodings.append(user_encoding)
                labels.append(os.path.splitext(filename)[0])  # Use filename without extension as label
            else:
                print(f"No face detected in '{filename}'\n")
                print(f"No face detected in '{filename}'\nProcessing Data")
                print("Processing Data...")
    print("Data Processing Task Completed")
    print("Data Processing Task Completed")
    return user_encodings, labels

def match_faces(user_encodings, labels, video_sources, user_images_directory):

    print("Enter Culprit Identification Number")
    user_label = get_user_label().lower()  # Get user input label in lower case
    file_path = os.path.join(user_images_directory, user_label)
    print(file_path+".jpg")

    if not os.path.exists(file_path+".jpg") or os.path.exists(file_path+".png"):
        print("Culprit Image not available!")
        print("Culprit Image not available. Update your database and try again")
        return

    print(f"Realtime Search Started. Activating Camera-{video_sources} Searching: {user_label}")
    video_captures = [cv2.VideoCapture(source) for source in video_sources]

    while True:
        frames = [capture.read()[1] for capture in video_captures]

        for frame, video_source in zip(frames, video_sources):
            # Find all face locations in the current frame
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Check if the face matches any of the users
                matches = face_recognition.compare_faces(user_encodings, face_encoding)
                color = (0, 0, 255)  # Default: Green but changed to red
                label = "Unknown"

                if any(matches):
                    idx = matches.index(True)
                    color = (0, 255, 0)  # Match: Green
                    label = labels[idx]
                    if label == user_label:
                        # Get the current date and time
                        current_datetime = datetime.now()
                        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                        print(f"{label}: Match found on Camera-{video_source} at {formatted_datetime}")
                        print(f"{label}: Match found on Camera-{video_source}")
                        result = messagebox.askyesno(f"Match found on Camera-{video_source}", "Do you want to proceed?")
                        if result:
                            continue
                        else:
                            print("System Shutdown Protocol Activate")
                            return

                # Draw rectangle around the face
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

                # Draw label
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, label, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

            # Display the resulting frame
            cv2.imshow(f'Video Source {video_source}', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("System Shutdown Protocol Activate")
            break

    # Release the video capture objects
    for capture in video_captures:
        capture.release()
    cv2.destroyAllWindows()

def get_user_images_directory():
    root = tk.Tk()
    root.withdraw()

    print("\t\tCulprit Identification Demo")
    print("*"*60)
    print("Choose your database directory")
    user_images_directory = filedialog.askdirectory(title="Select Directory Containing Culprit Images")
    return user_images_directory


if __name__ == "__main__":
    # Get user input path using Tkinter GUI
    user_images_directory = get_user_images_directory()
    print("\nInitializing Database Directory. Please Wait...")
    print("Initializing Database Directory. Please Wait...")

    # Check if the user selected a directory
    if not user_images_directory:
        print("Directory not selected. Exiting")
        print("Directory not selected. Exiting...")
    else:
        # Define one or more video sources
        video_sources = [1]

        # Load user face encodings and labels
        user_encodings, labels = load_user_images(user_images_directory)

        # Run the face matching program with labels and two video sources
        match_faces(user_encodings, labels, video_sources, user_images_directory)
