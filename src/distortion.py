import struct
import wave
from pathlib import Path

from numpy.ma import frombuffer
import numpy as np

from src.convert_wav_and_array import ndarray_to_wav


def wav_to_ndarray():
    pass


def create_distortion_file(origin_path: Path, result_path: Path, gain=5):
    # 音声をロード
    wf = wave.open(origin_path.open("rb"))
    print(origin_path)
    # 音声データの取得
    frame_rate = wf.getframerate()
    length = wf.getnframes()
    channel = wf.getnchannels()
    data = wf.readframes(length)

    # エフェクトをかけやすいようにバイナリデータを[-1, +1]に正規化
    # wav -> numpy ndArray
    # int16 の絶対値は 32767
    data = frombuffer(data, dtype="int16") / 32768.0

    # ここでサウンドエフェクト
    new_data = distortion(data, gain)
    # new_data = data

    # 正規化前のバイナリデータに戻す(32768倍)
    new_data = [int(x * 32767.0) for x in new_data]
    new_data = struct.pack("h" * len(new_data), *new_data)

    # 音声を保存
    ndarray_to_wav(new_data, channel, frame_rate, result_path)
    wf.close()


def distortion(data, gain=5, level=0.5):
    """gain乗の値をもちいてdistortion
    data: numpy.ndarray
    gain: 増幅の倍率
    level: 音量
    """
    new_data = np.sign(data) * (1 - np.exp(-1 * gain * np.abs(data)))
    # 単純に増幅する時は以下
    # for n in range(length):
    # newdata[n] = data[n] * gain
    # https://qiita.com/stringamp/items/4b6e344ddf878f5099c7#122-%E5%AE%9F%E8%A3%85
    # クリッピング
    # if is_clip:
    #     if new_data[n] > 1.0:
    #         new_data[n] = 1.0
    #     elif new_data[n] < -1.0:
    #         new_data[n] = -1.0
    # 音量を調整
    new_data *= level
    return new_data
