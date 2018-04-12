#### THIS IS UNDER CONSTRUCTION. NOT READY FOR IMPLEMENTATION OR TESTING

# trying to use the statsmodels/linearmodels set up, but not sure I have
# time to build the whole class set up. might need to just write individual
# functions.
# maybe ask around to see if anyone is already familiar with the structure
# and if they can help organize things.
# Currently, i need to add an equivalent to IVLIML class in linearmodels script.

from linearmodels import IVLIML


class Quadratic2SLSv3(IVLIML):
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
    
    def __init__(self, dependent, exog, endog, instruments, *, exog2=None, instruments2=None):
        self._method = 'Quadratic 2SLS'
        self.exog2 = exog2
        self.instruments2 = instruments2
        super(Quadratic2SLSv3, self).__init__(dependent, exog, endog, instruments, exog2=exog2, instruments2=instruments2)


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