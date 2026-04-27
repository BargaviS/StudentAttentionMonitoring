import cv2
import mediapipe as mp


class FaceTracker:
    def __init__(self):
        # FIXED: proper mediapipe import usage
        self.mp_face_mesh = mp.solutions.face_mesh

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        )

    def get_attention_score(self, frame):
        """
        Returns attention score (0–100)
        based on eye openness proxy
        """

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.face_mesh.process(rgb_frame)

        if not result.multi_face_landmarks:
            return 0

        landmarks = result.multi_face_landmarks[0].landmark

        # Eye landmarks (stable indices)
        left_eye = landmarks[159]
        right_eye = landmarks[386]

        # Attention proxy calculation
        eye_distance = abs(left_eye.y - right_eye.y)

        score = eye_distance * 5000

        # clamp between 0–100
        if score > 100:
            score = 100
        if score < 0:
            score = 0

        return score