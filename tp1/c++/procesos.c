#include<stdio.h>
#include<stdlib.h>
#include <sys/wait.h>
#include <unistd.h>
#define NO_INI -1
#define PROS_CREATED 0

void showPidAndPhaSi(pid_t pid,char name);
int main()
{
  pid_t pIdB=NO_INI;
  pid_t pIdC=NO_INI;
  pid_t pIdD=NO_INI;
  pid_t pIdE=NO_INI;
  pid_t pIdF=NO_INI;
  pid_t pIdG=NO_INI;
  pid_t pIdH=NO_INI;

  showPidAndPhaSi(PROS_CREATED,'A');
  pIdB=fork();
  if( pIdB != PROS_CREATED )
  {
   pIdC=fork();
  }
  if( pIdC == PROS_CREATED )
  {
   showPidAndPhaSi(pIdC,'C');
   pIdF=fork();
  }
  showPidAndPhaSi(pIdB,'B');
  if( pIdB == PROS_CREATED )
  {
   pIdE=fork();
   if( pIdE != PROS_CREATED )
     pIdD=fork();
  }

  showPidAndPhaSi(pIdE,'E');

  if( pIdE == PROS_CREATED )
  {
   pIdG=fork();
   if( pIdG != PROS_CREATED )
    pIdH=fork();
  }

  showPidAndPhaSi(pIdD,'D');
  showPidAndPhaSi(pIdF,'F');
  showPidAndPhaSi(pIdG,'G');
  showPidAndPhaSi(pIdH,'H');
  sleep(15);
  return 0;
}

void showPidAndPhaSi(pid_t pid,char name)
{
  if( pid == PROS_CREATED )
    printf("Soy el proceso %c PID:%d y su Padre es:%d\n",name,getpid(),getppid());
}
