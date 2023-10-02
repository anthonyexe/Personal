import java.util.Scanner;

public class HomeworkTest {
	public static void main(String[] args) {
		Homework hw = new Homework();
		Scanner scan = new Scanner(System.in);
		
		System.out.println("Please enter some text: ");
		String input = scan.nextLine();
		
		System.out.println("Please enter a key value: ");
		int key = scan.nextInt();
		//int[] keyArr = new int[2];
		//System.out.println("Please enter key values: ");
		
		//for (int i = 0; i < keyArr.length; i++) {
		//	keyArr[i] = scan.nextInt();
		//}
		
		//System.out.println(keyArr[0] + " : " + keyArr[1]);
		//System.out.println(hw.affineCipherEncryption(input, keyArr));
		
		
		
		System.out.println(hw.frequencyAnalysis(input));
		System.out.println(hw.shiftCipherDecryption(input));
		
		//System.out.println(hw.shiftCipherEncryption(input, key));
	}
}
