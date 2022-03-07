package Main;

import java.util.Scanner;

public class First {

    public static void main(String[] args) {
        System.out.println("hello world");
        Scanner scanner = new Scanner(System.in); // 입력
        String str = scanner.nextLine(); // 한줄을 입력받음, 변수 str
        System.out.println(str);
    }

}