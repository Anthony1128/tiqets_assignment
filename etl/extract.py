import os

import pandas as pd


class ExtractJob:
    """Job for getting source data."""

    def __init__(self):
        self.data_folder = os.getenv("DATA_FOLDER", "data")
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

    def read_csv_file(self, path: str) -> pd.DataFrame:
        """Method to read csv file by provided path."""
        return pd.read_csv(
            os.path.join(self.current_dir, self.data_folder, path)
        ).convert_dtypes()


job = ExtractJob()
