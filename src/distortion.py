from pathlib import Path
import numpy as np
from src import convert_wav_and_array as cwa


# deprecated
def create_distortion_file(origin_path: Path, result_path: Path, gain):
    # distortion nd_array
    new_data = distortion_array(origin_path, gain)
    # 音声を保存
    save_file(new_data, origin_path, result_path)


def play_file(new_data, origin_path, result_path):
    # 音声を保存
    wav_info = cwa.get_wave_info(origin_path)
    channel = wav_info['channel']
    width = wav_info['width']
    frame_rate = wav_info['frame_rate']
    frames = wav_info['frames']
    cwa.ndarray_to_device(new_data, channel, width, frame_rate)


def play_distortion_file(origin_path: Path, result_path: Path, gain):
    # distortion nd_array
    new_data = distortion_array(origin_path, gain)
    # 音声を保存
    # play_file(new_data, origin_path, result_path)


# origin_path の　ファイルに対して, distortion した　arrayを返す
def distortion_array(origin_path, gain=5):
    # 音声をロード→正規化→エフェクト→逆正規化
    return cwa.de_normalization(
        distortion(cwa.normalization(cwa.wav_to_ndarray(origin_path)), gain))


# array をwav に変換して保存
def save_file(bit_array, origin_path: Path, result_path: Path):
    # 音声を保存
    wav_info = cwa.get_wave_info(origin_path)
    frame_rate = wav_info['frame_rate']
    channel = wav_info['channel']
    cwa.ndarray_to_wav(bit_array, channel, frame_rate, result_path)


def distortion(data, gain, level=0.7, clip=True):
    """gain乗の値をもちいてdistortion
    data: numpy.ndarray
    gain: 増幅の倍率
    level: 音量
    clip: ハードクリッピングするか(下記Qiitaか論文参照)
    """
    # https://qiita.com/stringamp/items/4b6e344ddf878f5099c7#122-%E5%AE%9F%E8%A3%85
    # 単純にgain倍増幅する時は以下
    # for n in range(length):
    # newdata = data * gain
    new_data = np.sign(data) * (1 - np.exp(-1 * gain * np.abs(data)))
    if clip:
        new_data = np.clip(new_data, -1.0, 1.0)
    # 音量を調整
    new_data *= level
    return new_data
