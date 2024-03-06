import cv2
import face_recognition
import os
import time
def detect_face(user_name):
    # print("################################\n################################\n################################\n################################\n################################\n")
    # print("$$$$",user_name,"$$$$")
    # Path to the folder containing images of known faces 
    known_faces_folder = r"/Users/varsheethadari/Downloads/Advance ATM  using Facial Recognition and OTP/Face"

    # Load and encode known faces
    known_faces = []
    known_names = []

    # Iterate through each image file in the folder
    for file_name in os.listdir(known_faces_folder):
        if file_name.endswith(".jpg") or file_name.endswith(".png"):
            # Load the image file
            image_path = os.path.join(known_faces_folder, file_name)
            # Load the image file using face_recognition.load_image_file()
            image = face_recognition.load_image_file(image_path)
            
            # Encode the face in the image using face_recognition.face_encodings()
            face_encoding = face_recognition.face_encodings(image)
            
            # If a face is found, append it to the list of known_faces and its name to known_names
            if len(face_encoding) > 0:
                known_faces.append(face_encoding[0])
                # Assuming the file name contains the name of the person
                known_names.append(file_name.split('.')[0])

    # Now you have known_faces (list of face encodings) and known_names (list of corresponding names)
    # print(known_faces, known_names)

    # Capture video from the default camera (0)
    video_capture = cv2.VideoCapture(0)
    # print(known_faces,known_names)
    frame_count = 0
    max_frames = 30  # Set a maximum number of frames to process
    access_granted = False

    start_time = time.time()

    while frame_count < max_frames and not access_granted:
        # Capture a single frame from the video
        ret, frame = video_capture.read()

        # Resize frame to a smaller resolution to reduce processing load
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        
        # Find all face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        for face_encoding in face_encodings:
            # Compare each face encoding in the frame with the known faces
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = "Unknown"

            # Check if there's a match
            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]

            # Draw a rectangle around the face and display the name
            top, right, bottom, left = face_locations[0]
            cv2.rectangle(frame, (left*2, top*2), (right*2, bottom*2), (0, 0, 255), 2)  # Scale back to original size
            cv2.putText(frame, name, (left*2, bottom*2 + 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)

            # Check if the name is recognized and grant access
            if name == user_name:
                access_granted = True
                print("Access granted to "+name)
                end_time = time.time()
                elapsed_time = int(end_time - start_time)
                countdown = 5 - elapsed_time
                if countdown < 0:
                    countdown = 0
                cv2.putText(frame, f"Access Granted to ,"+name, (0, 0), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                return 1

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Increment frame count
        frame_count += 1

        # Check for exit condition
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    video_capture.release()
    cv2.destroyAllWindows()
    return 0
