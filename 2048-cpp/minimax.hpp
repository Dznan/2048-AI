#include "game2048.hpp"
#include "score.hpp"

#ifndef MINIMAX
#define MINIMAX 
#define MYMAX 1e10

double myMin(game2048 &env, int search_deepth, int& dir);

double myMax(game2048 &env, int search_deepth, int& dir);

int myFind(game2048 env);

#endif
