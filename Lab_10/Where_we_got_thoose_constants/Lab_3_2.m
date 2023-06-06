pkg load interval

fid = fopen('Chanel.txt', 'r');
A = fscanf(fid, '%f', [200 1]);
fclose(fid);

epsilon0 = 10^-4;




[tau, w, yint] = DataLinearModelZ(A, epsilon0);


lb = []

B = ones(200,2);

for i =1:200
  B(i, 2) = i;
endfor


% Решение задачи линейного программирования
SS = ir_problem(B, A, 2.3236 * epsilon0);
% Вершины информационного множества задачи
% построения интервальной регрессии
vertices = ir_beta2poly(SS);
% Внешние интервальные оценки параметров
% модели y = beta1 + beta2 * x
b_int = ir_outer(SS)
