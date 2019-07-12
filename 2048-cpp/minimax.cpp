#include "game2048.cpp"
#include "score.cpp"
#ifndef MINIMAX
#define MINIMAX 
#define MYMAX 1e10

const int my_search_deepth = 9;

double myMin(game2048 &env, int search_deepth, double alpha, double beta, int& dir);
double myMax(game2048 &env, int search_deepth, double alpha, double beta, int& dir){
	if(search_deepth < 0) return heuristic_evaluation_function(env);
	double now_alpha = -MYMAX, score;
	int action = env.action_space();
	for(int i = 0; i < 4; ++i){
		if(action & (1 << i)){
			game2048 tmp = env;
			tmp.move(i);
			score = myMin(tmp, search_deepth - 1, max(alpha, now_alpha), beta, dir);
			if(score >= now_alpha){
				now_alpha = score;
				if(search_deepth == my_search_deepth){
					dir = i; 
				}
			}
			if(score >= beta) return score;
		}	
	}
	return now_alpha;
}

double myMin(game2048 &env, int search_deepth, double alpha, double beta, int& dir){
	if(env.is_terminal()) return 0;
	if(search_deepth < 0) return heuristic_evaluation_function(env);
	double score, now_beta = MYMAX;
	for(int i = 0; i < 4; ++i){
		for(int j = 0; j < 4; ++j){
			if(env.board[i][j] == 0){
				env.board[i][j] = 1;
				score = myMax(env, search_deepth - 1, alpha, min(beta, now_beta), dir);
				if(score < now_beta)
					now_beta = score;
				if(score <= alpha) {
					env.board[i][j] = 0;
					return score;
				}
				env.board[i][j] = 2;
				score = myMax(env, search_deepth - 1, alpha, min(beta, now_beta), dir);
				if(score < now_beta)
					now_beta = score;
				if(score <= alpha) {
					env.board[i][j] = 0;
					return score;
				}
				env.board[i][j] = 0;
			}
		}
	}
	return now_beta;
}

int myFind(game2048& env){
	int res;
	myMax(env, my_search_deepth, INT_MIN, INT_MAX, res);
	return res;
}
#endif
