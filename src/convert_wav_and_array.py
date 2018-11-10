import wave
from pathlib import Path


def ndarray_to_wav(data, channel: int, fs: int, result_path: Path):
    """波形データをWAVEファイルへ出力"""
    try:
        wf = wave.open(result_path, "w")
        wf.setnchannels(channel)
        # 16bit // 2 で サンプルサイズは2(らしい)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(data)
    except IOError:
        print("file can not save")
    else:
        wf.close()
        print("data completely saved")
    finally:
        print("save func finished")
        # _print_wave_info(result_path)


def _print_wave_info(file: Path):
    """WAVEファイルの情報を取得"""
    try:
        wf = wave.open(Path,"r")
    except IOError:
        print(f"can't get info for {file.name}")
    else:
        print("チャンネル数:", wf.getnchannels())
        print("サンプル幅:", wf.getsampwidth())
        print("サンプリング周波数:", wf.getframerate())
        print("フレーム数:", wf.getnframes())
        print("パラメータ:", wf.getparams())
        print("長さ（秒）:", float(wf.getnframes()) / wf.getframerate())
