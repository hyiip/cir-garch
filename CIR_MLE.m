function status =  CIR_MLE(SD,MA,offset,itemName, itemType, epsilon)
    cHeader = {'Date' 'cir_kappa' 'cir_theta' 'cir_sigma' 'cir_leakage' 'cir_kappa_sd' 'cir_theta_sd' 'cir_sigma_sd' 'cir_kappa_z' 'cir_theta_z' 'cir_sigma_z' };
    textHeader = strjoin(cHeader, ',');
    delimiterIn = ','; %use , as delimiter, some might use an ' ', depends on how to write your csv
    headerlinesIn = 1; %assuming first row is header

    lb = [1e-5 1e-5 1e-5] ; 
    ub = [100.0 10.0 10.0];        

    TimeStep = 1;                       
    bd = 1e-6;
    prefixString = sprintf("%s/updating/tor%s/", itemType,epsilon);
    locString = sprintf("%stoanalysis/SD%d/day%d/",prefixString, SD*100, MA);
    rawName = sprintf("bounded_tor%s_day%d_SD%d_%s.csv", epsilon,MA,SD*100,itemName);
    filename = sprintf("%s%s",locString,rawName);
    rollPath = sprintf("%stemp/new/SD%d/day%d/roll/",prefixString,SD*100, MA);
    expandPath = sprintf("%stemp/new/SD%d/day%d/expand/",prefixString,SD*100, MA);
    if ~exist(char(rollPath),'dir') mkdir(char(rollPath)); end
    if ~exist(char(expandPath),'dir') mkdir(char(expandPath)); end
    resultname_roll = sprintf("%scir_roll_%s",rollPath,rawName);
    resultname_expand = sprintf("%scir_expand_%s",expandPath,rawName);
    raw = importdata(filename,delimiterIn,headerlinesIn); %import csv
    m = size(raw.data,1);
    Data = raw.data;


    day = 750;
    count = 0 ;
    ssave = zeros(m-day+1,10);

    if offset <= -1
        startDay = 1;
    else
        startDay = m-day+1-offset;
    end;

    for i = startDay : m-day+1
        %Datatemp = Data(1:day+i-1);
        Datatemp = Data(i:day+i-1); 


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
            continue;
        end
        if isreal(guess) ~= 1
            continue
        end
        if i > 2246
            
        end
        xo= mle(Datatemp,'nloglf', @myfun_O,'start', guess,'lowerbound',lb);

        while (abs(guess-xo)>bd)
            count = count + 1 ;
            guess = xo;
            xo= mle(Datatemp,'nloglf', @myfun_O,'start', guess,'lowerbound',lb);
        end
        leakage = xo(3)*xo(3)/(4*xo(1)*xo(2));
        acov = mlecov(xo, Datatemp, 'nloglf', @myfun_O);
        stderr = transpose(sqrt(diag(acov)));
        ssave(i, : ) = [real(xo) real(leakage) real(stderr) real(xo./stderr)];
        fprintf("rolling, file = %s. iter =  %d / %d\n\n",filename,i,m-day+1);
    end ;
    textData = transpose(raw.textdata(day+1:m+1));
    ssave = ssave( [startDay:end] , : );
    textData = textData( [startDay:end] , : );
    output = [textData num2cell(ssave)]';
    fid = fopen(resultname_roll,'w'); 
    fprintf(fid,'%s\n',textHeader);
    fprintf(fid, '%s, %.15f, %.15f,%.15f, %.15f, %.15f, %.15f, %.15f, %.15f, %.15f, %.15f\n', output{:});
    fclose(fid);

%     ssave = zeros(m-day+1,10);
% 
%     for i = startDay : m-day+1
%         Datatemp = Data(1:day+i-1);  
%         %Datatemp = Data(i:day+i-1);  
% 
%         x = Datatemp(1:end-1);
%         dx = diff(Datatemp);
%         delx = dx./x.^0.5;
%         regressors = [TimeStep./x.^0.5, TimeStep*x.^0.5];
%         drift = regressors\delx;
%         res = regressors*drift - delx;
%         kappai = -drift(2);
%         thetai = -drift(1)/drift(2);
%         sigmai = sqrt(var(res, 1)/TimeStep);
% 
%         guess = [kappai thetai sigmai];
% 
%         guess(guess<lb) = lb(guess<lb) + bd;
%         guess(guess>ub) = ub(guess>ub) - bd;
% 
%         if isnan(guess) == 1
%             continue;
%         end
%         xo= mle(Datatemp,'nloglf', @myfun_O,'start', guess,'lowerbound',lb);
% 
%         while (abs(guess-xo)>bd)
%             count = count + 1 ;
%             guess = xo;
%             xo= mle(Datatemp,'nloglf', @myfun_O,'start', guess,'lowerbound',lb);
%         end;
%         leakage = xo(3)*xo(3)/(4*xo(1)*xo(2));
%         acov = mlecov(xo, Datatemp, 'nloglf', @myfun_O);
%         stderr = transpose(sqrt(diag(acov)));
%         ssave(i, : ) = [real(xo) real(leakage) real(stderr) real(xo./stderr)];
%         fprintf("expanding, file = %s. iter =  %d / %d \n\n",filename,i,m-day+1);
%     end ;
% 
%     textData = transpose(raw.textdata(day+1:m+1));  
%     ssave = ssave( [startDay:end] , : );
%     textData = textData( [startDay:end] , : );
%     output = [textData num2cell(ssave)]';
%     fid = fopen(resultname_expand,'w'); 
%     fprintf(fid,'%s\n',textHeader);
%     fprintf(fid, '%s, %.15f, %.15f,%.15f, %.15f, %.15f, %.15f, %.15f, %.15f, %.15f, %.15f\n', output{:});
%     fclose(fid);
    status = 1;
    return
end