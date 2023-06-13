max: t0e0 - t3e0;

/* Time Constraints */
t1e0 <= t0e0;
t2e0 <= t1e0;
t4e0 <= t3e0;
t3e0 <= t1e0;
t5e0 <= t4e0;
t4e0 <= t2e0;

/* arrival constraints */
f0s0t3e0 - f0s0t4e0 <= x0 + 3000000.0 t3e0 - 3000000.0 t4e0;
f0s0t3e0 - f0s0t5e0 <= x0 + 3000000.0 t3e0 - 3000000.0 t5e0;
f0s0t4e0 - f0s0t5e0 <= x0 + 3000000.0 t4e0 - 3000000.0 t5e0;
f1s0t3e0 - f1s0t4e0 <= x1 + 2400000.0 t3e0 - 2400000.0 t4e0;
f1s0t3e0 - f1s0t5e0 <= x1 + 2400000.0 t3e0 - 2400000.0 t5e0;
f1s0t4e0 - f1s0t5e0 <= x1 + 2400000.0 t4e0 - 2400000.0 t5e0;
f2s1t1e0 - f2s1t2e0 <= x2 + 2400000.0 t1e0 - 2400000.0 t2e0;
f3s0t3e0 - f3s0t4e0 <= x3 + 2400000.0 t3e0 - 2400000.0 t4e0;
f3s0t3e0 - f3s0t5e0 <= x3 + 2400000.0 t3e0 - 2400000.0 t5e0;
f3s0t4e0 - f3s0t5e0 <= x3 + 2400000.0 t4e0 - 2400000.0 t5e0;

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
0+f0s0t3e0 - f0s0t4e0+f3s0t3e0 - f3s0t4e0<= 0 + 10000000t3e0 - 10000000t4e0;
0+f0s0t3e0 - f0s0t5e0+f3s0t3e0 - f3s0t5e0<= 0 + 10000000t3e0 - 10000000t5e0;
0+f0s0t4e0 - f0s0t5e0+f3s0t4e0 - f3s0t5e0<= 0 + 10000000t4e0 - 10000000t5e0;

/* SFA delay constraints */
t0e0 - t3e0 <= 4.698501076923077e-05;
t0e0 - t3e0 <= 4.749037043478261e-05;
t0e0 - t1e0 <= 2.9562470434782613e-05;
t1e0 - t3e0 <= 3.3558293478260865e-05;
t2e0 - t4e0 <= 3.3558293478260865e-05;

/* TFA delay constraints */
t1e0 - t3e0 <= 1.78901e-05;
t2e0 - t4e0 <= 1.78901e-05;
t0e0 - t1e0 <= 1.92727e-05;
x0 = 57.7875;
x1 = 8;
x2 = 8;
x3 = 78.1059;
