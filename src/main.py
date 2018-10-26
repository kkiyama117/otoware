from pathlib import Path

from src.distortion import create_distortion_file


def get_data_file_path(filename):
    file_path = Path(filename)
    if file_path.is_absolute():
        return file_path.resolve()
    else:
        data_dir_path = Path(__file__).parents[1] / "data"
        file_path = data_dir_path / filename
        return file_path.resolve()


def otowari(origin_file):
    origin_path = get_data_file_path(origin_file)
    result_file = "dist_" + origin_path.name
    result_path = get_data_file_path(result_file)
    create_distortion_file(str(origin_path),
                           str(result_path))


def main():
    # arg parse する
    origin_file = "origin.wav"
    otowari(origin_file)


if __name__ == '__main__':
    main()
