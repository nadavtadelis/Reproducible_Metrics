#### THIS IS UNDER CONSTRUCTION. NOT READY FOR IMPLEMENTATION OR TESTING

from linearmodels.iv import IV2SLS
IV2SL



class Quadratic2SLS(IVLIML):
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
    
    def __init__(self, dependent, exog, exog2=None, endog, instruments, instruments2=None):
        self._method = 'Quad-2SLS'
        super(Quadratic2SLS, self).__init__(dependent, exog, exog2=exog2, endog, instruments, instruments2=instruments2)


    def fit(self):
        '''
        Estimate model using 2SLS IV regression with quadratic RHS
        endogenous variables as described in Wooldridge.

        Returns
        -------
        results : similar to instance of RegressionResults
           regression result

        Notes
        -----
        This returns a custom output which is a less complete version of 
        the RegressionResults output in statsmodels.

        '''

        # COMPUTATION GOES HERE

        
        def summary(self, title=None):
            '''
            MAKES SUMMARY TABLE
            '''




