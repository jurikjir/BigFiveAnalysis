# Big Five prediction

Navigate to repository folder and install dependencies with:

## Install and run

```
pip install -r requirements.txt        
```

Code is can be runned with command:

```
python main.py    
```

Infromation about data preprocessing, model fit and data plotting will be
displayed in terminal.

## Code structure

1. main.py
The main() function in main.py file is the entry point of the program. It takes care about
data preprocessing, plotting and model fitting.

2. preprocess.py
Contains module which chains preprocessing functions and collect preprocessing data, which are
then used in report. It is possible to add new functions if it is preserved convention
that function takes and returns varables: data and metadata

3. dataloader.py
Function which loads data from csv and converts to pandas dataframe

4. ranges.py
Contains mapping functions to generate values str representations of value ranges in dataset

5. maps.py
Conversion dicts to map values to srt representations in dataset -> needed in plotting

6. plot.py
Plotter module which plots data in uniform format, handy for fast data exploration