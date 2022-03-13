import pyreadr
import pandas as pd
import os


def load_data(data_root: str) -> pd.DataFrame:
    """
    Load data, convert to pandas DataFrame and join 'performance' column
    """
    data_path = os.path.join(data_root, "AnalyticalSampleTask_Data.csv")
    perf_path = os.path.join(data_root, "performance.rds")
    performance = pyreadr.read_r(perf_path)
    data = pd.read_csv(data_path, sep="\t")
    df_perf = pd.DataFrame(performance[None], index=performance[None].index)
    df_perf.rename(columns={None: "performance"}, inplace=True)
    raw_data = data.join(df_perf)
    return raw_data
