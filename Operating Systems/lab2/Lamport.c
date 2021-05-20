#include <stdio.h>
#include <stdlib.h>
#include <stdatomic.h>
#include <pthread.h>
#include <unistd.h>

atomic_int n, m, A;
atomic_int *ULAZ, *BROJ;

void ulazakUKO(int i){
    ULAZ[i] = 1;
    int max = BROJ[0];
    for(int j = 0; j<n-1;j++){
        if(BROJ[j] > max) max = BROJ[j];
    }
    BROJ[i] = max + 1;
    ULAZ[i] = 0;

    for(int j = 0; j<n-1;j++){
        while(ULAZ[j] != 0);
        while(BROJ[j] != 0 && (BROJ[j] < BROJ[i] || (BROJ[j] == BROJ[i] && j<i)));
    }
}

void izlazakIzKO(int i){
    BROJ[i] = 0;
}

void* dretva(void* arg){
    int rbr = *((int*) arg);
    for(int i = 0; i < m; i++){
        ulazakUKO(rbr);
        A++;
        izlazakIzKO(rbr);
    }
    printf("Gotova dretva %d, trenutacno stanje broja a je %d\n",rbr,A);
}

int main(int argc, char *argv[]){
    n = atoi(argv[1]);
    m = atoi(argv[2]);
    int arg[n];
    pthread_t ID[n];
    ULAZ = malloc(sizeof(int) * n);
    BROJ = malloc(sizeof(int) * n);

    for(int i = 0; i < n; i++){
        arg[i] = i;
        if(pthread_create(&ID[i],NULL,dretva,&arg[i])){
            printf("Greska pri stvaranju dretvi!");
            exit(1);
        }
    }

    for(int i = 0; i < n; i++){
        pthread_join(ID[i], NULL);
    }

    printf("A=%d",A);
    return 0;
}