import java.util.Scanner;

public class HomeworkTest {
	public static void main(String[] args) {
		Homework hw = new Homework();
		/*
		Scanner scan = new Scanner(System.in);
		
		System.out.println("Please enter some text: ");
		String input = scan.nextLine();
		
		
		System.out.println(hw.relativeFrequencies(input));
		*/
		
		System.out.println(hw.shiftCipherEncryption("Hello World", 1));
	}
}
