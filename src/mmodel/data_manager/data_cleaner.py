from pandas import DataFrame


class Cleaner:
    def __init__(self) -> None:
        pass

    @staticmethod
    def select_rows(df: DataFrame, muncps):
        output = {}
        for c in df[muncps]:
            output[c] =  [int(v) for v in df.loc[:,[c]].values]

        return output