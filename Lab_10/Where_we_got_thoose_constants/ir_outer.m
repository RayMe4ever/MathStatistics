function [beta, exitcode, active] = ir_outer(irproblem)

X = irproblem.X;
y = irproblem.y;
epsilon = irproblem.epsilon;

C = irproblem.C;
d = irproblem.d;
Cdctype = irproblem.ctype;

if ~isfield(irproblem,'lb') || isempty(irproblem.lb)
  lb = -Inf*ones(size(X,2),1);
else
  lb = irproblem.lb;
endif

if ~isfield(irproblem,'ub') || isempty(irproblem.ub)
  ub = Inf*ones(size(X,2),1);
else
  ub = irproblem.ub;
endif

## Build matrix and right-hand side vector of linear programming problem
A = [X; -X; C];
b = [y+epsilon; -y+epsilon; d];
[n m] = size(X);

ctype(1:2*n) = 'U'; # constraints type is inequality
if ~isempty(Cdctype)
  ctype = [ctype; Cdctype];
endif
vartype(1:m) = 'C'; # variable type is continuous
sense = 1; % find minimum

## Siginificant digit for active bounds detection
SIGNIFICANT=0.0000001;

## Parameters estiamtes
beta = [];

## Lagrange multipliers (to detect active constraints)
L = [];

## Solve 2*m linear programming problems in order to find
## lower and upper bounds for feasible parameters set on each axis
for i = 1:m

  ## Set objective function coefficients
  c = zeros(1,m);
  c(i) = 1;

  ## Solve LPPs and save indicies for non-zero Lagrange multipliers

  exitcode = 1;
  [btlow, flow, errcode, lambda] = glpk (c, A, b, lb, ub, ctype, vartype, sense);
  if errcode > 0
      exitcode = -errcode;
      return
  endif
  L = unique([L; find(abs(lambda.lambda) > SIGNIFICANT)]);

  [bthigh, fhigh, errcode, lambda] = glpk (-c, A, b, lb, ub, ctype, vartype, sense);
  if errcode > 0
      exitcode = -errcode;
      return
  endif
  L = unique([L; find(abs(lambda.lambda) > SIGNIFICANT)]);

  ## Save lower and upper bounds for i-th parameter
  beta = [beta; [flow -fhigh]];
endfor

## Detect active boundary observations
active.lower = L(find(L>n))-n;
active.upper = L(find(L<=n));

## TODO: add active optional constraints

endfunction
