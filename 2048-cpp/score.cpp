#include "game2048.cpp"
#ifndef SCORE
#define SCORE
int find_near_tile(game2048 &env, int x, int y, int d){
    if (d == 0){	//up
    	for(int i = x - 1; i > -1; i--){
    		if(env.board[i][y] != 0){
    			return env.board[i][y];
			}
		}
	}
    if (d == 1){	//down
    	for(int i = x + 1; i < 4; i++){
    		if(env.board[i][y] != 0){
    			return env.board[i][y];
			}
		}
	}
	if (d == 2){	//left
    	for(int i = y - 1; i > -1; i--){
    		if(env.board[x][i] != 0){
    			return env.board[x][i];
			}
		}
	}
	if (d == 3){	//right
    	for(int i = y + 1; i < 4; i++){
    		if(env.board[x][i] != 0){
    			return env.board[x][i];
			}
		}
	}
    return 0;
}

int smoothness(game2048 &env){
	int res = 0;
	for(int i = 0; i < 4; ++i){
		for(int j = 0; j < 4; ++j){
			game2048::tile_type a = env.board[i][j];
			if(a == 0)continue;
			for(int d = 0; d < 4; ++d){
				int b = find_near_tile(env, i, j, d);
				res -= abs(a - b);
			}
		}
	}
	return res;
}

int tonicity(game2048& env){
	int t = 0;
	int a = 0, b = 0;
	for(int i = 0; i < 4; ++i){
		for(int j = 0; j < 4; ++j){
			game2048::tile_type c = env.board[i][j];
			if(c == 0)continue;
			int n = find_near_tile(env, i, j, 3);	//right
			if(n){
				if(c > n)
					a += c - n;
				if(c < n)
					b += n - c;
			}
		}
	}
	t += abs(a - b);
	a = 0;b = 0;
	for(int j = 0; j < 4; ++j){
		for(int i = 0; i < 4; ++i){
			game2048::tile_type c = env.board[i][j];
			if(c == 0)continue;
			int n = find_near_tile(env, i, j, 1);	//DOWN
			if(n){
				if(c > n)
					a += c - n;
				if(c < n)
					b += n - c;
			}
		}
	}
	t += abs(a - b);
	return t; 
}

double heuristic_evaluation_function(game2048 &env){
	return tonicity(env);
	int max_tile = 0, empty_tiles = 0;
	//int tonic = tonicity(env);
	//int smooth = smoothness(env);
	for(int i = 0; i < 4; ++i){
		for(int j = 0; j < 4; ++j){
			if(env.board[i][j] == 0)
				empty_tiles++;
			else if(env.board[i][j] > max_tile)
				max_tile = env.board[i][j];
		}
	}
	return max_tile + empty_tiles;
}

#endif