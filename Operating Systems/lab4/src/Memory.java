import java.util.LinkedList;
import java.util.List;

public class Memory {
    public int size;
    public char[] memoryList;
    public int[] indexList;

    public Memory(int size){
        this.size = size;
        memoryList = new char[size];
        indexList = new int[size];
        for(int i = 0; i<size; i++){
            memoryList[i] = '-';
            indexList[i] = i % 10;
        }
    }

    public String toString(){
        String returnString = new String();
        returnString += "Current Memory State.\n";
        for(int i = 0; i<size; i++){
            returnString += indexList[i];
        }
        returnString += '\n';
        for(int i = 0; i<size; i++){
            returnString += memoryList[i];
        }
        returnString += '\n';
        return returnString;
    }

    public void free(char f){
        boolean flag = false;
        System.out.println("Trying to free " + f + " request from memory.");
        for(int i = 0; i<size; i++){
            if(memoryList[i] == f){
                memoryList[i] = '-';
                flag = true;
            }
        }
        if(!flag){
            System.out.println("Memory didn't contain request " + f + ", so it did not free anything.");
        }
        else{
            System.out.println("Freed request " + f + " successfully.");
        }
    }

    public void take(char a, int s){
        String subString = "";
        String helpString = new String(memoryList);
        int i, index = -1, counter = 0, smallestSize = size;
        System.out.println("Trying to take memory with a size "+s+" and a request " + a);
        for(i = 0; i<size; i++){
            if(memoryList[i] == '-' && (i != size - 1)){
                counter++;
            }
            else {
                if(counter < smallestSize && counter >= s){
                    smallestSize = counter;
                    index = i - counter;
                }
                counter = 0;
            }
        }
        if(index == -1){
            System.out.println("Can't find free memory with size of at least " + s);
            return;
        }
        for(i = 0; i<s; i++){
            memoryList[index] = a;
            index++;
        }
        System.out.println("Memory occupied successfully!");
    }

    public void garbageCollect(){
        System.out.println("Starting garbage collector.");
        char[] newArray = new char[size];
        for(int i = 0; i<size; i++){
            newArray[i] = '-';
        }
        int counter = 0;
        for(int i = 0; i<size; i++){
            if(memoryList[i] != '-'){
                newArray[counter] = memoryList[i];
                counter++;
            }
        }
        memoryList = newArray;
    }
}
