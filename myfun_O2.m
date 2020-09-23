function lnL = myfun_O2(Params,Data,cens,freq)

% =========================================================================
% PURPOSE : Log-likelihood objective function (multiplied by -1) for the
% CIR process using MATLAB ncx2pdf function.
% =========================================================================
% USAGE : Model.TimeStep = Delta t
% Model.Data = Time series of interest rates observations
% Params = Model parameters (alpha, mu, sigma)
% =========================================================================
% RETURNS : lnL = Objective function value
% =========================================================================
    DataF = Data(2:end);
    DataL = Data(1:end-1);
    Nobs = length(Data);
    TimeStep = 1;
    kappa = Params(1);
    theta = Params(2);
    sigma = Params(3);
    
    c = 2*kappa/(sigma^2*(1-exp(-kappa*TimeStep)));
    q = 2*kappa*theta/sigma^2-1;
    u = c*exp(-kappa*TimeStep)*DataL;
    v = c*DataF;
    s = 2*c*DataF;
    nc = 2*u; % noncentrality parameter
    df = 2*q+2; % degrees of freedom
    gpdf = ncx2pdf(s, df, nc);
    ppdf = 2*c*gpdf;
    lnL = sum(-log(ppdf));
    
end