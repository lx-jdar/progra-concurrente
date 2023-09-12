#include<stdio.h>
#include<stdlib.h>
#include <sys/wait.h>
#include <unistd.h>
#define NO_INI -1
#define PROS_CREATED 0

void showPidAndPha(char name);
int main()
{
 pid_t pIdB=NO_INI;
 pid_t pIdC=NO_INI;
 pid_t pIdD=NO_INI;
 pid_t pIdE=NO_INI;
 pid_t pIdF=NO_INI;
 pid_t pIdG=NO_INI;
 pid_t pIdH=NO_INI;
 pIdB=fork();
 if( pIdB != PROS_CREATED )
 {
  showPidAndPha('A');
  pIdC=fork();
 }
 if( pIdC == PROS_CREATED )
 {
  showPidAndPha('C');
  pIdF=fork();
 }
 if( pIdB == PROS_CREATED )
 {
  showPidAndPha('B');
  pIdE=fork();
  if( pIdE != PROS_CREATED )
    pIdD=fork();
 }
 if( pIdE == PROS_CREATED )
 {
  showPidAndPha('E');
  pIdG=fork();
  if( pIdG != PROS_CREATED )
    pIdH=fork();
 }
 if( pIdD == PROS_CREATED )
 {
   showPidAndPha('D');
 }
  if( pIdF == PROS_CREATED )
  { 
   showPidAndPha('F');
  }
  if( pIdG == PROS_CREATED )
  { 
   showPidAndPha('G');
  }
  if( pIdH == PROS_CREATED )
  {
   showPidAndPha('H');
  }
  sleep(15);
  return 0;
}

void showPidAndPha(char name)
{
  printf("Soy el proceso %c PID:%d y su Padre es:%d\n",name,getpid(),getppid());
}
