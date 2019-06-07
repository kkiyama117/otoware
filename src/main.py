from src.distortion import DistortionWavAndArray
from src.utils import get_data_file_path


def main():
    # 取得した引数
    otowari_level = 1024
    origin_file = "origin.wav"
    # 多分これと別にThreadを立ててotowari_levelを更新させればいい
    play_otowari(origin_file, otowari_level)


def play_otowari(file_name, distortion_level=20):
    origin_path = get_data_file_path(file_name)
    # wav_file=WavAndArray(origin_path)
    wav_file = DistortionWavAndArray(origin_path,
                                     distortion_level=distortion_level)
    wav_file.play_file()


if __name__ == '__main__':
    main()
