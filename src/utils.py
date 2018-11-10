from pathlib import Path


def get_data_file_path(file_name):
    file_path = Path(file_name)
    if file_path.is_absolute():
        return file_path.resolve()
    else:
        data_dir_path = Path(__file__).parents[1] / "data"
        file_path = data_dir_path / file_name
        return file_path.resolve()
