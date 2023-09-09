#include <iostream>
#include <map>
#include <sys/wait.h> // it has wait function
#include <unistd.h>   // it has fork function

std::map<std::string, std::string> m;

int createProcesses(std::string letter) {
  //std::cout << "HOLA " << letter << " " << m[letter].length();
  int stat;
  for (int i = 0; i < m[letter].length(); i++) {
      pid_t pid = fork();
      if (pid < -1)
      {
          std::cout << "Error de creación" << std::endl;
          exit(1);
      }
      if (!pid) // if pid == 0, it's the child
      {
          std::string s;
          s.push_back(m[letter][i]);
          std::cout << "PID_Child: " << getpid() << " Padre: " << getppid()
                    << " Node: " << s << std::endl;
          if (s.length() != 0) 
          {  
            createProcesses(s);
            //std::cout << "next: " << std::endl;
          }
          //std::cout << "PID_Child: 1";
          sleep(10);
          return pid;
      }
      //std::cout << "PID_Child: 2";
      sleep(1);
      //pid_t cpid = waitpid(pid, &stat, 0);
      /*if (WIFEXITED(stat))
        printf("Child %d terminated with status: %d\n",
          cpid, WEXITSTATUS(stat)); */
  }
  return 1;
}

int main(int argc, char const *argv[]) {
  m["A"] = "CB";
  m["B"] = "ED";
  m["C"] = "F";
  m["D"] = "";
  m["E"] = "HG";
  m["F"] = "";
  std::cout << "PID_INIT : " << getpid() << " Padre: " << getppid()
            << " Node: A" << std::endl;

  /*std::cout << "PID_INIT : " << getpid() << " Padre: " << getppid()
            << " Node: " << "A with childs: " << m["A"] << std::endl; */
  
  if (createProcesses("A")) {
    sleep(20); 
    for (int i = 0; i < 7; i++) {
      wait(NULL);
    }
  }
  return EXIT_SUCCESS;
}
