import pytest
import pandas as pd

from etl.transform import TransformJob


class TestTransformJob:
    @pytest.mark.parametrize(
        "df, columns, expected_result",
        [
            (
                pd.DataFrame(
                    {
                        "barcode": [1111, 2222, 3333, 1111, 1111, 3333],
                        "order_id": [1, 2, 3, 3, 3, 1],
                    }
                ),
                ["barcode"],
                pd.DataFrame(
                    {
                        "barcode": [1111, 2222, 3333],
                        "order_id": [1, 2, 3],
                    }
                )
            ),
            (
                pd.DataFrame(
                    {
                        "barcode": [1111, 2222, 3333, 1111, 1111, 3333],
                        "order_id": [1, 2, 3, 3, 3, 1],
                    }
                ),
                ["barcode", "order_id"],
                pd.DataFrame(
                    {
                        "barcode": [1111, 2222, 3333, 1111, 3333],
                        "order_id": [1, 2, 3, 3, 1],
                    }
                )
            ),
            (
                pd.DataFrame(
                    {
                        "barcode": [],
                        "order_id": [],
                    }
                ),
                ["barcode", "order_id"],
                pd.DataFrame(
                    {
                        "barcode": [],
                        "order_id": [],
                    }
                )
            )
        ]
    )
    def test_handle_duplicates(self, df, columns, expected_result):
        job = TransformJob()
        result = job.handle_duplicates(df, columns)
        pd.testing.assert_frame_equal(expected_result.reset_index(drop=True), result.reset_index(drop=True))

    @pytest.mark.parametrize(
        "df, column, expected_result",
        [
            (
                pd.DataFrame(
                    {
                        "barcode": [1111, None, 3333, 1111, None, 3333],
                        "order_id": [1, 2, 3, 3, 3, 1],
                    }
                ),
                "barcode",
                pd.DataFrame(
                    {
                        "barcode": [1111, 3333, 1111, 3333],
                        "order_id": [1, 3, 3, 1],
                    }
                )
            ),
            (
                pd.DataFrame(
                    {
                        "barcode": [1111, None, 3333, 1111, None, 3333],
                        "order_id": [1, None, 3, None, 3, None],
                    }
                ),
                "order_id",
                pd.DataFrame(
                    {
                        "barcode": [1111, 3333, None],
                        "order_id": [1, 3, 3],
                    }
                )
            ),
        ]
    )
    def test_handle_empty_values(self, df, column, expected_result):
        job = TransformJob()
        result = job.handle_empty_values(df, column)
        pd.testing.assert_frame_equal(expected_result.reset_index(drop=True), result.reset_index(drop=True), check_dtype=False)

    @pytest.mark.parametrize(
        "df, group_column, column, sort_key, n_top, expected_result",
        [
            (
                pd.DataFrame(
                    {
                        "barcode": [(1, 2, 3), (1,), (1, 2), (1, 2, 3, 4), (1,), (1, 2, 3)],
                        "order_id": [1, 2, 3, 3, 3, 1],
                    }
                ),
                "order_id",
                "barcode",
                lambda col: col.str.len(),
                1,
                pd.DataFrame(
                    {
                        "order_id": [3],
                        "barcode": [(1, 2, 1, 2, 3, 4, 1)],
                    }
                )
            ),
            (
                pd.DataFrame(
                    {
                        "barcode": [111, 2222, 3333, 3333, 3333, 1111],
                        "order_id": [1, 2, 3, 3, 3, 1],
                    }
                ),
                "order_id",
                "barcode",
                lambda col: col,
                1,
                pd.DataFrame(
                    {
                        "order_id": [3],
                        "barcode": [9999],
                    }
                )
            ),
        ]
    )
    def test_find_top(self, df, group_column, column, sort_key, n_top, expected_result):
        job = TransformJob()
        result = job.find_top(df, group_column, column, sort_key, n_top)
        pd.testing.assert_frame_equal(expected_result.reset_index(drop=True), result.reset_index(drop=True))

    def test_transform(self):
        job = TransformJob()
        df_barcodes = pd.DataFrame(
            {
                "barcode": [1111, 2222, 3333, 4444, 5555],
                "order_id": [1, 2, 1, 3, 2],
            }
        )
        df_orders = pd.DataFrame(
            {
                "order_id": [1, 2, 3],
                "customer_id": [1, 2, 1],
            }
        )
        expected_result = pd.DataFrame(
            {
                "customer_id": [1, 1, 2],
                "order_id": [1, 3, 2],
                "barcode": [[1111, 3333], [4444], [2222, 5555]]
             }
        )
        result = job.transform_data(df_barcodes, df_orders)
        pd.testing.assert_frame_equal(expected_result.reset_index(drop=True), result.reset_index(drop=True))
