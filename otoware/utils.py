import pathlib
import sys


def get_data_file_path(file_name):
    file_path = pathlib.Path(file_name)
    if file_path.is_absolute():
        return file_path.resolve()
    else:
        # 相対PATHだった時.
        # venv etc.
        file_path_venv = (pathlib.Path(sys.prefix) / "data" / file_name).resolve()
        if file_path_venv.exists():
            return file_path_venv
        # develop
        file_path_dev = (pathlib.Path.cwd() / "data" / file_name).resolve()
        if file_path_dev.exists():
            print("dev:", file_path_dev)
            return file_path_dev.resolve()
        else:
            print(file_path)
            raise OSError("wav file path not exist")
