import java.util.Random;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Insert memory size > ");
        int n = sc.nextInt(); // list size
        Memory memory = new Memory(n); // initialising new Memory object
        char c;
        while(true){
             request();
             c = sc.next().charAt(0);
             if(c == 'e'){
                 System.out.println();
                 System.out.println("End of the program. :)");
                 System.out.println(memory);
                 break;
             }
             else if(c == 'o'){
                 System.out.println("Which part of the memory do you want to free? (Input must be in range from 0 to 9)");
                 char f = sc.next().charAt(0);
                 if(f < 48 || f > 57){
                     System.out.println("Wrong input, try again.");
                 }
                 else{
                     memory.free(f);
                     System.out.println(memory);
                 }
             }
             else if(c == 'z'){
                 System.out.print("Enter request number (Input must be in range from 0 to 9) > ");
                 char a = sc.next().charAt(0);
                 System.out.print("Enter size of request (Input must be in range from 0 to 9) > ");
                 int s = sc.nextInt();
                 if(a < 48 || a > 57 || s < 0 || s > 9){ // 48 ascii value of '0' and 57 ascii value of '9'
                     System.out.println("One of the inputs was wrong, try again.");
                 }
                 else{
                     memory.take(a, s);
                     System.out.println(memory);
                 }
             }
             else if(c == 'g'){
                 memory.garbageCollect();
                 System.out.println(memory);
             }
             else if(c == 'r'){
                 System.out.println("Making the program work randomly.");
                 System.out.print("How many iterations do you wish? > ");
                 int it = sc.nextInt();
                 random(memory, it);
                 break;
             }
             else{
                 System.out.println("Wrong input! Try again.");
             }
        }
    }

    public static void request(){
        System.out.println();
        System.out.println("Input time!");
        System.out.println("If you want to end the program, input - 'e'.");
        System.out.println("If you want to free memory, input - 'o'.");
        System.out.println("If you want to make a memory request, input - 'z'.");
        System.out.println("If you want the program to work randomly, input - 'r'.");
        System.out.println("If you want to start the garbage collector, input - 'g'.");
    }

    public static void random(Memory memory, int iterations){
        Random rand = new Random();
        int task;// if task 0 free memory, if task 1 make memory request, if task 2 start the garbage collector
        for(int i = 0; i<iterations; i++){
            task = rand.nextInt(3); // 0,1 or 2
            char c;
            int a;
            switch (task){
                case 0:
                    c = (char)(rand.nextInt(10) + '0'); // getting a random char from 0-9
                    memory.free(c);
                    break;
                case 1:
                    c = (char)(rand.nextInt(10) + '0');
                    a = rand.nextInt(10); // random number from 0-9
                    memory.take(c, a);
                    break;
                case 2:
                    memory.garbageCollect();
                    break;
            }
            System.out.println(memory);
            try {
                Thread.sleep(3000); // sleep for 2 seconds
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        System.out.println();
        System.out.println("End of the program. :)");
        System.out.println(memory);
    }
}
