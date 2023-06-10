max: t0e0 - t3e0;

/* Time Constraints */
t1e0 <= t0e0;
t2e0 <= t1e0;
t4e0 <= t3e0;
t3e0 <= t1e0;
t5e0 <= t4e0;
t4e0 <= t2e0;

/* arrival constraints */
f0s0t3e0 - f0s0t4e0 <= x0 + 1666666.6666666667 t3e0 - 1666666.6666666667 t4e0;
f0s0t3e0 - f0s0t5e0 <= x0 + 1666666.6666666667 t3e0 - 1666666.6666666667 t5e0;
f0s0t4e0 - f0s0t5e0 <= x0 + 1666666.6666666667 t4e0 - 1666666.6666666667 t5e0;
f1s0t3e0 - f1s0t4e0 <= x1 + 1666666.6666666667 t3e0 - 1666666.6666666667 t4e0;
f1s0t3e0 - f1s0t5e0 <= x1 + 1666666.6666666667 t3e0 - 1666666.6666666667 t5e0;
f1s0t4e0 - f1s0t5e0 <= x1 + 1666666.6666666667 t4e0 - 1666666.6666666667 t5e0;
f2s1t1e0 - f2s1t2e0 <= x2 + 1666666.6666666667 t1e0 - 1666666.6666666667 t2e0;
f3s0t3e0 - f3s0t4e0 <= x3 + 1666666.6666666667 t3e0 - 1666666.6666666667 t4e0;
f3s0t3e0 - f3s0t5e0 <= x3 + 1666666.6666666667 t3e0 - 1666666.6666666667 t5e0;
f3s0t4e0 - f3s0t5e0 <= x3 + 1666666.6666666667 t4e0 - 1666666.6666666667 t5e0;

/* fifo constraints */
f0s0t3e0 = f0s1t1e0; 
f0s0t4e0 = f0s1t2e0; 
f0s1t1e0= f0s2t0e0; 
f1s0t3e0 = f1s1t1e0; 
f1s0t4e0 = f1s1t2e0; 
f1s1t1e0= f1s2t0e0; 
f2s1t1e0= f2s2t0e0; 
f3s0t3e0 = f3s1t1e0; 
f3s0t4e0 = f3s1t2e0; 

/* Service constraints */
f0s1t2e0 - f0s0t5e0 + f1s1t2e0 - f1s0t5e0 + f3s1t2e0 - f3s0t5e0 + 100.00000000000001 >= 10000000 t2e0 - 10000000 t5e0;
f0s1t2e0 - f0s0t5e0 + f1s1t2e0 - f1s0t5e0 + f3s1t2e0 - f3s0t5e0 + 0 >= 0;
f0s2t0e0 - f0s1t2e0 + f1s2t0e0 - f1s1t2e0 + f2s2t0e0 - f2s1t2e0 + 100.00000000000001 >= 10000000 t0e0 - 10000000 t2e0;
f0s2t0e0 - f0s1t2e0 + f1s2t0e0 - f1s1t2e0 + f2s2t0e0 - f2s1t2e0 + 0 >= 0;

/* Monotony constraints */
f0s0t3e0 - f0s0t4e0 >= 0; 
f0s0t4e0 - f0s0t5e0 >= 0; 
f0s1t1e0 - f0s1t2e0 >= 0; 
f1s0t3e0 - f1s0t4e0 >= 0; 
f1s0t4e0 - f1s0t5e0 >= 0; 
f1s1t1e0 - f1s1t2e0 >= 0; 
f2s1t1e0 - f2s1t2e0 >= 0; 
f3s0t3e0 - f3s0t4e0 >= 0; 
f3s0t4e0 - f3s0t5e0 >= 0; 

/* Shaping constraints (e.g. maximum rate of a link)*/
0+ f0s1t1e0 - f0s1t2e0 + f1s1t1e0 - f1s1t2e0 <= 0 + 10000000 t1e0 - 10000000 t2e0;

/* arrival shaping constraints */
0+f0s0t3e0 - f0s0t4e0+f3s0t3e0 - f3s0t4e0<= 0 + 5000000.0t3e0 - 5000000.0t4e0;
0+f0s0t3e0 - f0s0t5e0+f3s0t3e0 - f3s0t5e0<= 0 + 5000000.0t3e0 - 5000000.0t5e0;
0+f0s0t4e0 - f0s0t5e0+f3s0t4e0 - f3s0t5e0<= 0 + 5000000.0t4e0 - 5000000.0t5e0;

/* SFA delay constraints */
t0e0 - t3e0 <= 3.468287e-05;
t0e0 - t3e0 <= 3.541811e-05;
t0e0 - t1e0 <= 2.057524e-05;
t1e0 - t3e0 <= 2.10143e-05;
t2e0 - t4e0 <= 2.10143e-05;

/* TFA delay constraints */
t1e0 - t3e0 <= 1.08e-05;
t2e0 - t4e0 <= 1.08e-05;
t0e0 - t1e0 <= 1.26514e-05;
x0 = 30.0572;
x1 = 8;
x2 = 8;
x3 = 48.0572;
