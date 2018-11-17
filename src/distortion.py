from pathlib import Path
import numpy as np
from src import convert_wav_and_array as cwa

class DistortionWavAndArray(cwa.WavAndArray):
    pass


# origin_path の　wavに対して, distortion した　arrayを返す
# リアルタイム処理の時は多分これでは駄目
def distortion_array(origin_path, gain=5):
    # 音声をロード→正規化→エフェクト→逆正規化
    return cwa.de_normalization(
        distortion(cwa.normalization(cwa.wav_to_ndarray(origin_path)), gain))


def realtime_distortion_array(origin_path, gain=5):
    data = cwa.wav_to_ndarray(origin_path)
    data_array = cwa.normalization(data)


# byteもしくはbyte列に対して distortion の処理をして送る
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
    # new_data = data * gain
    new_data = np.sign(data) * (1 - np.exp(-1 * gain * np.abs(data)))
    if clip:
        new_data = np.clip(new_data, -1.0, 1.0)
    # 音量を調整
    new_data *= level
    return new_data


# deprecated
# 今回は保存しないので使わない
def create_distortion_file(origin_path: Path, result_path: Path, gain):
    # distortion nd_array
    new_data = distortion_array(origin_path, gain)
    # 音声を保存
    cwa.save_file(new_data, origin_path, result_path)
