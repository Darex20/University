#define _XOPEN_SOURCE 500
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <signal.h>
#include <stdatomic.h>


int *A, N, M, ID;

void proces(int i){
    for(int j=0;j<M;j++){
        (*A)++;
    }
    printf("Proces %d gotov, vrijednost A je %d\n",i,*A);
}

void brisi(int sig){
    shmdt((char*) A);
    shmctl(ID, IPC_RMID, NULL);
}

int main(int argc, char *argv[]){
    N = atoi(argv[1]);
    M = atoi(argv[2]);

    sigset(SIGINT,brisi);
    ID = shmget(IPC_PRIVATE, sizeof(int), 0600);
    if(ID == -1){
        exit(1);
    }
    A = (int*) shmat(ID, NULL, 0);
    *A = 0;

    for(int i = 0; i<N; i++){
        switch(fork()){
            case -1:
                printf("Proces %d se nije uspio napravit\n", i);
                exit(1);
            case 0:
                proces(i);
                exit(0);
            default:
                break;
        }
    }

    for(int j = 0; j<N; j++){
        wait(NULL);
    }

    printf("A=%d",*A);
    shmdt((char*) A);
    shmctl(ID, IPC_RMID, NULL);
    return 0;
}