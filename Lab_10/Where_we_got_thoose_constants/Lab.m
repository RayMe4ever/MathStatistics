pkg load interval

fid = fopen('Chanel.txt', 'r');
A = fscanf(fid, '%f', [200 1]);
fclose(fid);

epsilon0 = 10^-4;

[tau, w, yint] = DataLinearModel(A, epsilon0);
fid = fopen('w0.csv', 'w+');
fprintf(fid, '%3.1f;\n', w);
fclose(fid);


[tau, w, yint] = DataLinearModelZ(A, epsilon0);
##sum = 0;
##for i =1:200
##  sum = sum + w(i);
##endfor
##sum
fid = fopen('w.csv', 'w+');
fprintf(fid, '%3.5f;\n', w);
fclose(fid);


