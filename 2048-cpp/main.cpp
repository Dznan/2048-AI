#include "game2048.hpp"
#include "minimax.hpp"
int main(){
	srand(time(0));
	//for (int i = 1; i <= 10; ++i) {
		game2048 env;
		env.print();
		bool MOVE = true;
		while (!env.is_terminal()) {
			if (MOVE) {
				printf("MOVE ");
				int selected = myFind(env);//action[abs(rand())%m];
				env.move(selected);
				switch (selected) {
				case 0:printf("UP\n"); break;
				case 1:printf("DOWN\n"); break;
				case 2:printf("LEFT\n"); break;
				case 3:printf("RIGHT\n"); break;
				default:exit(-1);
				}
			}
			else {
				printf("ADD TILE\n");
				env.add_random_tile();
			}
			env.print();

			MOVE = !MOVE;
		}
		//system("pause");
		//printf("times : %d   max_tile : %d\n", i, (1 << env.max_tile()));
	//}
	return 0;
}
