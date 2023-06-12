max: + x0+ x1+ x2+ x3+ x4;

x0 = 8;

/* flow 0 */

/* Time Constraints */
t1e1 <= t0e1;
t2e1 <= t1e1;
t7e1 <= t6e1;
t6e1 <= t3e1;
t8e1 <= t7e1;
t7e1 <= t4e1;
t9e1 <= t8e1;
t8e1 <= t5e1;
t4e1 <= t3e1;
t3e1 <= t1e1;
t5e1 <= t4e1;
t4e1 <= t2e1;

/* arrival constraints */
f0s2t1e1 - f0s2t2e1 <= x0 + 3000000.0 t1e1 - 3000000.0 t2e1;
f1s0t6e1 - f1s0t7e1 <= x1 + 3000000.0 t6e1 - 3000000.0 t7e1;
f1s0t6e1 - f1s0t8e1 <= x1 + 3000000.0 t6e1 - 3000000.0 t8e1;
f1s0t6e1 - f1s0t9e1 <= x1 + 3000000.0 t6e1 - 3000000.0 t9e1;
f1s0t7e1 - f1s0t8e1 <= x1 + 3000000.0 t7e1 - 3000000.0 t8e1;
f1s0t7e1 - f1s0t9e1 <= x1 + 3000000.0 t7e1 - 3000000.0 t9e1;
f1s0t8e1 - f1s0t9e1 <= x1 + 3000000.0 t8e1 - 3000000.0 t9e1;
f2s0t6e1 - f2s0t7e1 <= x2 + 2400000.0 t6e1 - 2400000.0 t7e1;
f2s0t6e1 - f2s0t8e1 <= x2 + 2400000.0 t6e1 - 2400000.0 t8e1;
f2s0t6e1 - f2s0t9e1 <= x2 + 2400000.0 t6e1 - 2400000.0 t9e1;
f2s0t7e1 - f2s0t8e1 <= x2 + 2400000.0 t7e1 - 2400000.0 t8e1;
f2s0t7e1 - f2s0t9e1 <= x2 + 2400000.0 t7e1 - 2400000.0 t9e1;
f2s0t8e1 - f2s0t9e1 <= x2 + 2400000.0 t8e1 - 2400000.0 t9e1;
f3s1t3e1 - f3s1t4e1 <= x3 + 2400000.0 t3e1 - 2400000.0 t4e1;
f3s1t3e1 - f3s1t5e1 <= x3 + 2400000.0 t3e1 - 2400000.0 t5e1;
f3s1t4e1 - f3s1t5e1 <= x3 + 2400000.0 t4e1 - 2400000.0 t5e1;
f4s0t6e1 - f4s0t7e1 <= x4 + 2400000.0 t6e1 - 2400000.0 t7e1;
f4s0t6e1 - f4s0t8e1 <= x4 + 2400000.0 t6e1 - 2400000.0 t8e1;
f4s0t6e1 - f4s0t9e1 <= x4 + 2400000.0 t6e1 - 2400000.0 t9e1;
f4s0t7e1 - f4s0t8e1 <= x4 + 2400000.0 t7e1 - 2400000.0 t8e1;
f4s0t7e1 - f4s0t9e1 <= x4 + 2400000.0 t7e1 - 2400000.0 t9e1;
f4s0t8e1 - f4s0t9e1 <= x4 + 2400000.0 t8e1 - 2400000.0 t9e1;

/* fifo constraints */
f0s2t1e1= f0s3t0e1; 
f1s0t6e1 = f1s1t3e1; 
f1s0t7e1 = f1s1t4e1; 
f1s0t8e1 = f1s1t5e1; 
f1s1t3e1 = f1s2t1e1; 
f1s1t4e1 = f1s2t2e1; 
f2s0t6e1 = f2s1t3e1; 
f2s0t7e1 = f2s1t4e1; 
f2s0t8e1 = f2s1t5e1; 
f2s1t3e1 = f2s2t1e1; 
f2s1t4e1 = f2s2t2e1; 
f2s2t1e1= f2s3t0e1; 
f3s1t3e1 = f3s2t1e1; 
f3s1t4e1 = f3s2t2e1; 
f3s2t1e1= f3s3t0e1; 
f4s0t6e1 = f4s1t3e1; 
f4s0t7e1 = f4s1t4e1; 
f4s0t8e1 = f4s1t5e1; 

