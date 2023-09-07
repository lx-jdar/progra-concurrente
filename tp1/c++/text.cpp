#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

#define MAX_CHILD 2

int main(int argc, char const *argv[]) {
  for (int i = 0; i < MAX_CHILD; i++) {
    pid_t pid = fork();
    if (pid < 0) {
      printf("Error de creación\n");
      return EXIT_FAILURE;
    }

    if (!pid) {
      printf("Proceso Hijo %d\n", getpid());
      return EXIT_SUCCESS;
    }
  }
  sleep(30);
  for (int i = 0; i < MAX_CHILD; i++) {
    wait(NULL);
  }

  return EXIT_SUCCESS;
}