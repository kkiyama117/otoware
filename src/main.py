from src.distortion import create_distortion_file
from src.utils import get_data_file_path


def main():
    # arg parse する
    origin_file = "origin.wav"
    otowari(origin_file)


def otowari(file_name):
    origin_path = get_data_file_path(file_name)
    result_file = "dist_" + origin_path.name
    result_path = get_data_file_path(result_file)
    create_distortion_file(origin_path, result_path)


if __name__ == '__main__':
    main()
