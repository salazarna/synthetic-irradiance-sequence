# One-day Synthetic Solar Irradiance Sequences

## Introduction

This software uses an `stochastic` and `bootstrap` method to generate one-day synthetic solar irradiance data at a minimum 60-minute time resolution.

The software required to define eight parameters to execute:

1. `DF`: Input dataset that contains the measured solar irradiance. Must be a `pd.Dataframe`.
2. `COL`: Column of the pd.DataFrame of the solar irradiance (input data).
3. `YEAR`: Year of study. Must exist in the input dataset.
4. `MONTH`: Month of study (1 to 12). Must exist in the input dataset.
5. `SC`: Sky condition of study. Must be 'sc1', 'sc2', 'sc3', 'sc4' or 'sc5'. Corresponds to fully covered, mostly covered, partially covered, mostly clear and totally clear, respectively.
6. `METHOD`: Method to generate the synthetic data. Must be 'stochastic' or 'bootstrap'.
7. `IC`: Confidence interval. Must be a value between 0 and 1. The suggested value is 0.95.
8. `RUNS`: Quantity of one-day synthetic sequences to generate.

The output of the software is a one-day synthetic solar irradiance time series with the same time resolution of the input dataset. It will be generated as many sequences as defined in the `RUNS` parameter.

## Overview of the repository structure

```
.
|-- src                  -- source codes
|-- validations
|   |-- data             -- input datasets
|   |-- distributions    -- goodness of fit assessment
|   |-- metrics
|       |-- energy       -- energy production validation
|       |-- statistical  -- goodness of fit validation
|       |-- variability  -- dynamic behavior validation
|   |-- notebooks        -- validations for each input dataset
|-- environment.yml      -- python environment creation
|-- notebook.ipynb       -- jupyter notebook for execution
|-- requirements.txt     -- dependencies
`-- setup.py             -- python library configuration
```

## Instalation

A specific python environment called `synthetic` will be created to run the methods and the necessary packages will be installed. For this, open the terminal and from the `(base)` environment move to the directory where you have downloaded the folder of this repository. For instance, if you have downloaded the folder to your desktop:

```terminal
cd C:\user\Desktop\synthetic_irradiance
```

Then, create the environment with the command:

```terminal
conda env create --file environment.yml
```

Next, activate the environment:

```terminal
conda activate synthetic
```

After executing the previous command, you must be in the corresponding environment, in this case denoted by `(synthetic)`. Now the respective kernel of the newly created environment is installed with the following command:

```terminal
python -m ipykernel install --user --name synthetic --display-name "synthetic"
```

Finally, run the following command to start the Jupyter Notebooks.

```terminal
jupyter notebook
```

## Uninstall

If you want to delete the `synthetic` environment, run the following command:

```terminal
conda env remove -n synthetic
```

Finally, to remove the created `synthetic` kernel, run the following command:

```terminal
jupyter kernelspec remove synthetic
```

## Basic Usage

In the root folder of the repository, the `notebook.ipynb` file contains the description for the basic usage of the code. This same file is suggested to be used as a template to generate the synthetic data. It is just needed to adaptate the input parameters.

An example of the code pipeline is:

```python
import src
import pvlib
import numpy as np
import pandas as pd
```

First, upload the input dataset.

```python
df = pd.read_csv(filepath_or_buffer=f'./validations/data/bogota-5.csv', sep=',', decimal='.', index_col='timestamp', parse_dates=True)
```

Next, define the input parameters.

```python
DF = df
COL = 'poa_wm2'
YEAR = 2023
MONTH = 1
SC = 'sc5'
METHOD = 'stochastic'
IC = 0.95
RUNS = 5
```

Finally, generate the one-day synthetic solar irradiance time series with the following function:

```python
synthetic = src.methods.sequential(data=DF,
                                   irradiance_column=COL,
                                   year=YEAR,
                                   month=MONTH,
                                   sky_condition=SC,
                                   method=METHOD,
                                   IC=IC,
                                   resolution=RESOLUTION,
                                   runs=RUNS)
```

The function will return a `pd.DataFrame` for each sky condition (i.e., fully covered, mostly covered, partially covered, mostly clear and totally clear) with a number of columns given by the `RUNS` parameters and the timestamps as an index.

<img src="https://github.com/salazarna/synthetic_irradiance/tree/main/figs/fig8a.pdf" align="center" width="500" alt="code results for sc2">
<img src="https://github.com/salazarna/synthetic_irradiance/tree/main/figs/fig8b.pdf" align="center" width="500" alt="code results for sc3">
<img src="https://github.com/salazarna/synthetic_irradiance/tree/main/figs/fig8c.pdf" align="center" width="500" alt="code results for sc4">
<img src="https://github.com/salazarna/synthetic_irradiance/tree/main/figs/fig8d.pdf" align="center" width="500" alt="code results for sc5">

.grades {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
.desktopGrades {
  box-sizing: border-box;
  padding: 10px;
  float: left;
  width: 50%;
  height: 50%;
}
.desktopGrades h1 {
  border: 1px solid #ccc;
}

<div class="grades">
  <div class="desktopGrades desktopGrades1">
    <h1><img src="https://github.com/salazarna/synthetic_irradiance/tree/main/figs/fig8a.pdf" align="center" width="500" alt="code results for sc2"></h1>
  </div>
  <div class="desktopGrades desktopGrades2">
    <h1><img src="https://github.com/salazarna/synthetic_irradiance/tree/main/figs/fig8b.pdf" align="center" width="500" alt="code results for sc3"></h1>
  </div>
  <div class="desktopGrades desktopGrades3">
    <h1><img src="https://github.com/salazarna/synthetic_irradiance/tree/main/figs/fig8c.pdf" align="center" width="500" alt="code results for sc4"></h1>
  </div>
  <div class="desktopGrades desktopGrades4">
    <h1><img src="https://github.com/salazarna/synthetic_irradiance/tree/main/figs/fig8d.pdf" align="center" width="500" alt="code results for sc5"></h1>
  </div>
</div>

## Citation

The original paper describing the methods implemented is:
```
Salazar-Peña, N., Tabares, A., Gonzalez-Mancera, A., 2023. Sequential stochastic and bootstrap methods to generate synthetic solar irradiance time series of high temporal resolution based on historical observations. Solar Energy XXXX, XXXX-XXXX. URL:XXXX, doi:XXXX.
```
The BibTex entry:
```
@article{SalazarPena2023,
title = "Sequential stochastic and bootstrap methods to generate synthetic solar irradiance time series of high temporal resolution based on historical observations",
journal = "Solar Energy",
volume = "XXXX",
pages = "XXXX-XXXX",
year = "2023",
issn = "XXXX-XXXX",
doi = "XXXX",
url = "XXXX",
author = "Nelson Salazar-Peña and Alejandra Tabares and Andrés González-Mancera",
keywords = "synthetic data, solar radiation models, irradiance generation, stochastic modeling, clear-sky index, sky condition",
}
```

## Licence

GNU AFFERO GENERAL PUBLIC LICENSE v3.0, dispuesta en el archivo `LICENSE`.