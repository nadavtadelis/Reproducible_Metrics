# Reproducibility and Applied Econometrics - The Effect of Studying on Grades

[![Build Status](https://travis-ci.org/nadavtadelis/Reproducible_Metrics.svg?branch=master)](https://travis-ci.org/nadavtadelis/Reproducible_Metrics) [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/nadavtadelis/Reproducible_Metrics/master) [![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](http://www.repostatus.org/badges/latest/wip.svg)](http://www.repostatus.org/#wip)

This is a work in progress attempting to provide a framework for a responsibly researched and reproducible econometric paper.

This repository holds all the material for "Reproducibility and Applied Econometrics - The Effect of Studying on Grades
". The main paper is [reproducible_metrics.pdf](https://github.com/nadavtadelis/Reproducible_Metrics/blob/master/reproducible_metrics.pdf) and all additional analaysis and intermediate steps can be found in the Jupyter Notebooks.

## Notebook Descriptions

* [`data_exploration.ipynb`](https://github.com/nadavtadelis/Reproducible_Metrics/blob/master/data_exploration.ipynb) - Numerical and visual representations of the data. Mapping studytime variable.
* [`model_fitting_1.ipynb`](https://github.com/nadavtadelis/Reproducible_Metrics/blob/master/model_fitting_1.ipynb) - Naive OLS model fitting. Multicollinearity exploration (VIF, LASSO).
* [`model_fitting_2.ipynb`](https://github.com/nadavtadelis/Reproducible_Metrics/blob/master/model_fitting_2.ipynb) - Q2SLS model fitting.
* [`function_testing.ipynb`](https://github.com/nadavtadelis/Reproducible_Metrics/blob/master/function_testing.ipynb) - Testing Q2SLS script and exploring asymptotic properties of Q2SLS procedure.

## Required Installations

The only installation needed to run this repo is Anaconda. Click [here](https://conda.io/docs/user-guide/install/index.html#regular-installation) to learn about how to install Anaconda. Once installed, you should be good to go!

## Using Binder

We've enabled Binder for this project which allows you to view and edit jupyter notebooks in an executable environment. Feel free to click the badge at the top of this README to launch the binder.

## Getting Started

Download the repo onto your local machine and open your command prompt to the Reproducible_Metrics directory. Simply type in the following commands to run the analysis:

```
make clean
make env
source activate study_env
make run
```

After all your notebooks have run you should see new files in the results, fig, and data directories. Read about our approach and results in main.ipynb. All the figures from our analysis are saved in the fig directory and our regressions are saved in the results directory as dataframes. You can load in these dataframes and work with them as regression instances (i.e. you can call `.summary()`, `.params()` etc. click [here](http://www.statsmodels.org/dev/generated/statsmodels.regression.linear_model.OLS.html) for OLS documentation)

## Licensing

In an effort to enable reproducible, collaborative reserach this project is subject to the MIT License which allows you to modify and distribute the above code for both private and commercial usage. See LICENSE to learn more.