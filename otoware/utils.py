import sys
import pathlib
import struct

from numpy.ma import frombuffer


def get_data_file_path(file_name):
    file_path = pathlib.Path(file_name)
    if file_path.is_absolute():
        return file_path.resolve()
    else:
        # 相対PATHだった時.
        # venv etc.
        for data_dir_path in sys.path:
            file_path_venv = (pathlib.Path(data_dir_path) / 'otoware' / file_name).resolve()
            if file_path_venv.exists():
                return file_path_venv.resolve()
        file_path_dev = pathlib.Path.cwd() / "data" / file_name
        if file_path_dev.exists():
            return file_path_dev.resolve()
        else:
            print(file_path)
            raise OSError("wav file path not exist")


# 変換用関数群
def normalization(array) -> list:
    # エフェクトをかけやすいようにバイナリデータを[-1, +1]に正規化
    # ndArray -> ndArray
    # int16 の絶対値は 32767
    return frombuffer(array, dtype="int16") / 32768.0


def de_normalization(array) -> bytes:
    # 正規化前のバイナリデータに戻す(32768倍)
    new_data = [int(x * 32767.0) for x in array]
    return struct.pack("h" * len(new_data), *new_data)
