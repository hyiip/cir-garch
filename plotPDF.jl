using LaTeXStrings,Plots
using SpecialFunctions
using QuadGK
using Distributions

SU = 5
SL = 0

#SU - exp(-theta) * SU

omega(kappa, theta, sigma) = 2 * kappa * theta / (sigma^2) - 1
#beta(kappa, sigma) = 2 * kappa / sigma^2
f(x;kappa, theta, sigma) =  x^(omega(kappa, theta, sigma)) / gamma(omega(kappa, theta, sigma)+1) * (2 * kappa / sigma^2)^(omega(kappa, theta, sigma)+1) * exp(-2 * kappa / sigma^2 * x)
s(S;SU,SL) = - log((SU - S) / (SU - SL))
logf2(S;SU,SL,kappa, theta, sigma) = omega(kappa, theta, sigma) * log(s(S,SU = SU,SL = SL)) - loggamma(omega(kappa, theta, sigma)+1) + (omega(kappa, theta, sigma)+1) * log(2 * kappa / sigma^2) - 2 * kappa / sigma^2 * s(S,SU = SU,SL = SL) - log(SU - S)
f2(S;SU,SL,kappa, theta, sigma) =  exp(logf2(S, SU = SU,SL = SL,kappa = kappa, theta = theta, sigma = sigma))

#res = quadgk(x -> f(x,kappa = kappa, theta = 0.3, sigma = sigma), 0, Inf)
#println(res)
#plot(f, 0, 1)
#alpha1 = 2 * kappa * theta / (sigma^2)
#g(x) = beta^(alpha1) / gamma(alpha1) * x^(alpha1-1) * exp(-beta * x)

#res2 = quadgk(x -> g(x), 0, Inf)
#println(res2)
#g(0.25)
#print(omega(kappa, 0.3, sigma))
#plot(x-> f(x,kappa = kappa, theta = 0.30, sigma = sigma), 0, 10, label="θ = 0.3", title = "κ = $kappa, σ = $sigma, SL = $SL, SU = $SU")

#kappa = 0.05;
#sigma = 0.007;

#kappa = 0.07;
#sigma = 0.02;

#kappa = 0.07;
#sigma = 0.08;

kappa = 0.03;
sigma = 0.14;
#kappa = 0.072;
#sigma = 0.14;
#kappa = 0.072;
#sigma = 0.14;

#kappa = 0.059;
#sigma = 0.045;

#kappa = 0.043;
#sigma = 0.031;

#kappa = 0.024;
#sigma = 0.034;

#kappa = 0.052;
#sigma = 0.052;

panelIndex = "C"

println(quadgk(x -> f2(x,SU = SU,SL = SL,kappa = kappa, theta = 0.3, sigma = sigma), SL, SU))

plot(S-> f2(S,SU = SU, SL = SL, kappa = kappa, theta = 0.25, sigma = sigma), SL, SU,
            label="θ = 0.25",fg_legend = :transparent,background_color_legend = nothing)
plot!(S-> f2(S,SU = SU, SL = SL, kappa = kappa, theta = 0.75, sigma = sigma), SL, SU,
            label="θ = 0.75", linestyle = :dash, linecolor = :red)
plot!(S-> f2(S,SU = SU, SL = SL, kappa = kappa, theta = 1.5, sigma = sigma), SL, SU,
            label="θ = 1.5", linestyle = :dashdot, linecolor = :black, title = "Panel $panelIndex\n κ = $kappa, σₓ = $sigma", legend=:top, padding = (0.0, 0.0))

#=
plot(S-> f2(S,SU = SU, SL = SL, kappa = kappa, theta = 0.25, sigma = sigma), SL, SU,
            label="θ = 0.25",fg_legend = :transparent,background_color_legend = nothing)
plot!(S-> f2(S,SU = SU, SL = SL, kappa = kappa, theta = 0.75, sigma = sigma), SL, SU,
            label="θ = 0.75", linestyle = :dash, linecolor = :red)
plot!(S-> f2(S,SU = SU, SL = SL, kappa = kappa, theta = 1.5, sigma = sigma), SL, SU,
            label="θ = 1.5", linestyle = :dashdot, linecolor = :black, title = "Panel $panelIndex\n κ = $kappa, σ = $sigma", legend=:top, padding = (0.0, 0.0))
=#

xlabel!("Bond Yield")
ylabel!("PDF")
xticks!(0:SU/10:SU)
#savefig("paper/bond/fig3_PDF_$(panelIndex).png")
#plot!(S-> f2(S,SU = SU, SL = SL, kappa = kappa, theta = 1, sigma = sigma),  SL, SU, label="θ = 1")
#plot!(S-> f2(S,SU = SU, SL = SL, kappa = kappa, theta = 1.5, sigma = sigma),  SL, SU, label="θ = 1.5")
