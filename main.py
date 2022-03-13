from preprocess import PreprocessData
from data_loader import load_data
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.model_selection import train_test_split


def main(data_root: str) -> None:
    """
    Function which loads data, preprocesses them and fits a model.
    """
    raw_data = load_data(data_root=data_root)
    preprocessor = PreprocessData(raw_data=raw_data)
    metadata = preprocessor.get_metadata()
    processed_data = preprocessor.get_data()
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
    main(data_root="./data")