import wave
from pathlib import Path


def ndarray_to_wav(data, channel: int, fs: int, result_path: Path):
    """波形データをWAVEファイルへ出力"""
    with result_path.open("w") as f, wave.open(f, "w") as wf:
        wf.setnchannels(channel)
        # 16bit // 2 で サンプルサイズは2(らしい)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(data)
        print("data completely saved")
    _print_wave_info(result_path)


def _print_wave_info(path: Path):
    """WAVEファイルの情報を取得"""
    with path.open() as f, wave.open(f) as wf:
        print("チャンネル数:", wf.getnchannels())
        print("サンプル幅:", wf.getsampwidth())
        print("サンプリング周波数:", wf.getframerate())
        print("フレーム数:", wf.getnframes())
        print("パラメータ:", wf.getparams())
        print("長さ（秒）:", float(wf.getnframes()) / wf.getframerate())
