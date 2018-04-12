'''Generalized Method of Moments, GMM, and Two-Stage Least Squares for
instrumental variables IV2SLS



Issues
------
* number of parameters, nparams, and starting values for parameters
  Where to put them? start was initially taken from global scope (bug)
* When optimal weighting matrix cannot be calculated numerically
  In DistQuantilesGMM, we only have one row of moment conditions, not a
  moment condition for each observation, calculation for cov of moments
  breaks down. iter=1 works (weights is identity matrix)
  -> need method to do one iteration with an identity matrix or an
     analytical weighting matrix given as parameter.
  -> add result statistics for this case, e.g. cov_params, I have it in the
     standalone function (and in calc_covparams which is a copy of it),
     but not tested yet.
  DONE `fitonce` in DistQuantilesGMM, params are the same as in direct call to fitgmm
      move it to GMM class (once it's clearer for which cases I need this.)
* GMM doesn't know anything about the underlying model, e.g. y = X beta + u or panel
  data model. It would be good if we can reuse methods from regressions, e.g.
  predict, fitted values, calculating the error term, and some result statistics.
  What's the best way to do this, multiple inheritance, outsourcing the functions,
  mixins or delegation (a model creates a GMM instance just for estimation).


Unclear
-------
* dof in Hausman
  - based on rank
  - differs between IV2SLS method and function used with GMM or (IV2SLS)
  - with GMM, covariance matrix difference has negative eigenvalues in iv example, ???
* jtest/jval
  - I'm not sure about the normalization (multiply or divide by nobs) in jtest.
    need a test case. Scaling of jval is irrelevant for estimation.
    jval in jtest looks to large in example, but I have no idea about the size
* bse for fitonce look too large (no time for checking now)
    formula for calc_cov_params for the case without optimal weighting matrix
    is wrong. I don't have an estimate for omega in that case. And I'm confusing
    between weights and omega, which are *not* the same in this case.



Author: josef-pktd
License: BSD (3-clause)

'''


from __future__ import print_function
from statsmodels.compat.python import lrange
from statsmodels.compat.numpy import np_matrix_rank

import numpy as np
from scipy import optimize, stats

from statsmodels.tools.numdiff import approx_fprime, approx_hess
from statsmodels.base.model import (Model,
                                    LikelihoodModel, LikelihoodModelResults)
from statsmodels.regression.linear_model import (OLS, RegressionResults,
                                                 RegressionResultsWrapper)
import statsmodels.stats.sandwich_covariance as smcov
from statsmodels.tools.decorators import (resettable_cache, cache_readonly)
from statsmodels.tools.tools import _ensure_2d

DEBUG = 0

def maxabs(x):
    '''just a shortcut to np.abs(x).max()
    '''
    return np.abs(x).max()

class Quadratic2SLS(LikelihoodModel):
    r"""
    Estimation of IV models using two-stage least squares
    in the case where the right hand side endogenous variable
    is quadratic. We use the estimation scheme proposed in 
    Wooldgridge p.236-237.

    Parameters
    ----------
    dependent : array-like
        Endogenous variables (nobs by 1)
    exog : array-like
        Exogenous regressors  (nobs by nexog)
    exog2 : array-like
        Exogenous regressors for part B of first stage (if different)  (nobs by nexog2)
    endog : array-like
        Endogenous regressors (nobs by 1)
    instruments : array-like
        Instrumental variables (nobs by ninstr)
    instruments2 : array-like
        Instrumental variables for part B of first stage (if different) (nobs by ninstr2)
    weights : array-like, optional
        Observation weights used in estimation

    Notes
    -----
    The 2SLS estimator is defined

    .. math::

      \hat{\beta}_{2SLS} & =(X'Z(Z'Z)^{-1}Z'X)^{-1}X'Z(Z'Z)^{-1}Z'Y\\
                         & =(\hat{X}'\hat{X})^{-1}\hat{X}'Y\\
                 \hat{X} & =Z(Z'Z)^{-1}Z'X

    The 2SLS estimator is a special case of a k-class estimator with
    :math:`\kappa=1`,

    This class uses the statsmodels/linearmodels documentation and structure.
    Specifically from the IV2SLS function.
    """
    
    def __init__(self, exog, endog, instruments=None, dependent=None, exog2=None, instruments2=None):
        self._method = 'Quadratic 2SLS'
        self.dependent = dependent
        self.instrument = instruments
        self.exog2 = exog2
        self.instruments2 = instruments2
        super(Quadratic2SLS, self).__init__(exog, endog)


        def fit(self, cov_type=None):
            '''
            Estimate model using 2SLS IV regression with quadratic RHS
            endogenous variables as described in Wooldridge.

            Parameters
            ----------
            cov_type : string
                If "HCR" computes heteroskedasticity robust covariance

            Returns
            -------
            results : similar to instance of RegressionResults
            regression result

            Notes
            -----
            This returns a custom output which is a less complete version of 
            the RegressionResults output in statsmodels.

            '''

            y, X, X2, endog, Z, Z2 = self.dependent, self.exog, self.exog2, self.endog, self.instruments, self.instruments2

            ### First Stage ###
            # Part A: Estimating endogenous var
            return print('testing')

            # Part B: Estimating (endogenous var)^2



            ### Second Stage ###



            ### Heteroskedasticity Robust Covariance Matrix ###



            ### Covariance Matrix under Homoskedasticity Assumption ###
            if cov_type == None:
                self.cov_type = 'nonrobust'
                self.cov_kwds = {'description' : 'Standard Errors assume that the ' +
                                'covariance matrix of the errors is correctly ' +
                                'specified. (Homoskedasticity assumed)'}

            
            ### Regression Features ###
            
            def nobs(self):
                return float(self.exog.shape[0])


            ### Summary Output Table ###
            def summary(self, title=None):
                '''
                MAKES SUMMARY TABLE
                '''

                if title is None:
                    title = self._method + ' ' + "Regression Results"
                return print(title)