import cv2
import numpy as np


class VideoExporter:
    """Context manager for streaming and encoding 2D projection matrices into MP4 video."""

    def __init__(self, output_path: str, fps: int = 30, frame_size: tuple = None):
        self.output_path = output_path
        self.fps = fps
        self.frame_size = frame_size  # (width, height)
        self.writer = None

    def _normalize_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Normalizes any 2D input array (uint8, uint16, int32, float) to 8-bit BGR format.
        """
        if frame.dtype != np.uint8:
            min_val = float(frame.min())
            max_val = float(frame.max())
            if max_val > min_val:
                norm = ((frame.astype(np.float32) - min_val) / (max_val - min_val) * 255.0).astype(np.uint8)
            else:
                norm = np.zeros(frame.shape, dtype=np.uint8)
        else:
            norm = frame

        if norm.ndim == 2:
            return cv2.cvtColor(norm, cv2.COLOR_GRAY2BGR)
        return norm

    def write_frame(self, frame: np.ndarray):
        """Encodes and appends a single frame to the video output stream."""
        if frame.size == 0:
            return

        bgr_frame = self._normalize_frame(frame)
        h, w = bgr_frame.shape[:2]

        if self.writer is None:
            if self.frame_size is None:
                self.frame_size = (w, h)

            # נסיון עם קודק mp4v, ובמידת הצורך fallback
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.writer = cv2.VideoWriter(self.output_path, fourcc, self.fps, self.frame_size)

            if not self.writer.isOpened():
                fourcc = cv2.VideoWriter_fourcc(*'avc1')
                self.writer = cv2.VideoWriter(self.output_path, fourcc, self.fps, self.frame_size)

        if (w, h) != self.frame_size:
            bgr_frame = cv2.resize(bgr_frame, self.frame_size, interpolation=cv2.INTER_NEAREST)

        self.writer.write(bgr_frame)

    def close(self):
        """Releases the video writer buffer to disk."""
        if self.writer is not None:
            self.writer.release()
            self.writer = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()