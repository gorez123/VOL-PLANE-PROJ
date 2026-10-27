import cv2
import numpy as np


class VideoExporter:
    """מחלקה לאריזת רצף מטריצות דו-ממדיות (פריימים) לקובץ וידאו MP4."""

    def __init__(self, output_path: str, fps: int = 30, frame_size: tuple = None):
        """
        :param output_path: נתיב קובץ הווידאו לשמירה (סיומת .mp4)
        :param fps: קצב פריימים לשנייה (דרישת המטלה: לפחות 30)
        :param frame_size: גודל קבוע (width, height). אם None, ייקבע לפי הפריים הראשון.
        """
        self.output_path = output_path
        self.fps = fps
        self.frame_size = frame_size  # (width, height)
        self.writer = None

    def _normalize_frame(self, frame: np.ndarray) -> np.ndarray:
        """ממירה מטריצה גולמית לתמונת 8-ביט תלת-ערוצית (BGR) שמתאימה ל-OpenCV."""
        # אם התמונה לא בטווח uint8, ננרמל אותה ל-0..255
        if frame.dtype != np.uint8:
            min_val = frame.min()
            max_val = frame.max()
            if max_val > min_val:
                norm = ((frame - min_val) / (max_val - min_val) * 255.0).astype(np.uint8)
            else:
                norm = np.zeros_like(frame, dtype=np.uint8)
        else:
            norm = frame

        # וידוא 3 ערוצי צבע (BGR) עבור ה-VideoWriter
        if norm.ndim == 2:
            return cv2.cvtColor(norm, cv2.COLOR_GRAY2BGR)
        return norm

    def write_frame(self, frame: np.ndarray):
        """הוספת פריים בודד לווידאו."""
        bgr_frame = self._normalize_frame(frame)
        h, w = bgr_frame.shape[:2]

        # אתחול ה-Writer בפריים הראשון אם טרם אותחל
        if self.writer is None:
            if self.frame_size is None:
                self.frame_size = (w, h)
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.writer = cv2.VideoWriter(self.output_path, fourcc, self.fps, self.frame_size)

        # התאמת מידות הפריים לגודל הקבוע שנקבע לסרטון
        if (w, h) != self.frame_size:
            bgr_frame = cv2.resize(bgr_frame, self.frame_size, interpolation=cv2.INTER_NEAREST)

        self.writer.write(bgr_frame)

    def close(self):
        """סגירה ושחרור הקובץ בדיסק."""
        if self.writer is not None:
            self.writer.release()
            self.writer = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()