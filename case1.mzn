I = 5;
J = 8;
C = 3992;
CV = 2;
CC = 4;
O_i = [49, 27, 42, 21, 22];
V_i = [1, 1, 1, 1, 0];
D_ij = 
[|222, 123, 226, 212, 192, 258, 202, 231
|169, 199, 187, 131, 165, 97, 167, 93
|167, 247, 179, 154, 184, 104, 179, 130
|210, 214, 230, 169, 199, 148, 204, 134
|381, 466, 388, 374, 402, 324, 396, 350
|];
E_ij = 
[|382, 233, 389, 367, 338, 436, 352, 396
|280, 325, 308, 224, 275, 173, 278, 167
|293, 412, 310, 273, 319, 198, 311, 237
|337, 342, 366, 275, 320, 243, 327, 223
|594, 722, 605, 583, 625, 508, 616, 547
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