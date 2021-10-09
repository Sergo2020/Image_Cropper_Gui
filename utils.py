import cv2 as cv
import numpy as np
from pathlib import Path
import os


class Cropper:
    def __init__(self, src_dir: str, dst_dir: str,
                 src_ext: str, dst_est: str, dst_size: int) -> None:

        self.src_dir = Path(src_dir)
        self.dst_dir = Path(dst_dir)

        self.src_ext = src_ext
        self.dst_est = dst_est

        self.dst_size = dst_size
        self.dummy_crop = np.zeros((self.dst_size, self.dst_size, 3), dtype='uint8')

        self.src_list = None

        self.get_file_list()

    def get_file_list(self):
        self.src_list = list(self.src_dir.glob(rf'*.{self.src_ext}'))

    def img2crops(self, img_path):
        n_crops = 0
        img_src = cv.imread(str(img_path), -1)
        h, w = img_src.shape[:-1]

        times_h, times_w = h // self.dst_size, w // self.dst_size
        # TODO: Test images with increment

        for idx_h in range(times_h):
            for idx_w in range(times_w):
                crop = img_src[idx_h * self.dst_size: (idx_h + 1) * self.dst_size,
                       idx_w * self.dst_size: (idx_w + 1) * self.dst_size]

                dst_name = f"{img_path.stem}_h{idx_h * self.dst_size}_w{idx_w * self.dst_size}.{self.dst_est}"
                cv.imwrite(str(self.dst_dir / dst_name), crop)
                n_crops += 1

        return n_crops

    def __len__(self):
        return len(self.src_list)


def check_ex(path: str, create: bool = False) -> int:
    if len(path) > 1:
        path = Path(path)
    if not os.path.exists(path):
        if create:
            try:
                os.mkdir(path)
                return 2
            except:
                return 0
        else:
            return 0
    else:
        return 1
