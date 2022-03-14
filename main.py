import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from data_loader import load_data
from preprocess import PreprocessData
from plot import PlotData


def main(data_root: str, save_plots: bool = False) -> None:
    """
    Function which loads data, preprocesses them and fits a model.
    Next plot data and save them into img folder.
    """
    raw_data = load_data(data_root=data_root)
    preprocessor = PreprocessData(raw_data=raw_data)
    metadata = preprocessor.get_metadata()
    processed_data = preprocessor.get_data()

    if save_plots:
        levels = ['E_level', 'N_level', 'A_level', 'C_level', 'O_level']
        plots = [sns.barplot, sns.boxplot, sns.violinplot]
        plotter = PlotData(imgdir_path="results")
        for level in tqdm(levels):
            for plot in plots:
                plotter.plot(
                    data=processed_data,
                    x=level,
                    y="performance",
                    plot=plot,
                    autosave=True)

    scores = ['E_score', 'N_score', 'A_score', 'C_score', 'O_score']
    inp = processed_data[scores]
    tgt = processed_data["performance"]
    train_inp, test_inp, train_tgt, test_tgt = train_test_split(inp, tgt, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(train_inp, train_tgt)
    pred = model.predict(test_inp)
    regres_coefs = {value: coef for value, coef in zip(scores, model.coef_)}
    regres_coefs["intercept"] = model.intercept_
    print(f"Model metadata: {metadata}")
    print(f"Regression coefficients: {regres_coefs}")


if __name__ == '__main__':
    main(data_root="./data", save_plots=True)
