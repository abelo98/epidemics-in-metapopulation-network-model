from pandas import DataFrame


class Cleaner:
    def __init__(self) -> None:
        pass

    def select_rows(df: DataFrame,muncps):
        return dict(zip(muncps,[df.loc(df[m]) for m in muncps]))
         