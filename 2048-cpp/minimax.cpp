#include "minimax.hpp"

int my_search_deepth = 9;

double myMax(game2048 &env, int search_deepth, double alpha, double beta, int& dir){
	if(search_deepth < 0) return heuristic_evaluation_function(env);
	bool f = (search_deepth == my_search_deepth);
	double now_alpha = -MYMAX, score;
	int action = env.action_space();
	for(int i = 0; i < 4; ++i){
		if(action & (1 << i)){
			game2048 tmp = env;
			tmp.move(i);
			
			score = myMin(tmp, search_deepth - 1, max(alpha, now_alpha), beta, dir);
			if(score > now_alpha){
				now_alpha = score;
				if(f){
					dir = i; 
				}
			}
			if (f && (score == now_alpha) && (rand() % 2)) {
					dir = i;
			}
			if(score >= beta) return score;
		}	
	}
	return now_alpha;
}

double myMin(game2048 &env, int search_deepth, double alpha, double beta, int& dir){
	if(search_deepth < 0) return heuristic_evaluation_function(env);
	double score, now_beta = MYMAX;
	for(int i = 0; i < 4; ++i){
		for(int j = 0; j < 4; ++j){
			if(env.board[i][j] == 0){
				env.board[i][j] = abs(rand()) % 2 + 1;
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

int myFind(game2048 env){
	int res = -1;
	int emp_tiles = env.empty_tiles();
	if (emp_tiles > 11) my_search_deepth = 1;
	if (emp_tiles > 7) my_search_deepth = 10;
	else my_search_deepth = emp_tiles;
	double score = myMax(env, my_search_deepth, INT_MIN, INT_MAX, res);
	if (score == -MYMAX) {
		int action = env.action_space();
		if (action & 1)res = 0;
		else if (action & 4) res = 2;
		else if (action & 8) res =3;
		else res = 1;
	}
	//printf("actions : %d    move:%d   score:%f\n", env.action_space(), res, score);
	return res;
}
