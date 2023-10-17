I = 12;
J = 12;
C = 3073;
CV = 2;
CC = 5;
O_i = [36, 66, 61, 67, 67, 34, 47, 63, 40, 61, 36, 61];
V_i = [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1];
D_ij = 
[|260, 223, 260, 207, 202, 253, 234, 227, 273, 187, 235, 272
|60, 59, 103, 41, 35, 85, 16, 23, 95, 65, 90, 121
|247, 209, 243, 196, 192, 237, 226, 218, 257, 173, 218, 253
|74, 90, 125, 78, 73, 107, 40, 53, 110, 103, 118, 142
|122, 85, 125, 71, 68, 116, 103, 94, 135, 49, 100, 139
|183, 143, 159, 142, 144, 160, 181, 168, 179, 115, 138, 165
|236, 268, 284, 263, 260, 270, 224, 237, 262, 290, 289, 295
|235, 197, 207, 197, 199, 211, 235, 223, 228, 170, 188, 210
|366, 357, 315, 379, 389, 333, 404, 393, 330, 368, 326, 298
|168, 157, 207, 133, 123, 189, 124, 129, 202, 141, 188, 224
|302, 262, 287, 253, 252, 285, 287, 277, 305, 228, 264, 294
|207, 178, 162, 191, 198, 174, 227, 214, 185, 169, 154, 155
|];
E_ij = 
[|426, 371, 427, 347, 340, 416, 388, 377, 445, 317, 389, 444
|157, 154, 221, 127, 118, 194, 91, 101, 209, 163, 201, 248
|432, 375, 426, 355, 350, 417, 401, 388, 447, 321, 388, 441
|178, 202, 255, 184, 177, 227, 127, 147, 233, 222, 244, 280
|250, 195, 255, 173, 169, 241, 222, 208, 270, 141, 217, 276
|308, 249, 273, 248, 251, 275, 305, 287, 302, 207, 241, 281
|401, 450, 473, 442, 438, 452, 384, 403, 440, 482, 481, 490
|416, 359, 374, 359, 362, 379, 416, 398, 405, 318, 345, 378
|590, 576, 513, 609, 624, 540, 647, 630, 536, 592, 529, 487
|313, 297, 371, 261, 246, 345, 247, 255, 364, 273, 343, 398
|489, 430, 467, 416, 414, 464, 467, 452, 493, 379, 432, 477
|372, 328, 304, 348, 358, 322, 402, 382, 338, 315, 293, 294
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