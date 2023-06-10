max: f8s0t0e0 - f8s1t0e0;
f8s0t0e0 - f8s0t1e0 <= 800.0 + 5.0t0e0 - 5.0t1e0;
f8s0t0e0 - f8s0t2e0 <= 800.0 + 5.0t0e0 - 5.0t2e0;

/* Time Constraints */
t1e0 <= t0e0;
t2e0 <= t1e0;

/* arrival constraints */
f0s0t1e0 - f0s0t2e0 <= x0 + 5.0 t1e0 - 5.0 t2e0;
f1s0t1e0 - f1s0t2e0 <= x1 + 5.0 t1e0 - 5.0 t2e0;
f2s0t1e0 - f2s0t2e0 <= x2 + 5.0 t1e0 - 5.0 t2e0;
f3s0t1e0 - f3s0t2e0 <= x3 + 5.0 t1e0 - 5.0 t2e0;
f4s0t1e0 - f4s0t2e0 <= x4 + 5.0 t1e0 - 5.0 t2e0;
f5s0t1e0 - f5s0t2e0 <= x5 + 5.0 t1e0 - 5.0 t2e0;
f6s0t1e0 - f6s0t2e0 <= x6 + 5.0 t1e0 - 5.0 t2e0;
f7s0t1e0 - f7s0t2e0 <= x7 + 5.0 t1e0 - 5.0 t2e0;
f8s0t1e0 - f8s0t2e0 <= x8 + 5.0 t1e0 - 5.0 t2e0;
f9s0t1e0 - f9s0t2e0 <= x9 + 5.0 t1e0 - 5.0 t2e0;

/* fifo constraints */
f0s0t1e0= f0s1t0e0; 
f1s0t1e0= f1s1t0e0; 
f2s0t1e0= f2s1t0e0; 
f3s0t1e0= f3s1t0e0; 
f4s0t1e0= f4s1t0e0; 
f5s0t1e0= f5s1t0e0; 
f6s0t1e0= f6s1t0e0; 
f7s0t1e0= f7s1t0e0; 
f8s0t1e0= f8s1t0e0; 
f9s0t1e0= f9s1t0e0; 

/* Service constraints */
f0s1t0e0 - f0s0t2e0 + f1s1t0e0 - f1s0t2e0 + f2s1t0e0 - f2s0t2e0 + f3s1t0e0 - f3s0t2e0 + f4s1t0e0 - f4s0t2e0 + f5s1t0e0 - f5s0t2e0 + f6s1t0e0 - f6s0t2e0 + f7s1t0e0 - f7s0t2e0 + f8s1t0e0 - f8s0t2e0 + f9s1t0e0 - f9s0t2e0 + 1000.0 >= 100.0 t0e0 - 100.0 t2e0;
f0s1t0e0 - f0s0t2e0 + f1s1t0e0 - f1s0t2e0 + f2s1t0e0 - f2s0t2e0 + f3s1t0e0 - f3s0t2e0 + f4s1t0e0 - f4s0t2e0 + f5s1t0e0 - f5s0t2e0 + f6s1t0e0 - f6s0t2e0 + f7s1t0e0 - f7s0t2e0 + f8s1t0e0 - f8s0t2e0 + f9s1t0e0 - f9s0t2e0 + 0 >= 0;

/* Monotony constraints */
f0s0t1e0 - f0s0t2e0 >= 0; 
f1s0t1e0 - f1s0t2e0 >= 0; 
f2s0t1e0 - f2s0t2e0 >= 0; 
f3s0t1e0 - f3s0t2e0 >= 0; 
f4s0t1e0 - f4s0t2e0 >= 0; 
f5s0t1e0 - f5s0t2e0 >= 0; 
f6s0t1e0 - f6s0t2e0 >= 0; 
f7s0t1e0 - f7s0t2e0 >= 0; 
f8s0t1e0 - f8s0t2e0 >= 0; 
f9s0t1e0 - f9s0t2e0 >= 0; 

/* Shaping constraints (e.g. maximum rate of a link)*/

/* arrival shaping constraints */
0+f0s0t1e0 - f0s0t2e0+f1s0t1e0 - f1s0t2e0+f2s0t1e0 - f2s0t2e0+f3s0t1e0 - f3s0t2e0+f4s0t1e0 - f4s0t2e0+f5s0t1e0 - f5s0t2e0+f6s0t1e0 - f6s0t2e0+f7s0t1e0 - f7s0t2e0+f9s0t1e0 - f9s0t2e0<= 0.0 + 100.0t1e0 - 100.0t2e0;

/* SFA delay constraints */
t0e0 - t1e0 <= 165.41337565036366;
t0e0 - t1e0 <= 161.9483014767273;
t0e0 - t1e0 <= 161.04457470363636;
t0e0 - t1e0 <= 160.04638778818182;
t0e0 - t1e0 <= 159.04453847236363;
t0e0 - t1e0 <= 158.03492845745455;
t0e0 - t1e0 <= 157.00320265636364;
t0e0 - t1e0 <= 155.92829772727274;
t0e0 - t1e0 <= 155.10698454545454;
t0e0 - t1e0 <= 165.41337565036366;

/* TFA delay constraints */
t0e0 - t1e0 <= 29.8692;
x0 = 2059.66451077;
x1 = 1636.16593122;
x2 = 1525.7079587;
x3 = 1403.70217835;
x4 = 1281.25846598;
x5 = 1157.85991516;
x6 = 1031.7544961;
x7 = 900.382875;
x8 = 800.0;
x9 = 2059.66451077;
