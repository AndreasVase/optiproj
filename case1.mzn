I = 5;
J = 10;
C = 3073;
CV = 2;
CC = 4;
O_i = [36, 66, 61, 67, 67];
V_i = [0, 1, 1, 1, 1];
D_ij = 
[|249, 270, 273, 208, 231, 172, 260, 281, 272, 218
|68, 129, 127, 38, 95, 79, 89, 118, 98, 63
|235, 250, 253, 197, 213, 157, 244, 263, 256, 204
|90, 151, 149, 75, 125, 119, 109, 135, 115, 95
|111, 140, 142, 71, 97, 35, 123, 146, 136, 80
|];
E_ij = 
[|409, 441, 446, 348, 382, 294, 426, 457, 445, 363
|168, 260, 257, 123, 209, 185, 200, 243, 214, 160
|413, 437, 441, 356, 380, 297, 427, 455, 446, 367
|202, 294, 290, 180, 255, 245, 231, 270, 239, 210
|233, 277, 280, 174, 213, 119, 252, 286, 271, 187
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