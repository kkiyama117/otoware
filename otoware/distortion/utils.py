# 変換用関数群

import struct

import numpy


def normalization(array) -> list:
    # エフェクトをかけやすいようにバイナリデータを[-1, +1]に正規化
    # ndArray -> ndArray
    # int16 の絶対値は 32767
    return numpy.ma.frombuffer(array, dtype="int16") / 32768.0


def de_normalization(array) -> bytes:
    # 正規化前のバイナリデータに戻す(32768倍)
    new_data = [int(x * 32767.0) for x in array]
    return struct.pack("h" * len(new_data), *new_data)
