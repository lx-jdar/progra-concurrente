#include<stdio.h>
#include<stdlib.h>
#include <sys/wait.h>
#include <unistd.h>
#define NO_INI -1
#define PROS_CREATED 0

void ShowPidAndPhaSi(pid_t pId,char name);

pid_t CreateProsSi(pid_t pId);

pid_t CreateProsSiNo(pid_t pId,pid_t pId2);

int main()
{
  pid_t pIdA=PROS_CREATED;
  pid_t pIdB=NO_INI;
  pid_t pIdC=NO_INI;
  pid_t pIdD=NO_INI;
  pid_t pIdE=NO_INI;
  pid_t pIdF=NO_INI;
  pid_t pIdG=NO_INI;
  pid_t pIdH=NO_INI;

  ShowPidAndPhaSi(pIdA,'A');
  
 
  pIdB=CreateProsSi(pIdA);
  
  pIdC=CreateProsSiNo(pIdA,pIdB);
  
  ShowPidAndPhaSi(pIdC,'C');
  
  pIdF=CreateProsSi(pIdC);

  ShowPidAndPhaSi(pIdB,'B');

  pIdE=CreateProsSi(pIdB);
  
  pIdD=CreateProsSiNo(pIdB,pIdE);
  
  ShowPidAndPhaSi(pIdE,'E');
  
  pIdG=CreateProsSi(pIdE);
  
  pIdH=CreateProsSiNo(pIdE,pIdG);
 

  ShowPidAndPhaSi(pIdD,'D');
  ShowPidAndPhaSi(pIdF,'F');
  ShowPidAndPhaSi(pIdG,'G');
  ShowPidAndPhaSi(pIdH,'H');
  sleep(15);
  return 0;
}

void ShowPidAndPhaSi(pid_t pId,char name)
{
  if( pId == PROS_CREATED )
    printf("Soy el proceso %c PID:%d y su Padre es:%d\n",name,getpid(),getppid());
}
pid_t CreateProsSi(pid_t pId)
{
    if(pId == PROS_CREATED)
     return fork();
    return -1;
}
pid_t CreateProsSiNo(pid_t pId,pid_t pId2)
{
    if(pId == PROS_CREATED && pId2 != PROS_CREATED)
      return fork();
    return -1;
}
