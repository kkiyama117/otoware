from src.distortion import create_distortion_file
from src.utils import get_data_file_path
import argparse


def main():
    # arg parse する
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("otowari_level", help="input number",
                        type=int)
    # 取得した引数
    args = parser.parse_args()
    otowari_level = args.otowari_level
    print("input:", otowari_level)
    origin_file = "origin.wav"
    play_otowari(origin_file, otowari_level)


def play_otowari(file_name, distortion_level=20):
    origin_path = get_data_file_path(file_name)
    result_file = "dist_" + origin_path.name
    result_path = get_data_file_path(result_file)
    create_distortion_file(origin_path, result_path, gain=distortion_level)


if __name__ == '__main__':
    main()
