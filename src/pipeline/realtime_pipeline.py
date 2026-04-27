import cv2
from loguru import logger

from src.core.face_tracker import FaceTracker
from src.core.attention_engine import AttentionEngine


class RealtimePipeline:
    """
    End-to-end pipeline:
    Webcam → Face Tracking → Attention Engine → Output State
    """

    def __init__(self, camera_index=0):
        self.camera_index = camera_index

        self.tracker = FaceTracker()
        self.engine = AttentionEngine()

        self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():
            raise Exception("Camera not accessible")

        logger.info("RealtimePipeline initialized")

    def run(self):
        """
        Run full real-time system
        """

        logger.info("Starting real-time attention monitoring...")

        while True:
            ret, frame = self.cap.read()

            if not ret:
                logger.error("Failed to read frame")
                break

            # Step 1: Face Tracking
            frame, face_data = self.tracker.process_frame(frame)

            if face_data:
                landmarks = face_data[0]["landmarks"]

                # Step 2: Attention Analysis
                result = self.engine.classify_attention(landmarks)

                state = result["state"]
                score = result["score"]

                # Step 3: Overlay UI on frame
                cv2.putText(
                    frame,
                    f"{state} | Score: {score}",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
            else:
                state = "ABSENT"
                cv2.putText(
                    frame,
                    "NO FACE DETECTED",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2
                )

            cv2.imshow("Student Attention Monitoring", frame)

            # Exit on Q
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


# ---------------------------
# RUN PIPELINE
# ---------------------------
if __name__ == "__main__":

    pipeline = RealtimePipeline()
    pipeline.run()