'get relative directory
'usage: SD MA "indexName" offset
'eg 2 30 "DJI" 10
%raw_path =  @runpath
%run_path =  @runpath
cd %run_path
%SD = @str({%0}*100)
%MA = @str({%1})
%indexName = {%2}
%old_path = "all\eviews\SD" + %SD + "\day" + %MA + "\wf1\"
!offset = {%3}

'get list of files
'%listFilenames = @wdir(%run_path)


%wf1name= %old_path + "bounded_day"+%MA+"_SD"+%SD+"_"+%indexName+".wf1"

%csvname = "bounded_day"+%MA+"_SD"+%SD+"_"+%indexName+".csv"

%current_csv = %raw_path + "\updating\toanalysis\SD" + %SD + "\day" + %MA + "\" + %csvname

if !offset <> -1 then
wfopen %wf1name

import(resize) %current_csv

else

wfopen %current_csv

endif
%pagetempname = @pagename

sample nasample if  bounded_x<>NA
pagecopy(smpl=nasample , page="temp")
pageselect temp
pagedelete {%pagetempname}
delete nasample 
pagerename temp {%pagetempname}

'change working directory to the folder
'%run_path = %run_path + "\updating\toanalysis\SD" + %SD + "\day" + %MA + "\"
%run_path = %raw_path + "\updating\"
cd %run_path
%eviewsPath = %run_path + "eviews\SD" + %SD + "\day" + %MA
 if @folderexist(%eviewsPath) = 0 then
shell mkdir %eviewsPath
endif
%run_path = %eviewsPath + "\"
cd %run_path


%filename = @left(%csvname,@instr(%csvname, ".csv")-1 )
%filename = "wf1\" + %filename
%savename = "garch\garch_"+ %csvname
%garchPath = %run_path + "garch"
 if @folderexist(%garchPath) = 0 then
shell mkdir %garchPath
endif

%wf1Path = %run_path + "wf1"
 if @folderexist(%wf1Path) = 0 then
shell mkdir %wf1Path
endif


' get size of workfile
!total = @obsrange

'count if there is y<0
series negx = @sum(bounded_x<0)

smpl @all
equation XAR1.ARCH(COV=HUBER) bounded_x c bounded_x(-1)
xar1.fit(d,e,g) x_f @se x_se @garch x_g
series xvol=@sqrt(X_G)
scalar wholekappa =  1 - xar1.@coef(2)
scalar wholetheta =   xar1.@coef(1) / wholekappa 
series tempx_g =@recode(x_g=NA,0,x_g) 

scalar wholekappa_se = xar1.@stderrs(2)
scalar wholetheta_se = @sqrt((xar1.@stderrs(1)/xar1.@coef(1))^2 + (xar1.@stderrs(2)/xar1.@coef(2))^2) * @abs(wholetheta)

if negx = 0 then
    scalar wholesigma = @mean(@sqrt(@ediv( tempx_g ,bounded_x  )))
    scalar wholesigma_se = @stdev(@sqrt(@ediv( tempx_g ,bounded_x  ))) / @sqrt(@obssmpl)
else 
    scalar wholesigma = -1
    scalar wholesigma_se = -1
endif	
d tempx_g
series x_sqrt = @sqrt(bounded_x)

'initialization
if !offset = -1 then
delete(noerr) xex_f
delete(noerr) xex_se
delete(noerr) xex_g
delete(noerr) xex_c
delete(noerr) xex_a
delete(noerr) xexpand
delete(noerr) xexpand_exp
delete(noerr) xexpand_kappa
delete(noerr) xexpand_theta
delete(noerr) xexpand_siga

delete(noerr) xroll_f
delete(noerr) xroll_se
delete(noerr) xroll_g
delete(noerr) xroll_c
delete(noerr) xroll_a
delete(noerr) xroll
delete(noerr) xroll_exp
delete(noerr) xroll_kappa
delete(noerr) xroll_theta
delete(noerr) xroll_siga
endif

!day=749

if !offset = -1 then
    !startDay = 1
    !sigmastartDay = 1
else
    !startDay = !total-!day-!offset
    !sigmastartDay = !startDay-!day
    
