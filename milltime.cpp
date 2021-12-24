#include <sys/time.h>
#include <stdio.h>

int main(){
	struct timeval stop, start;
	double a;
	
	gettimeofday(&start, NULL);
	for(int j = 0; j < 100000 ; j++){
		for(int i = 0; i < 100 ; i++){
			continue;
		}
		gettimeofday(&stop, NULL);
		a = (stop.tv_sec - start.tv_sec) * 1000000 + (stop.tv_usec - start.tv_usec);
		a /= 1000000;
		printf("took %lf us\n", a); 
	}
}