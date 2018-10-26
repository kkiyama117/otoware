import struct
import wave
from pathlib import Path

from numpy.ma import frombuffer


def print_wave_info(wf):
    """WAVEファイルの情報を取得"""
    print("チャンネル数:", wf.getnchannels())
    print("サンプル幅:", wf.getsampwidth())
    print("サンプリング周波数:", wf.getframerate())
    print("フレーム数:", wf.getnframes())
    print("パラメータ:", wf.getparams())
    print("長さ（秒）:", float(wf.getnframes()) / wf.getframerate())


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


def save(data, fs, bit, filename):
    """波形データをWAVEファイルへ出力"""
    wf = wave.open(filename, "w")
    wf.setnchannels(1)
    wf.setsampwidth(bit // 8)
    wf.setframerate(fs)
    wf.writeframes(data)
    wf.close()


def otowari(origin_file, result_file):
    origin_path = str(Path(origin_file).resolve())
    result_path = str(Path(result_file).resolve())
    # 音声をロード
    wf = wave.open(origin_path)
    print_wave_info(wf)
    # 音声データの取得
    fs = wf.getframerate()
    length = wf.getnframes()
    data = wf.readframes(length)

    # エフェクトをかけやすいようにバイナリデータを[-1, +1]に正規化
    data = frombuffer(data, dtype="int16") / 32768.0

    # ここでサウンドエフェクト
    new_data = distortion(data, 200, 0.3)

    # 正規化前のバイナリデータに戻す
    new_data = [int(x * 32767.0) for x in new_data]
    new_data = struct.pack("h" * len(new_data), *new_data)

    # サウンドエフェクトをかけた音声を保存
    save(new_data, fs, 16, result_path)
