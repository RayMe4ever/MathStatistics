function [tauZ, wZ, yint] = DataLinearModelZ (input1, epsilon0)
  x1 = input1;
%
yy = x1(:,1);
n = length(yy);
xx = 1:n;
xx=xx';
X = [ xx.^0 xx ];
[n, m]=size(X);
% instrument error
% epsilon0 = 10^(-4)
epsilon= epsilon0  * ones(n,1);
inf_b = yy - epsilon;
sup_b = yy + epsilon;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Linear programming
%[tau, w] = L_1_minimization(X, inf_b, sup_b);
%[tauNN, wNN] = L_1_minimizationNonNeg(X, inf_b, sup_b);
% w >= 0
[tauZ, wZ] = L_1_minimizationZ(X, inf_b, sup_b);
% new rad vector
rady=epsilon0*wZ;
yint=midrad(yy, rady);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


endfunction
