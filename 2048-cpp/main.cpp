#include "game2048.cpp"
#include "minimax.cpp"
int main(){
	srand(time(0));
	game2048 env;
	env.print();
	bool MOVE = true;
	while(!env.is_terminal()){
		if (MOVE){
			printf("MOVE ");
			int actions = env.action_space();
			int action[4], m = 0;
			for(int i = 0; i < 4; ++i)
				if(actions & (1 << i))
					action[m++] = i;
			int selected = myFind(env);//action[abs(rand())%m];
			env.move(selected);
			switch(selected){
				case 0:printf("UP\n");break;
				case 1:printf("DOWN\n");break;
				case 2:printf("LEFT\n");break;
				case 3:printf("RIGHT\n");break;
				default:exit(-1); 
			}
		}
        else{ 
    		printf("ADD TILE\n");
			env.add_random_tile();
       	} 
		env.print();
       	
       	MOVE = !MOVE;
	}
	system("pause");
	return 0;
}
