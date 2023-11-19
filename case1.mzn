I = 4;
J = 20;
C = 5;
CV = 1879;
CC = 1217;
O_i = [55, 61, 70, 61];
V_i = [0, 1, 1, 1];
D_ij = 
[|330, 327, 379, 336, 242, 300, 365, 310, 381, 323, 359, 351, 344, 287, 310, 333, 325, 366, 369, 325
|248, 257, 214, 262, 347, 285, 221, 279, 214, 261, 218, 270, 243, 293, 282, 258, 254, 228, 217, 256
|220, 194, 167, 160, 220, 199, 185, 186, 163, 196, 229, 125, 181, 216, 180, 174, 210, 165, 182, 205
|209, 212, 265, 228, 139, 187, 248, 199, 268, 208, 237, 250, 230, 172, 201, 221, 207, 253, 253, 207
|];
E_ij = 
[|550, 546, 623, 559, 418, 505, 602, 520, 626, 539, 593, 582, 572, 486, 520, 554, 543, 604, 609, 542
|434, 446, 382, 454, 582, 489, 392, 480, 383, 452, 389, 466, 425, 501, 484, 449, 443, 403, 387, 445
|401, 362, 321, 311, 400, 368, 348, 349, 314, 364, 414, 258, 342, 394, 340, 331, 386, 317, 343, 378
|375, 379, 459, 403, 270, 342, 434, 359, 463, 373, 416, 436, 407, 319, 362, 393, 371, 441, 441, 372
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