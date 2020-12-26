function [ssaveRow,count] =  setSsave(Datatemp,count,TimeStep,lb,ub,bd)
    %Datatemp = Data(i:day+i-1); 
    ssaveRow = NaN(1,10);
    x = Datatemp(1:end-1);
    dx = diff(Datatemp);
    delx = dx./x.^0.5;
    regressors = [TimeStep./x.^0.5, TimeStep*x.^0.5];
    drift = regressors\delx;
    res = regressors*drift - delx;
    kappai = -drift(2);
    thetai = -drift(1)/drift(2);
    sigmai = sqrt(var(res, 1)/TimeStep);

    guess = [kappai thetai sigmai];

    guess(guess<lb) = lb(guess<lb) + bd;
    guess(guess>ub) = ub(guess>ub) - bd;
    if isnan(guess) == 1
        return;
    end
    if isreal(guess) ~= 1
        return
    end
    try
        xo= mle(Datatemp,'nloglf', @myfun_O,'start', guess,'lowerbound',lb);
        while (abs(guess-xo)>bd)
            count = count + 1 ;
            guess = xo;
            xo= mle(Datatemp,'nloglf', @myfun_O,'start', guess,'lowerbound',lb);
        end
    catch
        fprintf("Error occur: The NLOGLF function returned a NaN or infinite log-likelihood value.\n\n");
        return
    end
    leakage = xo(3)*xo(3)/(4*xo(1)*xo(2));
    acov = mlecov(xo, Datatemp, 'nloglf', @myfun_O);
    stderr = transpose(sqrt(diag(acov)));
    ssaveRow = [real(xo) real(leakage) real(stderr) real(xo./stderr)];
    return;
end