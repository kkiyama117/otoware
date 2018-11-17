import struct
import wave
import pyaudio
from pathlib import Path

from numpy.ma import frombuffer


def wav_to_ndarray(path: Path):
    with path.open("rb") as f, wave.open(f) as wf:
        wav_data = get_wave_info(path=path)
        length = wav_data['frames']
        print(get_wave_info(path=path))
        return wf.readframes(length)


def get_wave_info(path: Path):
    """WAVEファイルの情報を取得"""
    with path.open("rb") as f, wave.open(f) as wf:
        return {'channel': wf.getnchannels(), 'width': wf.getsampwidth(),
                'frame_rate': wf.getframerate(), 'frames': wf.getnframes(),
                'params': wf.getparams(),
                "long": float(wf.getnframes() / wf.getframerate())
                }


def normalization(array) -> list:
    # エフェクトをかけやすいようにバイナリデータを[-1, +1]に正規化
    # wav -> numpy ndArray
    # int16 の絶対値は 32767
    return frombuffer(array, dtype="int16") / 32768.0


def de_normalization(array) -> bytes:
    # 正規化前のバイナリデータに戻す(32768倍)
    new_data = [int(x * 32767.0) for x in array]
    return struct.pack("h" * len(new_data), *new_data)


def ndarray_to_device(data: bytes, channel: int, width, rate):
    p = pyaudio.PyAudio()
    # Streamを生成(3)
    stream = p.open(format=p.get_format_from_width(width),
                    channels=channel,
                    rate=rate,
                    output=True)
    size = len(data)
    pos = 0  # byte count
    while pos < size:
        # frame_size
        frame_size = 1024
        o = data[pos:pos + frame_size]
        stream.write(o)
        pos += frame_size
    # time.sleep(float(size) / 2 / rate)
    stream.close()
    p.terminate()


# byte列を(本来のwavのデータの情報を元に再生)
def play_file(new_data, origin_path):
    wav_info = get_wave_info(origin_path)
    channel = wav_info['channel']
    width = wav_info['width']
    frame_rate = wav_info['frame_rate']
    # numpyのndarrayをデバイスのデフォルトの再生機器に送信
    ndarray_to_device(new_data, channel, width, frame_rate)


"""保存用関数群"""


# array をwav に変換して保存
def save_file(bit_array, origin_path: Path, result_path: Path):
    # 音声を保存
    wav_info = get_wave_info(origin_path)
    frame_rate = wav_info['frame_rate']
    channel = wav_info['channel']
    ndarray_to_wav(bit_array, channel=channel, rate=frame_rate,
                   path=result_path)


def ndarray_to_wav(data: bytes, channel: int, rate: int, path: Path):
    """波形データをWAVEファイルへ出力"""
    with path.open("wb") as f, wave.open(f, "w") as wf:
        wf.setnchannels(channel)
        # 16bit // 2 で サンプルサイズは2(らしい)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(data)
        print("data completely saved")
    print(get_wave_info(path=path))
