#### THIS IS UNDER CONSTRUCTION. NOT READY FOR IMPLEMENTATION OR TESTING

# Think more about whether we should actually keep `exog2` in... if an exogenous
# variable is included in either part of the first stage, then i think it should 
# be included in the second stage... The question is whether one might want to 
# include exogenous vars in the second part of the first stage that aren't included 
# in the first part, but will be included in the second stage. Could also include 
# those to possibilites as a True/False parameter.

# I think we may be able to use `IVRegressionResults` and `RegressionResultsWrapper`
# to output a nice summary table. We can specify the coeff. estimates and the standard errors,
# but im not sure if the other features will be correct. Need to check this.
# See `IV2SLS` summary function for an example of implementation.

import statsmodels.api as sm
import pandas as pd

class Quadratic2SLS(object):
    r'''   
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

    '''

    def __init__(self, dependent, exog, endog, instruments, exog2=None, instruments2=None):
        self.dependent = dependent
        self.exog = exog
        self.endog = endog
        self.instruments = instruments
        self.exog2 = exog2
        self.instruments2 = instruments2



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
        self.model1A = sm.OLS(endog, pd.concat([X, Z], axis=1))
        self.result1A = self.model1A.fit()
        endog_hat = self.result1A.fittedvalues

        # Part B: Estimating (endogenous var)^2
        if X2 == None: X2 = X
        if Z2 == None: Z2 = Z
        self.model1B = sm.OLS(endog**2, pd.concat([endog_hat**2, X2, Z2], axis=1))
        self.result1B = self.model1B.fit()
        endog_sq_hat = self.result1B.fittedvalues

        ### Second Stage ###
        self.model2 = sm.OLS(y, pd.concat([endog_hat, endog_sq_hat, X, Z], axis=1))
        self.result2 = self.model2.fit()

        ### Bootstrapped Covariance Matrix ###
            # ~~~~ NOTE: I might need to resort to using bootstrapping to estimate the
            #            Standard Errors of the coefficient estimates.
            #            If this is the case, need to decide if the final coefficients reported
            #            are the average estimates from the bootstrapping, or the coefficients
            #            returned by the full sample. I think standard practice is to return
            #            the average, but in this case it seems more reasonable to report the 
            #            coefficients from full sample... actually, they should definitely be the
            #            same if `n_iter` is large enough.
            #            If bootstrapping, I also should include a parameter in the `fit()`
            #            function `n_iter` for the number of bootstrap iterations.
            #            
            #  Question: Do we just collect the coefficient estimates from each iteration and 
            #            then find the SE of that coefficient?
            #            Or do we estimate the covariance matrix Sigma_hat in each iteration
            #            and then average across those matrices?
        start here

        ### Heteroskedasticity Robust Covariance Matrix ###
        if cov_type == 'HCR':
            self.cov_type = 'HCR'
            self.cov_kwds = {'description' : 'Standard Errors are robust ' +
                             'to heteroskedasticity.'}
            print('testing_in_robust')


        ### Covariance Matrix under Homoskedasticity Assumption ###
        if cov_type == None:
            self.cov_type = 'nonrobust'
            self.cov_kwds = {'description' : 'Standard Errors assume that the ' +
                             'covariance matrix of the errors is correctly ' +
                             'specified. (Homoskedasticity assumed)'}

        
        ### Regression Features ###
        self.nobs = float(self.exog.shape[0])

        # TESTING #
        return Results_wrap(model = 'testmodel', 
        coefficients = y, 
        VarCovMatrix = X, 
        cov_type = self.cov_type)

        


class Results_wrap(object):
    '''
    Summarize the Regression Results (based of statsmodels)

    Parameters
    -----------
    yname : string, optional
        Default is `y`
    xname : list of strings, optional
        Default is `var_##` for ## in p the number of regressors
    title : string, optional
        Title for the top table. If not None, then this replaces the
        default title
    alpha : float
        significance level for the confidence intervals

    Returns
    -------
    smry : Summary instance
        this holds the summary tables and text, which can be printed or
        converted to various output formats.
    '''
    def __init__(self, model, coefficients, VarCovMatrix, cov_type='nonrobust'):
        self.model = model
        self.coefficients = coefficients
        self.VarCovMatrix = VarCovMatrix

    def summary(self, title=None):
        if title is None:
            title = self.model + ' ' + "Regression Results"
        return print(title)

