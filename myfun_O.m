function lnL = myfun(Params,Data,cens,freq)
   
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
    z = 2*sqrt(u.*v);
    bf = besseli(q,z,1);
 
    lnL = -(Nobs-1)*log(c) + sum(u + v - 0.5*q*log(v./u) - log(bf)-z);
end