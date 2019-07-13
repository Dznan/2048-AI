#include "minimax.hpp"

int my_search_deepth = 5;

double myMax(game2048 &env, int search_deepth, int& dir){
	if(search_deepth < 0) return heuristic_evaluation_function(env);
	bool f = (search_deepth == my_search_deepth);
	double now_alpha = 0, score = 0;
	int action = env.action_space();
	for(int i = 0; i < 4; ++i){
		if(action & (1 << i)){
			game2048 tmp = env;
			tmp.move(i);
			score = myMin(tmp, search_deepth - 1, dir);
			if(score > now_alpha){
				now_alpha = score;
				if(f){
					dir = i; 
				}
			}
			if (f && (score == now_alpha) && (rand() % 2)) {
					dir = i;
			}
		}
	}
	return now_alpha;
}

double myMin(game2048 &env, int search_deepth,int& dir){
	if(search_deepth < 0) return heuristic_evaluation_function(env);
	double score = 0;
	int count = 0;
	for(int i = 0; i < 4; ++i){
		for(int j = 0; j < 4; ++j){
			if(env.board[i][j] == 0){
				count += 2;
				env.board[i][j] = 1;
				score += myMax(env, search_deepth - 1, dir);
				
				env.board[i][j] = 2;
				score += myMax(env, search_deepth - 1, dir);
				
				env.board[i][j] = 0;
			}
		}
	}
	return score / count;
}

int myFind(game2048 env){
	for(int j = 1; j < 4; ++j){
		if(env.board[0][j] >= env.board[0][j-1]) break;
		else if(env.board[0][j] != 0 && env.board[0][j] == env.board[1][j])
			return 0;//UP deal with special situation
	}




	int res = -1;
	int emp_tiles = env.empty_tiles();
	int max_tile = env.max_tile();
	if (emp_tiles > 10) {
		if (max_tile < 7) my_search_deepth = 2;
		else my_search_deepth = 4;
	}
	else if (emp_tiles >= 6) my_search_deepth = 4;
	else my_search_deepth = 6;
	double score = myMax(env, my_search_deepth, res);
	if (res == -1) {
		int action = env.action_space();
		if (action & 1)res = 0;
		else if (action & 4) res = 2;
		else if (action & 8) res = 3;
		else res = 1;
	}
	//printf("actions : %d    move:%d   score:%f\n", env.action_space(), res, score);
	return res;
}
