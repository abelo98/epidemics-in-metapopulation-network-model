from pandas import DataFrame


class Cleaner:
    def __init__(self) -> None:
        pass

    @staticmethod
    def select_rows(df: DataFrame, muncps):
        return dict(zip(muncps, df[muncps]))
