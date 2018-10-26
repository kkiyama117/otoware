from pathlib import Path

from src.distortion import otowari


def get_data_file_path(filename):
    file_path = Path(filename)
    if file_path.is_absolute():
        return file_path.resolve()
    else:
        data_dir_path = Path(__file__).parents[1] / "data"
        file_path = data_dir_path / filename
        return file_path.resolve()


def main():
    origin_file = "origin.wav"
    result_file = "distortion.wav"

    otowari(str(get_data_file_path(origin_file)),
            str(get_data_file_path(result_file)))


if __name__ == '__main__':
    main()
