#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>

unsigned long A = 0;
int N, M;

void* dretva(void* arg){
    int a = *((int*) arg);
    for(a = 0; a < M; a++){
        A++;
    }
  
}

int main(int argc, char *argv[]){
    N = atoi(argv[1]);
    M = atoi(argv[2]);
    int arg[N];
    pthread_t ID[N];

    for(int i = 0; i < N; i++){
        arg[i] = 0;
        if(pthread_create(&ID[i],NULL,dretva,&arg[i])){
            printf("Greska pri stvaranju dretvi!");
            exit(1);
        }
    }
    for(int i = 0; i < N; i++){
        pthread_join(ID[i], NULL);
    }
    printf("A=%lu\n",A);
    return 0;
}