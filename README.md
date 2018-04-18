# Brief Analysis on the Marginal Effects of Studying 
[![Build Status](https://travis-ci.org/nadavtadelis/Reproducible_Metrics.svg?branch=master)](https://travis-ci.org/nadavtadelis/Reproducible_Metrics) [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/nadavtadelis/Reproducible_Metrics/master) [![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](http://www.repostatus.org/badges/latest/wip.svg)](http://www.repostatus.org/#wip)


This is a working project attempting to provide a framework for a responsible and reproducible econometric paper.

As students, we have often wondered what effect an extra hour of studying will have on our grades. When trying to determine whether staying up an extra hour to study for that final exam is truly worth it, we usually are limited by imperfect information and our own superstitions. In this project, we attempt to estimate the "true" marginal effect of studying on students' grades. We try to model the effects of studying first using OLS and then various instruments and 2 stage least squares. This repository is also meant to serve as an example of what a reproducible econometric analysis would look like.

## Required Installations
The only installation needed to run this repo is Anaconda. Click [here](https://conda.io/docs/user-guide/install/index.html#regular-installation) to learn about how to install Anaconda. Once installed, you should be good to go!
 
## Using Binder
We've enabled Binder for this project which allows you to view and edit jupyter notebooks in an executable environment. Feel free to click the badge at the top of this README to launch the binder.

## Getting Started
Download the repo onto your local machine and open your command prompt. Simply type in the following commands to run the analysis:

```
make clean
make env
source activate study_env
make run
```
After all your notebooks have run you should see new files in the results, fig, and data directories. Read about our approach and results in main.ipynb. All the figures from our analysis are saved in the fig directory and our regressions are saved in the results directory as dataframes. You can load in these dataframes and work with them as regression instances (i.e. you can call `.summary()`, `.params()` etc. click [here](http://www.statsmodels.org/dev/generated/statsmodels.regression.linear_model.OLS.html) for OLS documentation and [here](https://bashtage.github.io/linearmodels/doc/iv/methods.html#linearmodels.iv.model.IV2SLS) for 2SLS documentation)

## Licensing
In an effort to enable reproducible, collaborative reserach our project is subject to the MIT License which allows you to modify and distribute the above code for both private and commercial usage. See LICENSE to learn more.