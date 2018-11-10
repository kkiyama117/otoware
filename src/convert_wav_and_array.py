import struct
import wave
from pathlib import Path

from numpy.ma import frombuffer


def get_wave_info(path: Path):
    """WAVEファイルの情報を取得"""
    with path.open("rb") as f, wave.open(f) as wf:
        return {'channel': wf.getnchannels(), 'width': wf.getsampwidth(),
                'frame_rate': wf.getframerate(), 'frames': wf.getnframes(),
                'params': wf.getparams(),
                "long": float(wf.getnframes() / wf.getframerate())
                }


def wav_to_ndarray(path: Path):
    with path.open("rb") as f, wave.open(f) as wf:
        wav_data = get_wave_info(path=path)
        length = wav_data['frames']
        return wf.readframes(length)


def ndarray_to_wav(data: bytes, channel: int, fs: int, result_path: Path):
    """波形データをWAVEファイルへ出力"""
    with result_path.open("wb") as f, wave.open(f, "w") as wf:
        wf.setnchannels(channel)
        # 16bit // 2 で サンプルサイズは2(らしい)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(data)
        print("data completely saved")
    print(get_wave_info(path=result_path))


def normalization(array) -> list:
    # エフェクトをかけやすいようにバイナリデータを[-1, +1]に正規化
    # wav -> numpy ndArray
    # int16 の絶対値は 32767
    return frombuffer(array, dtype="int16") / 32768.0


def de_normalization(array) -> bytes:
    # 正規化前のバイナリデータに戻す(32768倍)
    new_data = [int(x * 32767.0) for x in array]
    return struct.pack("h" * len(new_data), *new_data)
