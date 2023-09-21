import java.util.Random;

public class App 
{

    static int[][] matrix1;
    static int[][] matrix2;
    static int size = 5;
    static int minRange = -32;
    static int maxRange = 32;

    static int[][] matrixSec;
    static int[][] matrixCon;

    public static class MyThread extends Thread 
    {
        int row;

        public MyThread(int row) 
        {
            this.row = row;
        }

        public void run() 
        {
            for (int i = 0; i < size; i++) 
            {
                matrixCon[row][i] = matrix1[row][i] + matrix2[row][i];
            }
        }

    }

    public static void print2D(int mat[][]) 
    {
        for (int i = 0; i < size; i++) 
        {
            for (int j = 0; j < size; j++) 
            {
                System.out.print(mat[i][j] + " ");
            }
            System.out.println();
        }

    }

    public static int[][] generateMatrix(int size, int min, int max) 
    {
        int[][] matrix = new int[size][size];
        for (int i = 0; i < size; i++) 
        {
            for (int j = 0; j < size; j++) 
            {
                Random random = new Random();
                matrix[i][j] = random.nextInt(max - min + 1) + min;
            }
        }
        return matrix;
    }

    public static int[][] sumMatrix(int[][] mat1, int[][] mat2) 
    {
        int[][] matRes = new int[size][size];

        for (int i = 0; i < size; i++) 
        {
            for (int j = 0; j < size; j++) 
            {
                matRes[i][j] = mat1[i][j] + mat2[i][j];
            }
        }

        return matRes;
    }

    public static boolean matrixAreEqual(int[][] mat1, int[][] mat2) 
    {
        for (int i = 0; i < size; i++) 
        {
            for (int j = 0; j < size; j++) 
            {
                if (mat1[i][j] != mat2[i][j]) 
                {
                    return false;
                }
            }
        }

        return true;
    }

    public static void main(String[] args) throws Exception 
    {
        Thread[] threads = new Thread[size];

        matrix1 = generateMatrix(size, minRange, maxRange);
        matrix2 = generateMatrix(size, minRange, maxRange);

        matrixSec = sumMatrix(matrix1, matrix2);
        matrixCon = new int[size][size];

        for (int i = 0; i < size; i++) 
        {
            threads[i] = new MyThread(i);
        }

        for (int i = 0; i < size; i++) 
        {
            threads[i].start();
        }

        for (int i = 0; i < size; i++) 
        {
            threads[i].join();
        }

       
        System.out.print("   Matrix 1\n");
        System.out.println("---------------");
        print2D(matrix1);
        System.out.println();

        System.out.print("   Matrix 2\n");
        System.out.println("---------------");
        print2D(matrix2);
        System.out.println();

        System.out.print("   Matrix CS\n");
        System.out.println("---------------");
        print2D(matrixSec);
        System.out.println();

        System.out.print("   Matrix CC\n");
        System.out.println("---------------");
        print2D(matrixCon);
        System.out.println();

        System.out.println("Matrix CS and CC equal: " + matrixAreEqual(matrixSec, matrixCon));
    }
}
