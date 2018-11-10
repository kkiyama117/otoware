import struct
import wave
from pathlib import Path

from numpy.ma import frombuffer

from src.convert_wav_and_array import ndarray_to_wav


def wav_to_ndarray():
    pass


def create_distortion_file(origin_path, result_path):
    # 音声をロード
    wf = wave.open(origin_path)
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
    new_data = distortion(data, 200, 0.3)
    # new_data = data

    # 正規化前のバイナリデータに戻す(32768倍)
    new_data = [int(x * 32767.0) for x in new_data]
    new_data = struct.pack("h" * len(new_data), *new_data)

    # 音声を保存
    ndarray_to_wav(new_data, channel, frame_rate, result_path)
    wf.close()


def distortion(data, gain, level):
    length = len(data)
    newdata = [0.0] * length
    for n in range(length):
        newdata[n] = data[n] * gain  # 増幅
        # クリッピング
        if newdata[n] > 1.0:
            newdata[n] = 1.0
        elif newdata[n] < -1.0:
            newdata[n] = -1.0
        # 音量を調整
        newdata[n] *= level
    return newdata
