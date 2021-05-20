#define _XOPEN_SOURCE 500
#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

pthread_mutex_t monitor;
pthread_cond_t red[5];
int vilica[5];
char filozof[5];

void* dretva(void* arg){
    int n = *((int*) arg);
    do{
        // misliti
        sleep(3);
        // jesti
        pthread_mutex_lock(&monitor);
            filozof[n] = 'o';
            while(vilica[n] == 0 || vilica[(n+1) % 5] == 0){
                pthread_cond_wait(&red[n], &monitor);
            }
            vilica[n] = vilica[(n + 1) % 5] = 0;
            filozof[n] = 'X';
            for(int i = 0; i < 5; i++){
                printf("%c ", filozof[i]);
            }
            printf("(%d)\n", n+1);
        pthread_mutex_unlock(&monitor);

        sleep(2);

        pthread_mutex_lock(&monitor);
            filozof[n] = 'O';
            vilica[n] = vilica[(n+1) % 5] = 1;
            pthread_cond_signal(&red[(n - 1) % 5]);
            pthread_cond_signal(&red[(n + 1) % 5]);
            for(int i = 0; i < 5; i++){
                printf("%c ", filozof[i]);
            }
            printf("(%d)\n", n+1);
        pthread_mutex_unlock(&monitor);
    }while (1);
}

void izadi(int sig){
    pthread_mutex_destroy(&monitor);
    pthread_cond_destroy(&red[0]);
    pthread_cond_destroy(&red[1]);
    pthread_cond_destroy(&red[2]);
    pthread_cond_destroy(&red[3]);
    pthread_cond_destroy(&red[4]);
    exit(0);
}

int main(){
    sigset(SIGINT,izadi);
    pthread_mutex_init(&monitor, NULL);
    pthread_cond_init(&red[0], NULL);
    pthread_cond_init(&red[1], NULL);
    pthread_cond_init(&red[2], NULL);
    pthread_cond_init(&red[3], NULL);
    pthread_cond_init(&red[4], NULL);
    pthread_t threadId[5];
    int id[5];

    for(int i = 0; i<5; i++){
        id[i] = i;
        filozof[i] = '0';
        vilica[i] = 1;
        if(pthread_create(&threadId[i],NULL,dretva,&id[i])){
            printf("Greska pri stvaranju filozofa!\n");
            exit(1);
        }
    }
    for(int i = 0; i < 5; i++){
        pthread_join(threadId[i], NULL);
    }
    return 0;
}