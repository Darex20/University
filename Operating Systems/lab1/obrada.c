#define _XOPEN_SOURCE 500
#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#define N 6    /*broj razina proriteta*/

int OZNAKA_CEKANJA[N];
int PRIORITET[N];
int TEKUCI_PRIORITET;
 

int sig[]={SIGUSR1, SIGUSR2, SIGTERM, SIGQUIT, SIGINT};

void zabrani_prekidanje(){
   int i;
   for(i=0; i<5; i++)
      sighold(sig[i]);    
}

void dozvoli_prekidanje(){
   int i;
   for(i=0; i<5; i++)
      sigrelse(sig[i]);
}

void obrada_signala(int i){
   /* obrada se simulira trošenjem vremena,
      obrada traje 5 sekundi, ispis treba biti svake sekunde */
   switch(i){
      case 1:
         printf("-  P  -  -  -  -\n");
         for(int j = 1;j<6;j++){
            sleep(1);
            printf("-  %d  -  -  -  -\n",j);
         }
         printf("-  K  -  -  -  -\n");
         break;

      case 2:
         printf("-  -  P  -  -  -\n");
         for(int j = 1;j<6;j++){
            sleep(1);
            printf("-  -  %d  -  -  -\n",j);
         }
         printf("-  -  K  -  -  -\n");
         break;

      case 3:
         printf("-  -  -  P  -  -\n");
         for(int j = 1;j<6;j++){
            sleep(1);
            printf("-  -  -  %d  -  -\n",j);
         }
         printf("-  -  -  K  -  -\n");
         break;

      case 4:
         printf("-  -  -  -  P  -\n");
         for(int j = 1;j<6;j++){
            sleep(1);
            printf("-  -  -  -  %d  -\n",j);
         }
         printf("-  -  -  -  K  -\n");
         break;

      case 5:
         printf("-  -  -  -  -  P\n");
         for(int j = 1;j<6;j++){
            sleep(1);
            printf("-  -  -  -  -  %d\n",j);
         }
         printf("-  -  -  -  -  K\n");
         break;
   }
}

void prekidna_rutina(int sig){
   int n = -1, x;
   
   zabrani_prekidanje();
   
   switch(sig){
      case SIGUSR1: 

         n=1; 
         printf("-  X  -  -  -  -\n");
         break;

      case SIGUSR2: 
  
         n=2; 
         printf("-  -  X  -  -  -\n");
         break;
      
      case SIGTERM:

         n=3;
         printf("-  -  -  X  -  -\n");
         break;
    
      case SIGQUIT:
         
         n=4;
         printf("-  -  -  -  X  -\n");
         break;

      case SIGINT:

         n=5;
         printf("-  -  -  -  -  X\n");
         break;
   }

   OZNAKA_CEKANJA[n]++;
   do{
      x = 0;
      for(int j = TEKUCI_PRIORITET+1; j<N;j++){
         if(OZNAKA_CEKANJA[j] != 0){
            x = j;
         }
      }
      
      if(x > 0){
         OZNAKA_CEKANJA[x]--;
         PRIORITET[x] = TEKUCI_PRIORITET;
         TEKUCI_PRIORITET = x;
         
         dozvoli_prekidanje();

         obrada_signala(x);

         zabrani_prekidanje();

         TEKUCI_PRIORITET = PRIORITET[x];
      }

   }while(x > 0);

   dozvoli_prekidanje();
}

int main (){
   sigset (SIGUSR1, prekidna_rutina);
   sigset (SIGUSR2, prekidna_rutina);
   sigset (SIGTERM, prekidna_rutina);
   sigset (SIGQUIT, prekidna_rutina);
   sigset (SIGINT, prekidna_rutina);

   printf("Proces obrade prekida, PID=%ld\n", getpid());
   printf("GP S1 S2 S3 S4 S5\n");
   printf("-----------------\n");

   /* troši vrijeme da se ima šta prekinuti - 10 s */
    for(int i = 0; i<11;i++){
        printf("%d  -  -  -  -  -\n",i);
        sleep(1);
    }

   printf ("Zavrsio osnovni program\n");

   return 0;
}