/* Service constraints */
f1s1t5e1 - f1s0t9e1 + f2s1t5e1 - f2s0t9e1 + f4s1t5e1 - f4s0t9e1 + 100.00000000000001 >= 10000000 t5e1 - 10000000 t9e1;
f1s1t5e1 - f1s0t9e1 + f2s1t5e1 - f2s0t9e1 + f4s1t5e1 - f4s0t9e1 + 0 >= 0;
f1s2t2e1 - f1s1t5e1 + f2s2t2e1 - f2s1t5e1 + f3s2t2e1 - f3s1t5e1 + 100.00000000000001 >= 10000000 t2e1 - 10000000 t5e1;
f1s2t2e1 - f1s1t5e1 + f2s2t2e1 - f2s1t5e1 + f3s2t2e1 - f3s1t5e1 + 0 >= 0;
f0s3t0e1 - f0s2t2e1 + f2s3t0e1 - f2s2t2e1 + f3s3t0e1 - f3s2t2e1 + 100.00000000000001 >= 10000000 t0e1 - 10000000 t2e1;
f0s3t0e1 - f0s2t2e1 + f2s3t0e1 - f2s2t2e1 + f3s3t0e1 - f3s2t2e1 + 0 >= 0;

/* Monotony constraints */
f0s2t1e1 - f0s2t2e1 >= 0; 
f1s0t6e1 - f1s0t7e1 >= 0; 
f1s0t7e1 - f1s0t8e1 >= 0; 
f1s0t8e1 - f1s0t9e1 >= 0; 
f1s1t3e1 - f1s1t4e1 >= 0; 
f1s1t4e1 - f1s1t5e1 >= 0; 
f2s0t6e1 - f2s0t7e1 >= 0; 
f2s0t7e1 - f2s0t8e1 >= 0; 
f2s0t8e1 - f2s0t9e1 >= 0; 
f2s1t3e1 - f2s1t4e1 >= 0; 
f2s1t4e1 - f2s1t5e1 >= 0; 
f2s2t1e1 - f2s2t2e1 >= 0; 
f3s1t3e1 - f3s1t4e1 >= 0; 
f3s1t4e1 - f3s1t5e1 >= 0; 
f3s2t1e1 - f3s2t2e1 >= 0; 
f4s0t6e1 - f4s0t7e1 >= 0; 
f4s0t7e1 - f4s0t8e1 >= 0; 
f4s0t8e1 - f4s0t9e1 >= 0; 

/* Shaping constraints (e.g. maximum rate of a link)*/
0+ f1s1t3e1 - f1s1t4e1 + f2s1t3e1 - f2s1t4e1 <= 0 + 10000000 t3e1 - 10000000 t4e1;
0+ f1s1t3e1 - f1s1t5e1 + f2s1t3e1 - f2s1t5e1 <= 0 + 10000000 t3e1 - 10000000 t5e1;
0+ f1s1t4e1 - f1s1t5e1 + f2s1t4e1 - f2s1t5e1 <= 0 + 10000000 t4e1 - 10000000 t5e1;
0+ f2s2t1e1 - f2s2t2e1 + f3s2t1e1 - f3s2t2e1 <= 0 + 10000000 t1e1 - 10000000 t2e1;

/* arrival shaping constraints */
0+f1s0t6e1 - f1s0t7e1+f4s0t6e1 - f4s0t7e1<= 0 + 10000000t6e1 - 10000000t7e1;
0+f1s0t6e1 - f1s0t8e1+f4s0t6e1 - f4s0t8e1<= 0 + 10000000t6e1 - 10000000t8e1;
0+f1s0t6e1 - f1s0t9e1+f4s0t6e1 - f4s0t9e1<= 0 + 10000000t6e1 - 10000000t9e1;
0+f1s0t7e1 - f1s0t8e1+f4s0t7e1 - f4s0t8e1<= 0 + 10000000t7e1 - 10000000t8e1;
0+f1s0t7e1 - f1s0t9e1+f4s0t7e1 - f4s0t9e1<= 0 + 10000000t7e1 - 10000000t9e1;
0+f1s0t8e1 - f1s0t9e1+f4s0t8e1 - f4s0t9e1<= 0 + 10000000t8e1 - 10000000t9e1;

/* TFA delay constraints */
t3e1 - t6e1 <= 2.01148e-05;
t4e1 - t7e1 <= 2.01148e-05;
t5e1 - t8e1 <= 2.01148e-05;
t1e1 - t3e1 <= 1.98534e-05;
t2e1 - t4e1 <= 1.98534e-05;
t0e1 - t1e1 <= 2.03767e-05;

/* SFA delay constraints */

/* the x burst constraints*/
x1 = f0s2t0e1 - f0s3t0e1;
f0s2t0e1 - f0s2t1e1 <= x0 + 3000000.0t0e1 - 3000000.0t1e1;
f0s2t0e1 - f0s2t2e1 <= x0 + 3000000.0t0e1 - 3000000.0t2e1;
x2 = 8;
x3 = 8;

