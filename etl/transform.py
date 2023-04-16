from typing import Callable, List

import pandas as pd

from common import app_logger


class TransformJob:
    """Job for applying transformations."""

    @staticmethod
    def handle_duplicates(df: pd.DataFrame, columns: List) -> pd.DataFrame:
        """Method to handle duplicated rows within provided set of columns."""
        duplicate_rows = df[df.duplicated(subset=columns)]
        df_deduplicated = df.drop_duplicates(subset=columns)

        for row_number, row_data in duplicate_rows.to_dict("index").items():
            row_number += 2
            app_logger.error(
                f"Duplicate found - barcode: {row_data['barcode']}, order_id: {row_data['order_id']} - csv line {row_number}"
            )

        return df_deduplicated

    @staticmethod
    def handle_empty_values(df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Method to handle empty values within provided column."""
        empty_rows = df[df[column].isnull()]
        handled_df = df.dropna(subset=[column])

        for row_data in empty_rows.to_dict("records"):
            app_logger.error(f"Empty value in column [{column}] found - {row_data}")

        return handled_df

    @staticmethod
    def find_top(
        df: pd.DataFrame, group_column: str, column: str, sort_key: Callable, n_top: int = 5
    ) -> pd.DataFrame:
        """Method to find specified number of top rows by provided sorting
        function."""
        df_group = df.groupby(group_column).sum()
        df_sorted = df_group.sort_values(column, ascending=False, key=sort_key)
        top_rows = df_sorted.head(n_top).reset_index()
        return top_rows

    def transform_data(self, df_barcodes: pd.DataFrame, df_orders: pd.DataFrame):
        """Entrypoint for applying transformations to the Dataframes."""
        df_barcodes = self.handle_duplicates(df_barcodes, columns=["barcode"])
        barcodes_left = df_barcodes["order_id"].isnull().sum()
        df_joined = df_orders.merge(
            df_barcodes, on="order_id", how="outer", validate="one_to_many"
        )
        df_joined = self.handle_empty_values(df_joined, "barcode")
        df_result = df_joined.groupby(["customer_id", "order_id"], as_index=False)[
            "barcode"
        ].apply(list)
        top_customers = self.find_top(
            df_result, "customer_id", "barcode", sort_key=lambda col: col.str.len()
        )

        for i, row in top_customers.iterrows():
            app_logger.info(
                f"Top {i + 1} customer: {row['customer_id']}, {len(row['barcode'])}"
            )

        app_logger.info(f"The amount of unused barcodes: {barcodes_left}")

        return df_result


job = TransformJob()