endif
for !cc=!startDay to !total-!day
    smpl @first-1+!cc @first-1+!day+!cc
    equation xroll_exp.ARCH(COV=HUBER) bounded_x c bounded_x(-1)
    xroll_exp.fit(d,e,g) xroll_f @se xroll_se @garch xroll_g
    smpl @first-1+!day+!cc @first-1+!day+!cc
    series xroll=@sqrt(xroll_g)
    series xroll_c=xroll_exp.@coef(1)
    series xroll_a=xroll_exp.@coef(2)
    series xroll_ao=xroll_exp.@coef(3)
    series xroll_beta=xroll_exp.@coef(4)
    series xroll_alpha=xroll_exp.@coef(5)
    series xroll_sc=xroll_exp.@stderrs(1)
    series xroll_sa=xroll_exp.@stderrs(2)
    series xroll_sao=xroll_exp.@stderrs(3)
    series xroll_sbeta=xroll_exp.@stderrs(4)
    series xroll_salpha=xroll_exp.@stderrs(5)
    series xroll_tc=xroll_exp.@tstat(1)
    series xroll_ta=xroll_exp.@tstat(2)
    series xroll_tao=xroll_exp.@tstat(3)
    series xroll_tbeta=xroll_exp.@tstat(4)
    series xroll_talpha=xroll_exp.@tstat(5)
    !roll_kappa = 1 - xroll_exp.@coef(2)
    !roll_theta = xroll_exp.@coef(1) / !roll_kappa
    series xroll_kappa = !roll_kappa
    series xroll_theta = !roll_theta
    series xroll_kappa_se = xroll_exp.@stderrs(2)

    series xroll_theta_se = @sqrt((xroll_exp.@stderrs(1)/xroll_exp.@coef(1))^2 + (xroll_exp.@stderrs(2)/xroll_exp.@coef(2))^2) * @abs(!roll_theta)


next

!day=749


for !cc=!startDay to !total-!day
    smpl @first @first-1+!day+!cc
    equation xexpand_exp.ARCH(COV=HUBER) bounded_x c bounded_x(-1)
    smpl @first-1+!day+!cc @first-1+!day+!cc
    xexpand_exp.fit(d,e,g) xex_f @se xex_se @garch xex_g
    series xexpand=@sqrt(xex_g)
    series xex_c=xexpand_exp.@coef(1)
    series xex_a=xexpand_exp.@coef(2)	
    series xex_sc=xexpand_exp.@stderrs(1)
    series xex_sa=xexpand_exp.@stderrs(2)	
    series xex_tc=xroll_exp.@tstat(1)
    series xex_ta=xroll_exp.@tstat(2)


    !expand_kappa = 1 - xexpand_exp.@coef(2)
    !expand_theta = xexpand_exp.@coef(1) / !expand_kappa
    series xexpand_kappa = !expand_kappa
    series xexpand_theta = !expand_theta
    series xexpand_kappa_se = xexpand_exp.@stderrs(2)
    series xexpand_theta_se = @sqrt((xexpand_exp.@stderrs(1)/xexpand_exp.@coef(1))^2 + (xexpand_exp.@stderrs(2)/xexpand_exp.@coef(2))^2) * @abs(!expand_theta)

next

!day=749

if !offset = -1 then
delete(noerr) xroll_sigma
delete(noerr) xroll_sigma_se
delete(noerr) xexpand_sigma
delete(noerr) xexpand_sigma_se
endif
smpl @all
if negx = 0 then
    for !cc=!sigmastartDay to !total-!day-!day
        smpl @first-1+!day+!cc @first-1+!day+!cc+!day
        scalar xroll_sigma_s =  @mean(@ediv(xroll , x_sqrt ))
        scalar xroll_sigma_se_s =  @stdev(@ediv(xroll , x_sqrt)) / @sqrt(@obssmpl)
        smpl @first+!day @first-1+!day+!cc+!day
        scalar xexpand_sigma_s = @mean(@ediv(xexpand,x_sqrt) )
        scalar xexpand_sigma_se_s = @stdev(@ediv(xexpand,x_sqrt) )/ @sqrt(@obssmpl)
        smpl @first-1+!day+!cc+!day @first-1+!day+!cc+!day
        series xroll_sigma =  xroll_sigma_s
        series xroll_sigma_se =  xroll_sigma_se_s
        series xexpand_sigma =  xexpand_sigma_s
        series xexpand_sigma_se =  xexpand_sigma_se_s
        d xroll_sigma_s
        d xroll_sigma_se_s
        d xexpand_sigma_s
        d xexpand_sigma_se_s
    next
else
    smpl @first+!day+!day @last
    series xroll_sigma = -1
    series xroll_sigma_se =  -1
    series xexpand_sigma =  -1
    series xexpand_sigma_se =  -1
endif
smpl @all

wfsave(2) %filename
wfsave(2, type=text) %savename @keep date xexpand_kappa xexpand_kappa_se xexpand_theta xexpand_theta_se xexpand_sigma xexpand_sigma_se  xroll_kappa xroll_kappa_se xroll_theta xroll_theta_se xroll_sigma xroll_sigma_se

toc
wfclose

