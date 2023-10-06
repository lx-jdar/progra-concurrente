import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.Random;
import java.util.concurrent.ArrayBlockingQueue;

public class App 
{

  private static final int MIN_VALUE = 0;
  private static final int MAX_VALUE = 99;
  private static int quantity;

  public static class Producer extends Thread 
  {
    private final ArrayBlockingQueue<Optional<Integer>> queue;

    public Producer(ArrayBlockingQueue<Optional<Integer>> queue) 
    {
      this.queue = queue;
    }

    public void run() 
    {
      try 
      {
        for (int i = 0; i < quantity; i++) 
        {
          // Genero un valor random
          Random random = new Random();
          int item = random.nextInt(MAX_VALUE - MIN_VALUE + 1) + MIN_VALUE;
          // Agrego el valor a la cola
          queue.put(Optional.ofNullable(item));
          Thread.sleep(100);
        }
        // Agrego null para avisar al consumidor que el productor dejo de producir
        queue.put(Optional.ofNullable(null));
      } 
      catch (InterruptedException e) 
      {
        Thread.currentThread().interrupt();
      }
    }
  }

  public static class Consumer extends Thread 
  {
    private final ArrayBlockingQueue<Optional<Integer>> queue;
    private ArrayList<Integer> values = new ArrayList<>(); 

    public Consumer(ArrayBlockingQueue<Optional<Integer>> queue) 
    {
      this.queue = queue;
    }

    public void run() 
    {
      try 
      {
        // Tomo valor de la cola
        Optional<Integer> value = queue.take();
        // El isPresent() me indica que existe el valor y no es null
        while (value.isPresent()) 
        {
          // Guardo el valor
          values.add(value.get());
          Thread.sleep(200);
          value = queue.take();
        }
      } 
      catch (InterruptedException e) 
      {
        Thread.currentThread().interrupt();
      }
      this.showStadistics();
    }

    private void showStadistics() 
    {   
      int sum = 0;
      int min = MAX_VALUE;
      int max = MIN_VALUE;

      for (int value : values) 
      {
        sum += value;
        min = Math.min(min, value);
        max = Math.max(max, value);
      }

      double average = (double) sum / values.size();

      System.out.println("Sum: " + sum);
      System.out.println("Average: " + average);
      System.out.println("Min: " + min);
      System.out.println("Max: " + max);
      System.out.print("Most Frequent Values: ");
      getMostFrequentValues().forEach((value) -> System.out.print(value + " "));
    }

    private ArrayList<Integer> getMostFrequentValues ()
    {
      Map<Integer, Integer> mapValues = new HashMap<>();

        // Genero el map con los valores y la cantidad de veces que aparecen
      for (Integer value : values) 
      {
        mapValues.put(value, mapValues.getOrDefault(value, 0) + 1);
      }

      // Busco cual es la maxima cantidad
      int maxCount = 0;
      for (int count : mapValues.values()) 
      {
        maxCount = Math.max(maxCount, count);
      }

      // Busco todos los valores con la max cantidad
      ArrayList<Integer> mostFrequentNumbers = new ArrayList<>();
      for (Map.Entry<Integer, Integer> entry : mapValues.entrySet()) 
      {
        if (entry.getValue() == maxCount) 
        {
          mostFrequentNumbers.add(entry.getKey());
        }
      }

      return mostFrequentNumbers;
    }
  }

  public static void main(String[] args) throws Exception 
  {
    try 
    {
      quantity = Integer.parseInt(args[0]);
    } 
    catch (NumberFormatException e) 
    {
      // En caso que el valor pasado por argumento no sea un numero
      System.err.println("Invalid input. Please provide a valid integer as the first argument.");
      System.exit(-1);
    } 
    catch (ArrayIndexOutOfBoundsException e) 
    {
      // En caso que no se haya pasado ningun argumento
      System.err.println("No input provided. Please provide an integer as the first argument.");
      System.exit(-1);
    }

    // Creo el ArrayBlockingQueue
    ArrayBlockingQueue<Optional<Integer>> queue = new ArrayBlockingQueue<>(quantity);

    System.out.println("Loading...");

    // Creo el productor y el consumidor
    Thread producerThread = new Thread(new Producer(queue));
    Thread consumerThread = new Thread(new Consumer(queue));

    producerThread.start();
    consumerThread.start();    

    producerThread.join();
    consumerThread.join();
  }
}
