I = 12;
J = 13;
C = 2266;
CV = 3;
CC = 4;
O_i = [20, 34, 63, 64, 24, 56, 46, 60, 60, 59, 64, 38];
V_i = [1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0];
D_ij = 
[|122, 220, 200, 203, 135, 219, 139, 185, 133, 153, 170, 123, 154
|225, 128, 159, 144, 211, 133, 208, 192, 213, 207, 179, 229, 203
|170, 115, 89, 116, 163, 78, 157, 106, 167, 135, 122, 165, 133
|214, 304, 248, 284, 230, 274, 228, 212, 232, 204, 238, 197, 210
|343, 241, 292, 261, 327, 265, 325, 328, 327, 337, 305, 352, 331
|358, 442, 440, 429, 367, 455, 373, 430, 364, 397, 408, 365, 397
|159, 251, 198, 231, 174, 225, 173, 165, 177, 152, 186, 142, 158
|190, 259, 194, 241, 203, 220, 200, 156, 208, 163, 196, 170, 169
|84, 154, 162, 142, 87, 171, 93, 165, 82, 130, 128, 101, 128
|175, 231, 250, 222, 176, 256, 182, 255, 170, 220, 216, 191, 218
|127, 228, 192, 209, 143, 216, 144, 169, 143, 143, 169, 119, 146
|235, 277, 208, 261, 244, 230, 239, 174, 250, 196, 223, 214, 202
|];
E_ij = 
[|203, 351, 320, 324, 223, 349, 228, 298, 220, 249, 276, 204, 252
|372, 226, 272, 250, 351, 234, 346, 322, 354, 345, 303, 378, 338
|319, 236, 196, 237, 307, 181, 299, 222, 314, 265, 246, 310, 262
|385, 520, 436, 490, 409, 476, 407, 383, 413, 371, 422, 360, 380
|538, 386, 462, 416, 515, 422, 512, 516, 515, 529, 481, 553, 521
|594, 719, 716, 700, 607, 738, 615, 702, 602, 651, 668, 604, 652
|284, 423, 344, 393, 308, 383, 306, 294, 312, 275, 325, 259, 283
|346, 449, 351, 421, 365, 390, 360, 295, 372, 304, 355, 315, 314
|187, 292, 303, 273, 191, 317, 199, 308, 183, 256, 252, 212, 252
|321, 405, 434, 392, 323, 444, 332, 442, 315, 390, 384, 345, 386
|255, 407, 353, 378, 278, 388, 281, 318, 279, 278, 317, 243, 284
|391, 453, 351, 430, 405, 383, 397, 300, 413, 332, 373, 360, 341
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