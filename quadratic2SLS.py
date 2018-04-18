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
import numpy as np
from tqdm import tqdm

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



    def fit(self, cov_type=None, n_iter=None):
        '''
        Estimate model using 2SLS IV regression with quadratic RHS
        endogenous variables as described in Wooldridge.

        Parameters
        ----------
        cov_type : string
            If "Bootstrap" uses bootstrapping with n_iter to estimate errors
            If "HCR" computes heteroskedasticity robust covariance
        n_iter : int
            Number of iterations for bootstrapping

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
        self.nobs = int(self.exog.shape[0])
        K = int(self.exog.shape[1] + 2)
        
        ### First Stage ###
        # Part A: Estimating endogenous var
        model1A = sm.OLS(endog, pd.concat([X, Z], axis=1))
        result1A = model1A.fit()
        endog_hat = result1A.fittedvalues

        # Part B: Estimating (endogenous var)^2
        if self.exog2 is None: X2 = X
        if self.instruments2 is None: Z2 = Z
        model1B = sm.OLS(endog**2, pd.concat([endog_hat**2, X2, Z2], axis=1))
        result1B = model1B.fit()
        endog_sq_hat = result1B.fittedvalues

        ### Second Stage ###
        inter_df = pd.DataFrame({'endog_hat' : endog_hat, 'endog_sq_hat' : endog_sq_hat})
        X_hat_full = pd.concat([X['const'], inter_df, X.ix[:, X.columns != 'const']], axis = 1)
        model2 = sm.OLS(y, X_hat_full)
        result2 = model2.fit()

        ### Bootstrapped Covariance Matrix ###
            # ~~~~ NOTE: I might need to resort to using bootstrapping to estimate the
            #            Standard Errors of the coefficient estimates.
            #            If this is the case, need to decide if the final coefficients reported
            #            are the average estimates from the bootstrapping, or the coefficients
            #            returned by the full sample. I think standard practice is to return
            #            the average, but in this case it seems more reasonable to report the 
            #            coefficients from full sample... actually, they should be the
            #            same if `n_iter` is large enough.
            #            
            #  Question: Do we just collect the coefficient estimates from each iteration and 
            #            then find the SE of that coefficient?
            #            Or do we estimate the covariance matrix Sigma_hat in each iteration
            #            and then average across those matrices?
        if cov_type == 'Bootstrap':
            self.cov_type = 'Bootstrap'
            self.cov_kwds = {'description' : 'Standard Errors are bootstrapped ' +
                             'ADD STUFF HERE.'}
            self.n_iter = n_iter

            # Bootstrapping
            beta_hat_boots = np.zeros((n_iter, K))
            for b_iter in tqdm(range(0, n_iter)):
                b_index = np.random.choice(range(0, self.nobs), self.nobs, replace = True)
                y, X, endog, Z = self.dependent.iloc[b_index], self.exog.iloc[b_index], self.endog.iloc[b_index], self.instruments.iloc[b_index]
                if self.exog2 is not None: 
                    X2 = self.exog2.iloc[b_index]
                if self.instruments2 is not None: 
                    Z2 = self.instruments2.iloc[b_index]

                ## First Stage ##
                # Part A: Estimating endogenous var
                b_model1A = sm.OLS(endog, pd.concat([X, Z], axis=1))
                b_result1A = b_model1A.fit()
                b_endog_hat = b_result1A.fittedvalues

                # Part B: Estimating (endogenous var)^2
                if self.exog2 is None: X2 = X
                if self.instruments2 is None: Z2 = Z
                b_model1B = sm.OLS(endog**2, pd.concat([b_endog_hat**2, X2, Z2], axis=1))
                b_result1B = b_model1B.fit()
                b_endog_sq_hat = b_result1B.fittedvalues

                ## Second Stage ##
                inter_df = pd.DataFrame({'endog_hat' : b_endog_hat, 'endog_sq_hat' : b_endog_sq_hat})
                X_hat = pd.concat([X['const'], inter_df, X.ix[:, X.columns != 'const']], axis = 1)
                b_model2 = sm.OLS(y, X_hat)
                b_result2 = b_model2.fit()

                # Saving coefficient estimates from second stage
                beta_hat_boots[b_iter] = b_result2.params
            
            beta_hat_boots = pd.DataFrame(beta_hat_boots)
            beta_hat_boots.index.name = 'boot_iter'
            beta_hat_boots.columns = X_hat.columns.values.tolist()

            # ~~~~~~ TESTING ~~~~~~
            return Results_wrap(model = 'Q2SLS_bootstrap', 
                                coefficients = np.zeros(K), 
                                VarCovMatrix = 0 * X,
                                model1A = model1A,
                                result1A = result1A,
                                model1B = model1B,
                                result1B = result1B,
                                X_hat = X_hat_full,
                                model2 = model2,
                                result2 = result2, 
                                cov_type = self.cov_type,
                                bootstrap_coeffs = beta_hat_boots)




        ### Heteroskedasticity Robust Covariance Matrix ###
        if cov_type == 'HCR':
            self.cov_type = 'HCR'
            self.cov_kwds = {'description' : 'Standard Errors are robust ' +
                             'to heteroskedasticity.'}
            
            # ~~~~~~ TESTING ~~~~~~
            print('testing_in_robust')
            return Results_wrap(model = 'Q2SLS', 
                                coefficients = np.zeros(K), 
                                VarCovMatrix = 0 * X,
                                model1A = model1A,
                                result1A = result1A,
                                model1B = model1B,
                                result1B = result1B,
                                X_hat = X_hat_full,
                                model2 = model2,
                                result2 = result2, 
                                cov_type = self.cov_type)


        ### Covariance Matrix under Homoskedasticity Assumption ###
        if cov_type == None:
            self.cov_type = 'nonrobust'
            self.cov_kwds = {'description' : 'Standard Errors assume that the ' +
                             'covariance matrix of the errors is correctly ' +
                             'specified. (Homoskedasticity assumed)'}
            
            # ~~~~~~ TESTING ~~~~~~
            return Results_wrap(model = 'Q2SLS', 
                                coefficients = np.zeros(K), 
                                VarCovMatrix = 0 * X,
                                model1A = model1A,
                                result1A = result1A,
                                model1B = model1B,
                                result1B = result1B,
                                X_hat = X_hat_full,
                                model2 = model2,
                                result2 = result2, 
                                cov_type = self.cov_type)

        
        ### Regression Features ###
        

        

        


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
    def __init__(self, model, coefficients, VarCovMatrix, model1A, result1A, model1B, result1B, X_hat, model2, result2, cov_type='nonrobust', bootstrap_coeffs=None):
        self.model = model
        self.coefficients = coefficients
        self.VarCovMatrix = VarCovMatrix
        self.model1A = model1A
        self.result1A = result1A
        self.model1B = model1B
        self.result1B = result1B
        self.X_hat = X_hat
        self.model2 = model2
        self.result2 = result2
        self.cov_type = cov_type
        self.beta_hat_boots = bootstrap_coeffs

    def summary(self, title=None):
        if title is None:
            title = self.model + ' ' + "Regression Results"
        return print(title)

