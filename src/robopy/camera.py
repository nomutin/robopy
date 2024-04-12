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
        fps: int = 60,
    ) -> None:
        """
        カメラの初期化.

        Note
        ----
        - カメラが対応していない `width`・`height`・`fps`を指定すると,
          この時点でエラーが発生する.
        - Intel Realsense の (width, height) = (640, 480) or (320, 240).
        - Intel Realsense の fps = 30 or 60.

        Parameters
        ----------
        camera_id : int
            カメラのID.
        width : int, default 320
            画像の幅.
        height : int, default 240
            画像の高さ.
        fps : int, default 60
            カメラのFPS.

        """
        super().__init__(index=camera_id)
        self.camera_id = camera_id
        self.set(cv2.CAP_PROP_FPS, fps)
        self.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        if not self.isOpened():
            msg = f"Failed to open camera {camera_id}"
            raise RuntimeError(msg)

    def get_frame(self) -> npt.ArrayLike:
        """
        現在の画像を `np.ndarray` として返す.

        Example
        -------
        ```python
        driver = CameraDriver(camera_id)
        frame = driver.get_frame()
        print(frame.shape)
        ```

        Note
        ----
        カメラによっては, 帰ってくる画像が BGR になっていたり,
        チャネルの次元が無かったりするので注意.

        Returns
        -------
        np.ndarray
            カメラから取得したフレーム.
            `self.height`・`self.width`のサイズの画像.

        """
        ret, frame = self.read()
        if not ret:
            msg = f"camera: {self.camera_id}からのフレーム取得に失敗."
            raise RuntimeError(msg)
        return np.array(frame)

    def __del__(self) -> None:
        """
        GCで自動的にカメラのリソースを解放する.

        Note:
        ----
        python インタプリタが `CameraDriver`が使われなくなったと解釈すると,
        自動的にこのメソッドが呼ばれる.

        """
        self.release()
        cv2.destroyAllWindows()
