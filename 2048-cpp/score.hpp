#include "game2048.hpp"

#ifndef SCORE
#define SCORE

int find_near_tile(game2048 &env, int x, int y, int d);

int smoothness(game2048 &env);

int tonicity(game2048& env);

double heuristic_evaluation_function(game2048 &env);

#endif
