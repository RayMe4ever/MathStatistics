pkg load interval

fid = fopen('Chanel.txt', 'r');
A = fscanf(fid, '%f', [200 1]);
fclose(fid);

epsilon0 = 10^-4;




[tau, w, yint] = DataLinearModelZ(A, epsilon0);


lb = []

B1 = ones(31,2);
B2 = ones(146,2);
B3 = ones(25,2);

A1 = ones(31,1);
A2 = ones(146,1);
A3 = ones(25,1);

max1 = 0;
max2 = 0;
max3 = 0;

for i =1:31
  B1(i, 2) = i;
  A1(i)=A(i);
  if w(i) > max1
    max1 = w(i);
  endif
endfor

for i =1:146
  B2(i, 2) = i + 30;
  A2(i)=A(i+30);
  if w(i + 30) > max2
    max2 = w(i+30);
  endif
endfor

for i =1:25
  B3(i, 2) = i + 175;
  A3(i)=A(i+175);
  if w(i + 175) > max3
    max3 = w(i+175);
  endif
endfor


% Решение задачи линейного программирования
SS = ir_problem(B1, A1, max1 * epsilon0);
% Вершины информационного множества задачи
% построения интервальной регрессии
vertices = ir_beta2poly(SS);
% Внешние интервальные оценки параметров
% модели y = beta1 + beta2 * x
b_int = ir_outer(SS)

% Решение задачи линейного программирования
SS = ir_problem(B2, A2, max2 * epsilon0);
% Вершины информационного множества задачи
% построения интервальной регрессии
vertices = ir_beta2poly(SS);
% Внешние интервальные оценки параметров
% модели y = beta1 + beta2 * x
b_int = ir_outer(SS)

% Решение задачи линейного программирования
SS = ir_problem(B3, A3, max3 * epsilon0);
% Вершины информационного множества задачи
% построения интервальной регрессии
vertices = ir_beta2poly(SS);
% Внешние интервальные оценки параметров
% модели y = beta1 + beta2 * x
b_int = ir_outer(SS)
