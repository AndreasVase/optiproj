I = 7;
J = 7;
C = 2955;
CV = 2;
CC = 1;
O_i = [34, 56, 68, 61, 31, 37, 69];
V_i = [1, 1, 0, 1, 1, 1, 1];
D_ij = 
[|267, 242, 258, 237, 284, 201, 246
|131, 164, 146, 208, 120, 150, 186
|267, 233, 252, 192, 282, 279, 214
|140, 141, 135, 130, 133, 235, 125
|240, 207, 227, 180, 257, 218, 198
|123, 89, 109, 67, 139, 126, 81
|135, 169, 149, 204, 118, 197, 183
|];
E_ij = 
[|435, 397, 421, 389, 460, 336, 403
|252, 302, 276, 369, 236, 281, 335
|469, 417, 446, 356, 491, 486, 390
|271, 272, 264, 257, 261, 413, 249
|392, 342, 371, 302, 417, 358, 329
|221, 170, 200, 137, 246, 226, 159
|272, 323, 293, 376, 247, 364, 343
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