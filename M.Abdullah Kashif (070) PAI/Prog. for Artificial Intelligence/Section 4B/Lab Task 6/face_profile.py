import cv2
import mediapipe as mp
import math

# live webcam detection 

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        image = cv2.flip(image, 1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_image)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                ih, iw, _ = image.shape

                def get_point(index):
                    landmark = face_landmarks.landmark[index]
                    return int(landmark.x * iw), int(landmark.y * ih)

                left_eye = get_point(33)
                right_eye = get_point(263)
                nose_top = get_point(1)
                nose_bottom = get_point(2)
                left_lip = get_point(61)
                right_lip = get_point(291)
                left_face = get_point(234)
                right_face = get_point(454)
                chin = get_point(152)
                forehead = get_point(10)

                important_points = [left_eye, right_eye, nose_top, nose_bottom,
                                    left_lip, right_lip, left_face, right_face,
                                    chin, forehead]

                for point in important_points:
                    cv2.circle(image, point, 3, (0, 255, 0), -1)

                eye_distance = math.hypot(right_eye[0] - left_eye[0], right_eye[1] - left_eye[1])
                nose_length = math.hypot(nose_bottom[0] - nose_top[0], nose_bottom[1] - nose_top[1])
                lip_width = math.hypot(right_lip[0] - left_lip[0], right_lip[1] - left_lip[1])
                face_width = math.hypot(right_face[0] - left_face[0], right_face[1] - left_face[1])
                face_height = math.hypot(chin[0] - forehead[0], chin[1] - forehead[1])

                cv2.putText(image, f"Eye Distance: {int(eye_distance)}px", (30, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                cv2.putText(image, f"Nose Length: {int(nose_length)}px", (30, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                cv2.putText(image, f"Lip Width: {int(lip_width)}px", (30, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                cv2.putText(image, f"Face Width: {int(face_width)}px", (30, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                cv2.putText(image, f"Face Height: {int(face_height)}px", (30, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        cv2.imshow('Full Face Profiling', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
