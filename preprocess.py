from itertools import groupby
from typing import Callable, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pycountry
import seaborn as sns

from maps import ans_map, maps, strfwd_score_map


def init_metadata(data: pd.DataFrame, metadata: str,) -> Tuple[pd.DataFrame, str]: 
    """
    Add header to metadata buffer
    """
    metadata += "Big Five Personality Traits Dataset\n" + 80 * "-" + "\n"
    return data, metadata


def process_age(
    data: pd.DataFrame,
    metadata: str,
    survey_year: int = 2012,
    min_age: int = 13) -> Tuple[pd.DataFrame, str]:
    """
    Repairs items column 'age' in data. Some participants have
    filled incorrectly their age as the year of birth, this function calculates
    the true age based on the date when the survey was conducted. Samples which
    contains unreasonable values such as age=99999 are dropped, since inputs
    from such participants should not be taken seriously. Participants younger
    than min_age are also dropped.
    """
    dataset_len = len(data)
    metadata += f"Dataset lenght before preprocessing: {dataset_len}\n"
    byears = data[(data["age"]>1912) & (data["age"]<2009)]["age"]
    byears_cnt, byears_unq = len(byears), byears.unique()
    rpr_age_map = {byear: survey_year - byear for byear in byears_unq}
    data.replace({"age": rpr_age_map}, inplace=True)
    drop_cnt = len(data[(data["age"]<min_age) | (data["age"]>105)])
    data = data[(data["age"]>min_age) & (data["age"]<105)]
    metadata += f"Age column:\n{byears_cnt} of rows repaired \n{drop_cnt} of rows dropped\n"
    return data, metadata


def process_country(data: pd.DataFrame, metadata: str) -> Tuple[pd.DataFrame, str]:
    """
    Remove such rows, where values form 'country' column are not
    in ISO countries list
    """
    dataset_len = len(data)
    iso_countries = [country.alpha_2 for country in pycountry.countries]
    not_in_iso = [c for c in data["country"].unique() if c not in iso_countries]
    drop_cnt = len(data[data["country"].isin(not_in_iso)])
    data = data[data["country"].isin(iso_countries)]
    metadata += f"Country column:\n{drop_cnt} rows dropped because not present in ISO countries\n"
    return data, metadata


def apply_maps(data: pd.DataFrame, metadata: str) -> Tuple[pd.DataFrame, str]:
    """
    Apply maps to dataframe. Maps are defined in maps.py and
    serves as conversion from digit representations to human readable values.
    This is handy for plotting later. 
    Example:
    hand = 1 -> hand_str = 'Right'
    """
    for k, v in maps.items():
        data[f"{k}_str"] = data[k].map(v)
    metadata += f"Additional columns: {list(maps.keys())}_str were added \n"
    return data, metadata


def remove_zero_ans(data: pd.DataFrame, metadata: str) -> Tuple[pd.DataFrame, str]:
    """
    Remowe rows with zero vale answers. User probably did not
    answer the question, if zero is present.
    """
    traits = ["E", "N", "A", "C", "O"]
    answers = [column for column in data.columns if column[0] in traits]
    for ans in answers:
        data.drop(data.loc[data[ans]==0].index, inplace=True)
    return data, metadata


def calculate_scores(data: pd.DataFrame, metadata: str) -> Tuple[pd.DataFrame, str]:
    """
    Calculate score for each trait in 0-100 scale. Each trait 
    consist of 10 questions and answers. Score is calculated as a sum of values
    representing answers in following manner:
    
    Initial value is set to 50 since it is neutral vale in given range. Initial
    value is then increased or decreased by weighted value of the answer to
    the question. Some of the questions are designed in reversed manner,
    which means that value which would be normally added is substracted.
    
    Example: 
        Q: I am the life of the party. A: 5 -> score += 5
        Q: I am the life of the party. A: 1 -> score -= 5
        Q: I don't talk a lot. A: 5 -> score -= 5
        Q: I don't talk a lot. A: 1 -> score += 5
    """
    traits = ["E", "N", "A", "C", "O"]
    ans = [column for column in data.columns if column[0] in traits]
    group_ans = [list(group) for key, group in groupby(ans, key=lambda x: x[0])]
    traits_ans = {k: v for k, v in zip(traits, group_ans)}
    rvs_ans_map = {k: -v for k, v in strfwd_score_map.items()}
    tmp_df = pd.DataFrame()
    for trait, answers in traits_ans.items():
        for ans in answers:
            if ans_map[ans] == "strfwd":
                tmp_df[ans] = data[ans].map(strfwd_score_map)
            elif ans_map[ans] == "reversed":
                tmp_df[ans] = data[ans].map(rvs_ans_map)
        data[f"{trait}_score"] = 50
        for ans in answers:
            data[f"{trait}_score"] += tmp_df[ans]
    return data, metadata


def assign_level(data, metadata):
    """
    Assign level of each trait by its score.
    Example:
    Extraversion_score in [90, 100] -> E_ext_high
    Extraversion_score in [70, 90] -> E_high
    Extraversion_score in [60, 70] -> E_moderate
    Extraversion_score in [40, 60] -> neutral
    Extraversion_score in [30, 40] -> I_moderate
    Extraversion_score in [10, 30] -> I_high
    Extraversion_score in [0, 10] -> I_extreme
    """
    for column in data.columns:
        if "score" in column:
            first_letter = column[0]
            new_col_name = first_letter + "_level"
            data[new_col_name] = data[column].apply(lambda x: level(x))
    return data, metadata


def level(value):
    """
    Return level of trait by its score.
    Note: Not quite proud of this, but it works.
    """
    if 90 < value <= 100:
        return "ext_high"
    elif 70 < value <= 90:
        return "high"
    elif 60 < value <= 70:
        return "higher"
    elif 40 <= value <= 60:
        return "neutral"
    elif 30 <= value < 40:
        return "lower"
    elif 10 <= value < 30:
        return "low"
    elif 0 <= value < 10:
        return "ext_low"


def chain_funcs(data: pd.DataFrame, funcs: List[Callable]) -> pd.DataFrame:
    """
    Apply a list of functions to a dataframe and collects metadata.
    """
    raw_data_len = len(data)
    for i, func in enumerate(funcs):
        if i == 0:
            metadata = ""
        data, metadata = func(data, metadata)
    proc_data_len = len(data)
    drop_all_pct = (raw_data_len - proc_data_len) / raw_data_len * 100
    metadata += f"Dataset lenght after preprocessing: {len(data)} \n"
    metadata += f"Total rows dropped: {drop_all_pct:.2f}% \n" + 80 * "-" + "\n"
    return data, metadata


class PreprocessData(object):
    def __init__(
        self,
        raw_data: pd.DataFrame,
        process_funcs: List[Callable] = [
            init_metadata,
            process_age,
            process_country,
            apply_maps,
            remove_zero_ans,
            calculate_scores,
            assign_level
            ]) -> None:
        """
        Load and process data
        """
        self.data, self.metadata = chain_funcs(data=raw_data, funcs=process_funcs)

    def get_data(self) -> pd.DataFrame:
        """
        Return processed data
        """
        return self.data
    
    def get_metadata(self) -> str:
        """
        Return metadata gathered during the preprocessing
        """
        return self.metadata
