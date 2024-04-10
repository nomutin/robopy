"""Webカメラの制御を行うモジュール."""

import cv2
import numpy as np
import numpy.typing as npt


class CameraDriver(cv2.VideoCapture):
    """OpenCVを用いた, Webカメラの制御を行うクラス."""

    def __init__(
        self,
        camera_id: int,
        width: int = 320,
        height: int = 240,
    ) -> None:
        """カメラの初期化."""
        super().__init__(index=camera_id)
        self.camera_id = camera_id
        self.set(cv2.CAP_PROP_FPS, 60)
        self.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        if not self.isOpened():
            msg = f"Failed to open camera {camera_id}"
            raise RuntimeError(msg)

    def get_frame(self) -> npt.ArrayLike:
        """
        フレームをnp.ndarrayとして返す.

        Example:
        -------
        ```python
        driver = CameraDriver(camera_id)
        frame = driver.get_frame()
        print(frame.shape)
        ```

        """
        ret, frame = self.read()
        if not ret:
            msg = f"camera: {self.camera_id}からのフレーム取得に失敗."
            raise RuntimeError(msg)
        return np.array(frame[:, :, ::-1])

    def __del__(self) -> None:
        """GCで自動的にカメラのリソースを解放する."""
        self.release()
        cv2.destroyAllWindows()
