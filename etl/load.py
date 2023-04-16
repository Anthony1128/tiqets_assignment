import os

import pandas as pd


class LoadJob:
    """Job for loading data into the destination."""

    def __init__(self):
        self.load_dir = os.path.abspath(os.curdir)

    def save_locally(self, df: pd.DataFrame, path: str):
        """Method to save DataFrame locally as csv file by provided path."""
        df.to_csv(os.path.join(self.load_dir, path), index=False)


job = LoadJob()
