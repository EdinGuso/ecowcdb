max: f15s0t0e0 - f15s1t0e0;
f15s0t0e0 - f15s0t1e0 <= 45.2470558 + 312500.0t0e0 - 312500.0t1e0;
f15s0t0e0 - f15s0t2e0 <= 45.2470558 + 312500.0t0e0 - 312500.0t2e0;

/* Time Constraints */
t1e0 <= t0e0;
t2e0 <= t1e0;

/* arrival constraints */
f0s0t1e0 - f0s0t2e0 <= x0 + 312500.0 t1e0 - 312500.0 t2e0;
f1s0t1e0 - f1s0t2e0 <= x1 + 312500.0 t1e0 - 312500.0 t2e0;
f2s0t1e0 - f2s0t2e0 <= x2 + 312500.0 t1e0 - 312500.0 t2e0;
f3s0t1e0 - f3s0t2e0 <= x3 + 312500.0 t1e0 - 312500.0 t2e0;
f4s0t1e0 - f4s0t2e0 <= x4 + 312500.0 t1e0 - 312500.0 t2e0;
f5s0t1e0 - f5s0t2e0 <= x5 + 312500.0 t1e0 - 312500.0 t2e0;
f6s0t1e0 - f6s0t2e0 <= x6 + 312500.0 t1e0 - 312500.0 t2e0;
f7s0t1e0 - f7s0t2e0 <= x7 + 312500.0 t1e0 - 312500.0 t2e0;
f8s0t1e0 - f8s0t2e0 <= x8 + 312500.0 t1e0 - 312500.0 t2e0;
f9s0t1e0 - f9s0t2e0 <= x9 + 312500.0 t1e0 - 312500.0 t2e0;
f10s0t1e0 - f10s0t2e0 <= x10 + 312500.0 t1e0 - 312500.0 t2e0;
f11s0t1e0 - f11s0t2e0 <= x11 + 312500.0 t1e0 - 312500.0 t2e0;
f12s0t1e0 - f12s0t2e0 <= x12 + 312500.0 t1e0 - 312500.0 t2e0;
f13s0t1e0 - f13s0t2e0 <= x13 + 312500.0 t1e0 - 312500.0 t2e0;
f14s0t1e0 - f14s0t2e0 <= x14 + 312500.0 t1e0 - 312500.0 t2e0;
f15s0t1e0 - f15s0t2e0 <= x15 + 312500.0 t1e0 - 312500.0 t2e0;

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
f10s0t1e0= f10s1t0e0; 
f11s0t1e0= f11s1t0e0; 
f12s0t1e0= f12s1t0e0; 
f13s0t1e0= f13s1t0e0; 
f14s0t1e0= f14s1t0e0; 
f15s0t1e0= f15s1t0e0; 

/* Service constraints */
f0s1t0e0 - f0s0t2e0 + f1s1t0e0 - f1s0t2e0 + f2s1t0e0 - f2s0t2e0 + f3s1t0e0 - f3s0t2e0 + f4s1t0e0 - f4s0t2e0 + f5s1t0e0 - f5s0t2e0 + f6s1t0e0 - f6s0t2e0 + f7s1t0e0 - f7s0t2e0 + f8s1t0e0 - f8s0t2e0 + f9s1t0e0 - f9s0t2e0 + f10s1t0e0 - f10s0t2e0 + f11s1t0e0 - f11s0t2e0 + f12s1t0e0 - f12s0t2e0 + f13s1t0e0 - f13s0t2e0 + f14s1t0e0 - f14s0t2e0 + f15s1t0e0 - f15s0t2e0 + 100.00000000000001 >= 10000000 t0e0 - 10000000 t2e0;
f0s1t0e0 - f0s0t2e0 + f1s1t0e0 - f1s0t2e0 + f2s1t0e0 - f2s0t2e0 + f3s1t0e0 - f3s0t2e0 + f4s1t0e0 - f4s0t2e0 + f5s1t0e0 - f5s0t2e0 + f6s1t0e0 - f6s0t2e0 + f7s1t0e0 - f7s0t2e0 + f8s1t0e0 - f8s0t2e0 + f9s1t0e0 - f9s0t2e0 + f10s1t0e0 - f10s0t2e0 + f11s1t0e0 - f11s0t2e0 + f12s1t0e0 - f12s0t2e0 + f13s1t0e0 - f13s0t2e0 + f14s1t0e0 - f14s0t2e0 + f15s1t0e0 - f15s0t2e0 + 0 >= 0;

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
f10s0t1e0 - f10s0t2e0 >= 0; 
f11s0t1e0 - f11s0t2e0 >= 0; 
f12s0t1e0 - f12s0t2e0 >= 0; 
f13s0t1e0 - f13s0t2e0 >= 0; 
f14s0t1e0 - f14s0t2e0 >= 0; 
f15s0t1e0 - f15s0t2e0 >= 0; 

/* Shaping constraints (e.g. maximum rate of a link)*/

/* arrival shaping constraints */
0+f0s0t1e0 - f0s0t2e0+f2s0t1e0 - f2s0t2e0+f4s0t1e0 - f4s0t2e0+f6s0t1e0 - f6s0t2e0+f8s0t1e0 - f8s0t2e0+f10s0t1e0 - f10s0t2e0+f12s0t1e0 - f12s0t2e0+f14s0t1e0 - f14s0t2e0<= 0 + 10000000t1e0 - 10000000t2e0;
0+f1s0t1e0 - f1s0t2e0+f3s0t1e0 - f3s0t2e0+f5s0t1e0 - f5s0t2e0+f7s0t1e0 - f7s0t2e0+f9s0t1e0 - f9s0t2e0+f11s0t1e0 - f11s0t2e0+f13s0t1e0 - f13s0t2e0+f15s0t1e0 - f15s0t2e0<= 0 + 10000000t1e0 - 10000000t2e0;

/* SFA delay constraints */
t0e0 - t1e0 <= 8.531390435294117e-05;
t0e0 - t1e0 <= 8.531390435294117e-05;
t0e0 - t1e0 <= 8.548422285647058e-05;
t0e0 - t1e0 <= 8.548422285647058e-05;
t0e0 - t1e0 <= 8.545524763576472e-05;
t0e0 - t1e0 <= 8.545524763576472e-05;
t0e0 - t1e0 <= 8.548422285647058e-05;
t0e0 - t1e0 <= 8.548422285647058e-05;
t0e0 - t1e0 <= 8.531390435294117e-05;
t0e0 - t1e0 <= 8.531390435294117e-05;
t0e0 - t1e0 <= 8.548422285647058e-05;
t0e0 - t1e0 <= 8.548422285647058e-05;
t0e0 - t1e0 <= 8.545524763576472e-05;
t0e0 - t1e0 <= 8.545524763576472e-05;
t0e0 - t1e0 <= 8.548422285647058e-05;
t0e0 - t1e0 <= 8.548422285647058e-05;

/* TFA delay constraints */
t0e0 - t1e0 <= 5.76612e-05;
x0 = 43.31671375;
x1 = 43.31671375;
x2 = 45.2470558;
x3 = 45.2470558;
x4 = 44.91866244;
x5 = 44.91866244;
x6 = 45.2470558;
x7 = 45.2470558;
x8 = 43.31671375;
x9 = 43.31671375;
x10 = 45.2470558;
x11 = 45.2470558;
x12 = 44.91866244;
x13 = 44.91866244;
x14 = 45.2470558;
x15 = 45.2470558;
