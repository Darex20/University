#define _XOPEN_SOURCE 500
#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

int pid=0;

void prekidna_rutina(int sig){
   /* pošalji SIGKILL procesu 'pid'*/
   kill(pid, SIGKILL);
   exit(0);
}

int main(int argc, char *argv[]){
   pid=atoi(argv[1]);
   sigset(SIGINT, prekidna_rutina);
   srand(time(0));

   while(1){
        /* odspavaj 3-5 sekundi */
        int num = (rand() % 3) + 3 ;
        sleep(num);

        /* slučajno odaberi jedan signal (od 4) */
        int i = (rand() % 4) + 1;

        /* pošalji odabrani signal procesu 'pid' funkcijom kill*/
        switch(i){
            case 1: 
                kill(pid, SIGUSR1);
                break;
            case 2:
                kill(pid, SIGUSR2);
                break;
            case 3:
                kill(pid, SIGTERM);
                break;
            case 4:
                kill(pid, SIGQUIT);
                break;
        }
   }
   return 0;
}