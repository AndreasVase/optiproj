I = 6;
J = 8;
C = 3325;
CV = 2;
CC = 4;
O_i = [70, 30, 52, 56, 67, 47];
V_i = [0, 0, 1, 0, 0, 1];
D_ij = 
[|325, 306, 262, 362, 280, 349, 326, 348
|296, 318, 291, 260, 294, 346, 225, 361
|170, 184, 150, 155, 155, 221, 109, 233
|295, 287, 238, 314, 254, 333, 271, 337
|325, 296, 272, 378, 285, 325, 361, 316
|180, 148, 151, 238, 155, 161, 239, 148
|];
E_ij = 
[|558, 530, 463, 613, 490, 594, 560, 592
|475, 507, 467, 420, 471, 549, 367, 571
|307, 328, 277, 285, 285, 383, 216, 402
|499, 487, 413, 528, 438, 556, 463, 562
|555, 511, 475, 635, 495, 555, 608, 541
|317, 270, 274, 404, 280, 289, 406, 269
|];

% Define sets I and J
int: I;
int: J;

int: C; % Cost of installing a warehouse in all zones
int: CV; % Capacity in green zone
int: CC; % Capacity in blue zone

array[1..I] of int: O_i; % Emissions per operation for each warehouse i
array[1..I, 1..J] of int: D_ij; % Distance between warehouse i and store j
array[1..I, 1..J] of int: E_ij; % Transportation emissions
array[1..I] of int: V_i; % 1 if warehouse i is in the green zone, 0 if in the blue zone

% Define decision variables
array[1..I, 1..J] of var 0..1: X; % 1 if warehouse i supplies store j, 0 otherwise
array[1..I] of var 0..1: Y;

% Define constraints

% Add the constraint to ensure Y_i is 1 if the warehouse I supplies at least one store
constraint forall(i in 1..I)(
  sum(j in 1..J)(X[i,j]) > 0 -> Y[i] == 1
);

% Emissions constraint
constraint sum(i in 1..I, j in 1..J)(E_ij[i, j] * X[i, j]) + sum(i in 1..I)(O_i[i] * Y[i]) <= 500 * J;

% Assignment constraint
constraint forall(j in 1..J)(sum(i in 1..I)(X[i, j]) == 1);

% Green zone capacity constraint
constraint forall(i in 1..I)(sum(j in 1..J)(X[i, j] * V_i[i]) <= CV);

% Blue zone capacity constraint
constraint forall(i in 1..I)(sum(j in 1..J)(X[i, j] * (1 - V_i[i])) <= CC);

% Solve the optimization problem using a solver
% Define the objective function
solve minimize sum(i in 1..I, j in 1..J)(1.25 * D_ij[i, j] * X[i, j]) + sum(i in 1..I)(C * Y[i]);

output ["Solution:", ""];
output ["X = \n", show2d(X), ";"];
output ["\n"];
output ["Y = ", show(Y), ";"];
output ["\n"];
output ["FO = ", show(sum(i in 1..I, j in 1..J)(1.25 * D_ij[i, j] * X[i, j]) + sum(i in 1..I)(C * Y[i])), "\n"];