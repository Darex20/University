#define _XOPEN_SOURCE 500
#include <signal.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/time.h>
#include <math.h>
#include <stdlib.h>

unsigned long pauza = 0;
unsigned long broj = 1000000001;
unsigned long zadnji = 1000000001;

void periodicki_ispis(){
    printf("Zadnji prosti broj je %lu \n", zadnji);
}

void postavi_pauzu(){
    pauza = 1 - pauza;
}

void prekini(){
    printf("Zadnji prosti broj je %lu \n", zadnji);
    exit(0);
}

int prost(unsigned long n){
    unsigned long i, max;

    if((n & 1) == 0)
        return 0;
    
    max = sqrt(n);

    for(i = 3;i <= max;i+=2){
        if((n % i) == 0)
            return 0;
    }

    return 1;
}

int main(){
    sigset(SIGTERM, prekini);
    sigset(SIGALRM, periodicki_ispis);
    sigset(SIGINT,postavi_pauzu);

    struct itimerval t;

    t.it_value.tv_sec = 5;
    t.it_value.tv_usec = 0;

    t.it_interval.tv_sec = 5;
    t.it_interval.tv_usec = 0;

    setitimer(ITIMER_REAL, &t, NULL);

    while(1){
        if(prost(broj) == 1)
            zadnji = broj;
        broj++;
        while(pauza == 1)
            pause();
    }

    return 0;
}
    