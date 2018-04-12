#### THIS IS UNDER CONSTRUCTION. NOT READY FOR IMPLEMENTATION OR TESTING

class Results_wrap(object):
    def __init__(self, model, coefficients, VarCovMatrix, cov_type='nonrobust'):
        self.model = model
        self.coefficients = coefficients
        self.VarCovMatrix = VarCovMatrix

    def summary(self, title=None):
        if title is None:
            title = self.model + ' ' + "Regression Results"
        return print(title)




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

    The 2SLS estimator is a special case of a k-class estimator with
    :math:`\kappa=1`,

    This class uses the statsmodels/linearmodels documentation and structure.
    Specifically from the IV2SLS function.
    '''

    def __init__(self, dependent, exog, endog, instruments, exog2=None, instruments2=None):
        self.dependent = dependent
        self.exog = exog
        self.endog = endog
        self.instruments = instruments
        self.exog2 = exog2
        self.instruments2 = instruments2



    def fit(self):
        y, X, X2, endog, Z, Z2 = self.dependent, self.exog, self.exog2, self.endog, self.instruments, self.instruments2
        
        return Results_wrap(model = 'testmodel', coefficients = y, VarCovMatrix = X)

        


