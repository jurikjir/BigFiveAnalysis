import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Callable, Tuple
import os
from tqdm import tqdm

from data_loader import load_data
from preprocess import PreprocessData


class PlotData(object):
    def __init__(self, imgdir_path: str = ".") -> None:
        """
        Module which plots given data and save them if user wants to
        """
        self.plot_storage = os.path.join(imgdir_path, "img")
        if not os.path.exists(self.plot_storage):
            os.makedirs(self.plot_storage)
        self.plot_paths = []

    def plot(
        self,
        data: pd.DataFrame,
        plot: Callable,
        x: str,
        y: str = None,
        rotation: int = 0,
        figsize: Tuple[int]=(8, 6),
        autosave: bool = False,
        grid: bool = False,
        **kwargs) -> None:
        """
        Function which takes data, x, y columns and sns or plt function and plot
        them in united setting. User is asked if he wants to save the plot after
        plotting.
        """
        plt.figure(figsize=figsize)
        
        ax = plot(data[x], data[y], **kwargs) if y is not None else plot(data[x], **kwargs)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=rotation)
        plot_name = str(plot).split(" ")[1]
        if "str" in x: x = x.split("_")[0]
        plt.xlabel(xlabel=x, fontweight="bold")
        if y is not None:
            if "str" in y: y = y.split("_")[0]
            plt.ylabel(ylabel=y, fontweight="bold")
            plt.title(label=f"{x} vs {y} - {plot_name}", fontweight="bold")
        else:
            plt.title(label=f"{x} - {plot_name}", fontweight="bold")
        if grid:
            plt.grid()
        save_path = os.path.join(self.plot_storage, f"{x}_{y}_{plot_name}.png")
        self.plot_paths.append(save_path)
        plt.savefig(save_path)
        if autosave == False:
            plt.show()
            save_img = input("Do you want to save this plot? (y/n)")
            # This has to be this way, because if plot is saved after plt.show()
            # plain image is saved. plt.show() clears canvas after call
            if save_img.lower() in ["n", "no", "nope"]:
                os.remove(path=save_path)
        elif autosave == True:
            pass

    @property
    def get_plot_paths(self) -> list:
        """
        Function which returns list of paths to saved plots
        """
        return self.plot_paths


def plot_data(processed_data: pd.DataFrame) -> None:
    """
    Plots data and saves them into img folder
    """
    levels = ['E_level', 'N_level', 'A_level', 'C_level', 'O_level']
    trait_order = ["ext_low", "low", "lower", "neutral", "higher", "high", "ext_high"]
    age_order = ["14-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80", "80-90", "90-100"]
    plots = [sns.barplot, sns.boxplot, sns.violinplot]
    plotter = PlotData(imgdir_path="results")

    for plot in tqdm(plots):
        for level in levels:
            plotter.plot(
                data=processed_data,
                x=level,
                y="performance",
                plot=plot,
                order=trait_order,
                autosave=True)

        plotter.plot(
            data=processed_data,
            x="age_range",
            y="performance",
            plot=plot,
            order=age_order,
            autosave=True)

    for plot_path in plotter.get_plot_paths:
        print(f"Plot saved to {plot_path}")
