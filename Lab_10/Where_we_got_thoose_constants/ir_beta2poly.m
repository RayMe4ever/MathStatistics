function [vertices] = ir_beta2poly(irproblem)

## Get IR problem data
X = irproblem.X;
y = irproblem.y;
epsilon = irproblem.epsilon;
C = irproblem.C;
d = irproblem.d;
ctype = irproblem.ctype;
lb = irproblem.lb;
ub = irproblem.ub;

##  Unfold epsilon
if numel(epsilon)==1
  epsilon = epsilon*ones(numel(y),1);
endif

## Prepare inequalities defining feasible parameters set polytope
A = [X; -X];
b = [y+epsilon; -y+epsilon];

Lidx = (ctype == 'L');
A = [ A; -C(Lidx,:) ];
b = [ b; -d(Lidx) ];

Sidx = (ctype == 'S');
Aeq = C(Sidx,:);
beq = d(Sidx);

[A,b,Aeq,beq] = addBounds(A,b,Aeq,beq,lb,ub);

## Calculate vertices of feasibile parameters set
warning('off', 'Octave:colon-nonscalar-argument');
[V,nr] = lcon2vert(A,b,Aeq,beq);

dim = size(V,2);
if dim == 1
  k = nr;
elseif dim == 2
  k = convhull(V(:,1),V(:,2));
  k = k(1:end-1);
else
  h = convhulln(V);
  k = unique(h(:));
endif

vertices = V(k,:);

endfunction
