I = 8;
J = 15;
C = 3073;
CV = 2;
CC = 7;
O_i = [63, 30, 27, 57, 36, 20, 68, 57];
V_i = [1, 0, 1, 1, 0, 1, 0, 1];
D_ij = 
[|174, 158, 81, 106, 196, 149, 195, 169, 164, 107, 173, 128, 174, 115, 204
|171, 159, 227, 237, 242, 174, 198, 214, 218, 169, 267, 179, 252, 244, 265
|219, 213, 114, 115, 193, 196, 222, 186, 178, 175, 148, 179, 162, 114, 186
|54, 73, 158, 145, 70, 78, 34, 69, 77, 121, 117, 98, 99, 143, 90
|429, 446, 452, 428, 363, 437, 398, 395, 395, 469, 363, 445, 369, 418, 344
|147, 129, 154, 170, 210, 136, 179, 178, 178, 109, 219, 129, 208, 180, 230
|349, 340, 237, 246, 331, 324, 357, 321, 313, 294, 286, 304, 300, 247, 325
|81, 82, 183, 180, 145, 99, 97, 126, 132, 124, 183, 116, 165, 184, 168
|];
E_ij = 
[|324, 301, 185, 222, 357, 286, 356, 317, 309, 224, 322, 255, 325, 235, 369
|286, 268, 371, 386, 393, 291, 327, 351, 357, 284, 431, 298, 408, 397, 427
|356, 347, 198, 200, 317, 322, 361, 306, 295, 290, 249, 295, 271, 198, 307
|138, 166, 295, 274, 163, 174, 108, 161, 172, 239, 233, 205, 205, 272, 192
|679, 705, 715, 678, 580, 692, 633, 629, 629, 739, 581, 704, 589, 664, 552
|241, 213, 251, 276, 335, 224, 288, 287, 288, 183, 348, 214, 333, 290, 365
|592, 578, 424, 437, 565, 555, 603, 550, 538, 510, 497, 525, 518, 439, 555
|179, 180, 332, 328, 275, 206, 203, 246, 256, 244, 331, 232, 305, 333, 309
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