import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Callable, Tuple
import os


class PlotData(object):
    def __init__(self, imgdir_path: str = ".") -> None:
        """
        Module which plots given data and save them if user wants to
        """
        self.plot_storage = os.path.join(imgdir_path, "img")
        if not os.path.exists(self.plot_storage):
            os.makedirs(self.plot_storage)

    def plot(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        plot: Callable,
        rotation: int = 0,
        figsize: Tuple[int]=(8, 6),
        autosave: bool = False,
        **kwargs) -> None:
        """
        Function which takes data, x, y columns and sns or plt function and plot
        them in united setting. User is asked if he wants to save the plot after
        plotting.
        """
        plt.figure(figsize=figsize)
        ax = plot(data[x], data[y], **kwargs)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=rotation)
        plot_name = str(plot).split(" ")[1]
        if "str" in x: x = x.split("_")[0]
        if "str" in y: y = y.split("_")[0]
        plt.title(label=f"{x} vs {y} - {plot_name}", fontweight="bold")
        plt.xlabel(xlabel=x, fontweight="bold")
        plt.ylabel(ylabel=y, fontweight="bold")
        #plt.legend()
        save_path = os.path.join(self.plot_storage, f"{x}_{y}_{plot_name}.png")
        plt.savefig(save_path)
        if autosave == False:
            plt.show()
            save_img = input("Do you want to save this plot? (y/n)")
            # This has to be this way, because if plot is saved after plt.show()
            # plain image is saved. plt.show() clears canvas after call
            if save_img.lower() in ["n", "no", "nope"]:
                os.remove(path=save_path)
        elif autosave == True:
            print(f"Plot saved as {save_path}")