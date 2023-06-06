function [tau, w, yint] = DataLinearModel (input1, epsilon0)
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
% w > 1
[tau, w] = L_1_minimization(X, inf_b, sup_b);
% new rad vector
rady=epsilon0*w;
yint=midrad(yy, rady);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


endfunction
