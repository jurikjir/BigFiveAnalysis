import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from tqdm import tqdm
import pandas as pd

from data_loader import load_data
from plot import plot_data
from preprocess import PreprocessData


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
        print("Plotting data. It may take a while...")
        plot_data(processed_data=processed_data)
    scores = ['E_score', 'N_score', 'A_score', 'C_score', 'O_score']
    inp = processed_data[scores]
    tgt = processed_data["performance"]
    train_inp, test_inp, train_tgt, test_tgt = train_test_split(inp, tgt, test_size=0.15, random_state=42)
    # model = LinearRegression()
    forest_model = RandomForestClassifier(n_estimators=100)
    linear_model = LinearRegression()
    forest_model.fit(train_inp, train_tgt)
    linear_model.fit(train_inp, train_tgt)
    forest_pred = forest_model.predict(test_inp)
    linear_pred = linear_model.predict(test_inp)
    forest_acc = metrics.accuracy_score(test_tgt, forest_pred)
    linear_acc = metrics.accuracy_score(test_tgt, np.round(linear_pred))
    regres_coefs = {value: coef for value, coef in zip(scores, linear_model.coef_)}
    regres_coefs["intercept"] = linear_model.intercept_
    print(f"Model metadata: {metadata}")
    print(f"Regression coefficients: {regres_coefs}")
    print(f"Forest accuracy : {forest_acc}%")
    print(f"Regression accuracy : {linear_acc}%")


if __name__ == '__main__':
    main(data_root="./data", save_plots=False)