/* flow 3 */

/* Time Constraints */
t1e4 <= t0e4;
t2e4 <= t1e4;
t7e4 <= t6e4;
t6e4 <= t3e4;
t8e4 <= t7e4;
t7e4 <= t4e4;
t9e4 <= t8e4;
t8e4 <= t5e4;
t4e4 <= t3e4;
t3e4 <= t1e4;
t5e4 <= t4e4;
t4e4 <= t2e4;

/* arrival constraints */
f0s2t1e4 - f0s2t2e4 <= x0 + 3000000.0 t1e4 - 3000000.0 t2e4;
f1s0t6e4 - f1s0t7e4 <= x1 + 3000000.0 t6e4 - 3000000.0 t7e4;
f1s0t6e4 - f1s0t8e4 <= x1 + 3000000.0 t6e4 - 3000000.0 t8e4;
f1s0t6e4 - f1s0t9e4 <= x1 + 3000000.0 t6e4 - 3000000.0 t9e4;
f1s0t7e4 - f1s0t8e4 <= x1 + 3000000.0 t7e4 - 3000000.0 t8e4;
f1s0t7e4 - f1s0t9e4 <= x1 + 3000000.0 t7e4 - 3000000.0 t9e4;
f1s0t8e4 - f1s0t9e4 <= x1 + 3000000.0 t8e4 - 3000000.0 t9e4;
f2s0t6e4 - f2s0t7e4 <= x2 + 2400000.0 t6e4 - 2400000.0 t7e4;
f2s0t6e4 - f2s0t8e4 <= x2 + 2400000.0 t6e4 - 2400000.0 t8e4;
f2s0t6e4 - f2s0t9e4 <= x2 + 2400000.0 t6e4 - 2400000.0 t9e4;
f2s0t7e4 - f2s0t8e4 <= x2 + 2400000.0 t7e4 - 2400000.0 t8e4;
f2s0t7e4 - f2s0t9e4 <= x2 + 2400000.0 t7e4 - 2400000.0 t9e4;
f2s0t8e4 - f2s0t9e4 <= x2 + 2400000.0 t8e4 - 2400000.0 t9e4;
f3s1t3e4 - f3s1t4e4 <= x3 + 2400000.0 t3e4 - 2400000.0 t4e4;
f3s1t3e4 - f3s1t5e4 <= x3 + 2400000.0 t3e4 - 2400000.0 t5e4;
f3s1t4e4 - f3s1t5e4 <= x3 + 2400000.0 t4e4 - 2400000.0 t5e4;
f4s0t6e4 - f4s0t7e4 <= x4 + 2400000.0 t6e4 - 2400000.0 t7e4;
f4s0t6e4 - f4s0t8e4 <= x4 + 2400000.0 t6e4 - 2400000.0 t8e4;
f4s0t6e4 - f4s0t9e4 <= x4 + 2400000.0 t6e4 - 2400000.0 t9e4;
f4s0t7e4 - f4s0t8e4 <= x4 + 2400000.0 t7e4 - 2400000.0 t8e4;
f4s0t7e4 - f4s0t9e4 <= x4 + 2400000.0 t7e4 - 2400000.0 t9e4;
f4s0t8e4 - f4s0t9e4 <= x4 + 2400000.0 t8e4 - 2400000.0 t9e4;

/* fifo constraints */
f0s2t1e4= f0s3t0e4; 
f1s0t6e4 = f1s1t3e4; 
f1s0t7e4 = f1s1t4e4; 
f1s0t8e4 = f1s1t5e4; 
f1s1t3e4 = f1s2t1e4; 
f1s1t4e4 = f1s2t2e4; 
f2s0t6e4 = f2s1t3e4; 
f2s0t7e4 = f2s1t4e4; 
f2s0t8e4 = f2s1t5e4; 
f2s1t3e4 = f2s2t1e4; 
f2s1t4e4 = f2s2t2e4; 
f2s2t1e4= f2s3t0e4; 
f3s1t3e4 = f3s2t1e4; 
f3s1t4e4 = f3s2t2e4; 
f3s2t1e4= f3s3t0e4; 
f4s0t6e4 = f4s1t3e4; 
f4s0t7e4 = f4s1t4e4; 
f4s0t8e4 = f4s1t5e4; 

