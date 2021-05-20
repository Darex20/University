#define _XOPEN_SOURCE 500
#include <stdio.h>
#include <semaphore.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/shm.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <time.h>

#define BR_PROCESA 3

sem_t *K;
sem_t *konzultacije;
sem_t *djedbozicnjak;
sem_t *sobovi;
int ID;
int *br_sobova = 0;
int *br_patuljaka = 0;
pid_t djedPid;

void djedbozicnjakFunk(){
    do
    {
        sem_wait(djedbozicnjak);
        sem_wait(K);
        if(*br_sobova == 10 && *br_patuljaka > 0){
            sem_post(K);
            printf("Stiglo je 10 sobova i nekoliko patuljaka, Djed Bozicnjak ukrcava i raznosi poklone.\n");
            printf("Djed salje sobove na odmor i nastavlja spavati.\n");
            sleep(2);
            sem_wait(K);

            for(int i = 0; i<10; i++){
                sem_post(sobovi);
            }
            *br_sobova = 0;
        }
        if(*br_sobova == 10){
            sem_post(K);
            printf("Djed hrani sobove.\n");
            sleep(2);
            sem_wait(K);
        }
        if(*br_patuljaka >= 3){
            sem_post(K);
            printf("Djed riješava problem od 3 patuljka.\n");
            sleep(2);
            sem_wait(K);

            for(int i = 0; i<3; i++){
                sem_post(konzultacije);
            }
            *br_patuljaka -= 3;
        }
        sem_post(K);

    } while (1);
    
}

void patuljciFunk(){
    sem_wait(K);
    (*br_patuljaka)++;
    printf("Pravim patuljka broj %d\n", *br_patuljaka);
    if(*br_patuljaka == 3){
        printf("Stiglo je 3 patuljka, budim Djeda.\n");
        sem_post(djedbozicnjak);
    }
    sem_post(K);
    sem_wait(konzultacije);
}

void soboviFunk(){
    sem_wait(K);
    (*br_sobova)++;
    printf("Pravim soba broj %d\n", *br_sobova);
    if(*br_sobova == 10){
        printf("Stiglo je 10 sobova, budimo Djeda.\n");
        sem_post(djedbozicnjak);
    }
    sem_post(K);
    sem_wait(sobovi);
}

void brisi(int sig){
    sem_destroy(K);
    sem_destroy(djedbozicnjak);
    sem_destroy(konzultacije);
    sem_destroy(sobovi);
    shmdt(K);
    shmdt(konzultacije);
    shmdt(djedbozicnjak);
    shmdt(sobovi);
    kill(djedPid, SIGKILL);
    exit(0);
}

int main(){
    sigset(SIGINT,brisi);
    
    ID = shmget(IPC_PRIVATE, sizeof(sem_t)*4 + sizeof(int)*2, 0600);
    K = shmat(ID, NULL, 0);
    shmctl(ID, IPC_RMID, NULL);

    konzultacije = (sem_t*) (K + 1);
    djedbozicnjak = (sem_t*) (konzultacije + 1);
    sobovi = (sem_t*) (djedbozicnjak + 1);
    br_sobova = (int*) (sobovi + 1);
    br_patuljaka = (int*) (br_sobova + 1);

    sem_init(K, 1, 1);
    sem_init(konzultacije, 1, 0);
    sem_init(djedbozicnjak,1, 0);
    sem_init(sobovi, 0, 0);

    djedPid = fork();
    if(djedPid == 0){
        djedbozicnjakFunk();
        exit(0);
    }

    srand(time(0));
    int delay;
    // "Sjeverni pol"
    do{
        delay = (rand() % 3) + 1;
        sleep(delay);

        if(rand() % 100 > 50 && *br_sobova < 10){
            if(fork() == 0){
                soboviFunk();
                exit(0);
            }
        }

        if(rand() % 100 > 50){
            if(fork() == 0){
                patuljciFunk();
                exit(0);
            }
        }

        
    }while(1);

}