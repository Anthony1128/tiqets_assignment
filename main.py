from etl import extract_job, load_job, transform_job


class DataProcessor:
    """Main class to process the data."""

    def __init__(self):
        self.destination = "result.csv"
        self.barcodes_path = "barcodes.csv"
        self.orders_path = "orders.csv"

    def run(self):
        """Entrypoint of data processing."""
        df_barcodes = extract_job.read_csv_file(self.barcodes_path)
        df_orders = extract_job.read_csv_file(self.orders_path)
        df_transformed = transform_job.transform_data(df_barcodes, df_orders)
        load_job.save_locally(df_transformed, self.destination)


if __name__ == "__main__":
    DataProcessor().run()
