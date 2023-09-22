import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class App 
{
    public static List<String> getArguments(String[] args) 
    {
        if (args.length == 0) 
        {
            return Arrays.asList("B", "C");
        } 
        else 
        {
            switch (args[0]) 
            {
                case "B":
                    return Arrays.asList("D", "E");
                case "C":
                    return Arrays.asList("F");
                case "E":
                    return Arrays.asList("G", "H");
                default:
                    return Arrays.asList();
            }
        }
    }

    public static void main(String[] args) throws Exception 
    {
        List<String> arguments = getArguments(args);
        List<Process> children = new ArrayList<Process>();

        ProcessHandle current = ProcessHandle.current();
        long pid = current.pid();
        long ppid = current.parent().get().pid();
        String process = args.length == 0 ? "A" : args[0];
        System.out.println(process + "-> PID: " + pid + " PPID: " + ppid);

        try 
        {
            for (String arg : arguments) 
            {
                ProcessBuilder pb = new ProcessBuilder("java", "App", arg);
                children.add(pb.inheritIO().start());
            }

            for (Process child : children) 
            {
                child.waitFor();
            }

            if (process.equals("A")) 
            {
                Thread.sleep(10000);
                //System.out.println("Waiting");
            }

        } 
        catch (IOException e) 
        {
            e.printStackTrace();
        } 
        catch (Exception expn) 
        {  
            // catching the exception  
            expn.printStackTrace();  
        }
    }
}