/* Service constraints */
f1s1t5e4 - f1s0t9e4 + f2s1t5e4 - f2s0t9e4 + f4s1t5e4 - f4s0t9e4 + 100.00000000000001 >= 10000000 t5e4 - 10000000 t9e4;
f1s1t5e4 - f1s0t9e4 + f2s1t5e4 - f2s0t9e4 + f4s1t5e4 - f4s0t9e4 + 0 >= 0;
f1s2t2e4 - f1s1t5e4 + f2s2t2e4 - f2s1t5e4 + f3s2t2e4 - f3s1t5e4 + 100.00000000000001 >= 10000000 t2e4 - 10000000 t5e4;
f1s2t2e4 - f1s1t5e4 + f2s2t2e4 - f2s1t5e4 + f3s2t2e4 - f3s1t5e4 + 0 >= 0;
f0s3t0e4 - f0s2t2e4 + f2s3t0e4 - f2s2t2e4 + f3s3t0e4 - f3s2t2e4 + 100.00000000000001 >= 10000000 t0e4 - 10000000 t2e4;
f0s3t0e4 - f0s2t2e4 + f2s3t0e4 - f2s2t2e4 + f3s3t0e4 - f3s2t2e4 + 0 >= 0;

/* Monotony constraints */
f0s2t1e4 - f0s2t2e4 >= 0; 
f1s0t6e4 - f1s0t7e4 >= 0; 
f1s0t7e4 - f1s0t8e4 >= 0; 
f1s0t8e4 - f1s0t9e4 >= 0; 
f1s1t3e4 - f1s1t4e4 >= 0; 
f1s1t4e4 - f1s1t5e4 >= 0; 
f2s0t6e4 - f2s0t7e4 >= 0; 
f2s0t7e4 - f2s0t8e4 >= 0; 
f2s0t8e4 - f2s0t9e4 >= 0; 
f2s1t3e4 - f2s1t4e4 >= 0; 
f2s1t4e4 - f2s1t5e4 >= 0; 
f2s2t1e4 - f2s2t2e4 >= 0; 
f3s1t3e4 - f3s1t4e4 >= 0; 
f3s1t4e4 - f3s1t5e4 >= 0; 
f3s2t1e4 - f3s2t2e4 >= 0; 
f4s0t6e4 - f4s0t7e4 >= 0; 
f4s0t7e4 - f4s0t8e4 >= 0; 
f4s0t8e4 - f4s0t9e4 >= 0; 

/* Shaping constraints (e.g. maximum rate of a link)*/
0+ f1s1t3e4 - f1s1t4e4 + f2s1t3e4 - f2s1t4e4 <= 0 + 10000000 t3e4 - 10000000 t4e4;
0+ f1s1t3e4 - f1s1t5e4 + f2s1t3e4 - f2s1t5e4 <= 0 + 10000000 t3e4 - 10000000 t5e4;
0+ f1s1t4e4 - f1s1t5e4 + f2s1t4e4 - f2s1t5e4 <= 0 + 10000000 t4e4 - 10000000 t5e4;
0+ f2s2t1e4 - f2s2t2e4 <= 0 + 10000000 t1e4 - 10000000 t2e4;

/* arrival shaping constraints */
0+f1s0t6e4 - f1s0t7e4+f4s0t6e4 - f4s0t7e4<= 0 + 10000000t6e4 - 10000000t7e4;
0+f1s0t6e4 - f1s0t8e4+f4s0t6e4 - f4s0t8e4<= 0 + 10000000t6e4 - 10000000t8e4;
0+f1s0t6e4 - f1s0t9e4+f4s0t6e4 - f4s0t9e4<= 0 + 10000000t6e4 - 10000000t9e4;
0+f1s0t7e4 - f1s0t8e4+f4s0t7e4 - f4s0t8e4<= 0 + 10000000t7e4 - 10000000t8e4;
0+f1s0t7e4 - f1s0t9e4+f4s0t7e4 - f4s0t9e4<= 0 + 10000000t7e4 - 10000000t9e4;
0+f1s0t8e4 - f1s0t9e4+f4s0t8e4 - f4s0t9e4<= 0 + 10000000t8e4 - 10000000t9e4;

/* TFA delay constraints */
t3e4 - t6e4 <= 2.01148e-05;
t4e4 - t7e4 <= 2.01148e-05;
t5e4 - t8e4 <= 2.01148e-05;
t1e4 - t3e4 <= 1.98534e-05;
t2e4 - t4e4 <= 1.98534e-05;
t0e4 - t1e4 <= 2.03767e-05;

/* SFA delay constraints */

/* the x burst constraints*/
x4 = f3s1t0e4 - f3s3t0e4;
f3s1t0e4 - f3s1t3e4 <= x3 + 2400000.0t0e4 - 2400000.0t3e4;
f3s1t0e4 - f3s1t4e4 <= x3 + 2400000.0t0e4 - 2400000.0t4e4;
f3s1t0e4 - f3s1t5e4 <= x3 + 2400000.0t0e4 - 2400000.0t5e4;
