#include <bits/stdc++.h>
using namespace std;

#ifndef GAME2048
#define GAME2048
class game2048{
	
public:
	
	typedef unsigned char tile_type;
	
	tile_type board[4][4];
	
	int score;
	
	
public:
	
	game2048(){
		init();
	} 
	
	game2048(const game2048 &o){
		score = o.score;
		for(int i = 0; i < 16; ++i)
			board[i/4][i%4] = o.board[i/4][i%4];
	}
	
	game2048& operator=(const game2048 &o){
		score = o.score;
		for(int i = 0; i < 16; ++i)
			board[i/4][i%4] = o.board[i/4][i%4];
		return *this;
	} 
	
	~game2048(){}
	
public:
	
	void print(){
		printf("---------------------------------\n");
		for(int i = 0; i < 4; ++i){
			for(int j = 0; j < 4; ++j)
				printf("%6d", (board[i][j]));
			printf("\n");
		}
	}
	
	void add_random_tile(){
		tile_type tile = (abs(rand()) % 2) + 1;
		int pos[16], counter = 0;
		for(int i = 0; i < 16; ++i){
			if(board[i/4][i%4] == 0)
				pos[counter++] = i;
		}
		int selected = pos[abs(rand())%counter];
		board[selected/4][selected%4] = tile;
	}
	
	void init(){
		score = 0;
		for(int i = 0; i < 16; ++i){
			board[i/4][i%4] = 0;
		}
		add_random_tile();
		add_random_tile();
	}
	
	
	
	void move_right(){
		for(int i = 0; i < 4; ++i){
			int top = 0, now = 3;
			for(int j = 3; j > -1; j--){
				tile_type t = board[i][j];
				if(t){
					if(top == 0){
						top = t;
					}
					else if(t == top){
						board[i][now--] = top + 1;
						top = 0;
					}
					else{
						board[i][now--] = top;
						top = t;
					}
				}
			}
			board[i][now--] = top;
			while(now > -1)
				board[i][now--] = 0;
		}
	}
	
	void move_left(){
		for(int i = 0; i < 4; ++i){
			int top = 0, now = 0;
			for(int j = 0; j < 4; j++){
				tile_type t = board[i][j];
				if(t){
					if(top == 0){
						top = t;
					}
					else if(t == top){
						board[i][now++] = top + 1;
						top = 0;
					}
					else{
						board[i][now++] = top;
						top = t;
					}
				}
			}
			board[i][now++] = top;
			while(now < 4)
				board[i][now++] = 0;
		}
	}
	
	void move_up(){
		for(int j = 0; j < 4; ++j){
			int top = 0, now = 0;
			for(int i = 0; i < 4; i++){
				tile_type t = board[i][j];
				if(t){
					if(top == 0){
						top = t;
					}
					else if(t == top){
						board[now++][j] = top + 1;
						top = 0;
					}
					else{
						board[now++][j] = top;
						top = t;
					}
				}
			}
			board[now++][j] = top;
			while(now < 4)
				board[now++][j] = 0;
		}
	}
	
	void move_down(){
		for(int j = 0; j < 4; ++j){
			int top = 0, now = 3;
			for(int i = 3; i > -1; i--){
				tile_type t = board[i][j];
				if(t){
					if(top == 0){
						top = t;
					}
					else if(t == top){
						board[now--][j] = top + 1;
						top = 0;
					}
					else{
						board[now--][j] = top;
						top = t;
					}
				}
			}
			board[now--][j] = top;
			while(now > -1)
				board[now--][j] = 0;
		}
	}
	
	void move(int direction){
		switch(direction){
			case 0:return move_up();
			case 1:return move_down();
			case 2:return move_left();
			case 3:return move_right();
			default:exit(-1);
		}
	}
	
	bool can_move_up(){
		for(int j = 0; j < 4; ++j){
			int top = -1;
			bool emp = false;
			for(int i = 0; i < 4; i++){
				tile_type t = board[i][j];
				if(t){
					if(emp || (t == top)){
						return true;
					}
					else{
						top = t;
					}
				}
				else {
					emp = true;
				}
			}
		}
		return false;
	}
	
	bool can_move_down(){
		for(int j = 0; j < 4; ++j){
			int top = -1;
			bool emp = false;
			for(int i = 3; i > -1; i--){
				tile_type t = board[i][j];
				if(t){
					if(emp || (t == top)){
						return true;
					}
					else{
						top = t;
					}
				}
				else {
					emp = true;
				}
			}
		}
		return false;
	}
	
	bool can_move_left(){
		for(int i = 0; i < 4; ++i){
			int top = -1;
			bool emp = false;
			for(int j = 0; j < 4; j++){
				tile_type t = board[i][j];
				if(t){
					if(emp || (t == top)){
						return true;
					}
					else{
						top = t;
					}
				}
				else {
					emp = true;
				}
			}
		}
		return false;
	}
	
	bool can_move_right(){
		for(int i = 0; i < 4; ++i){
			int top = -1;
			bool emp = false;
			for(int j = 3; j > -1; j--){
				tile_type t = board[i][j];
				if(t){
					if(emp || (t == top)){
						return true;
					}
					else{
						top = t;
					}
				}
				else {
					emp = true;
				}
			}
		}
		return false;
	}
	
	int action_space(){
        int actions = 0;
        if (can_move_up())
			actions |= 0b1;
		if (can_move_down())
			actions |= 0b10;
		if (can_move_left())
			actions |= 0b100;
		if (can_move_right())
			actions |= 0b1000;
		return actions;
	}
	
	bool is_terminal(){
		return action_space() == 0;
	}	
	
	
}; 

#endif


