import java.util.*;
import java.util.Map.Entry;

public class HomeworkTest {
	public static void main(String[] args) {
		Homework hw = new Homework();
		Scanner scan = new Scanner(System.in);
		
		
		System.out.println("Please enter some text: ");
		String input = scan.nextLine();
		
		System.out.println("Please enter vigenere key: ");
		String input2 = scan.nextLine();
		//System.out.println("Please enter a key value: ");
		//int key = scan.nextInt();
		
		
		int[] keyArr = new int[2];
		System.out.println("Please enter key values: ");
		
		for (int i = 0; i < keyArr.length; i++) {
			keyArr[i] = scan.nextInt();
		}
		
		System.out.println(keyArr.length);
		System.out.println(keyArr[0] + " : " + keyArr[1]);
		System.out.println(hw.affineCipherEncryption(input, keyArr));
		
		System.out.println(hw.bruteForceAffineCipherDecryption(hw.affineCipherEncryption(input, keyArr)));
		
		
		//System.out.println(hw.shiftCipherEncryption(input, key) + "\n");
		//System.out.println(hw.frequencyAnalysis(input) + "\n");
		//System.out.println(hw.shiftCipherDecryption(hw.affineCipherEncryption(input, keyArr)));
		
		//HashMap<Character, ArrayList<int[]>> temp = hw.affineCipherDecryption(hw.affineCipherEncryption(input, keyArr));
		//System.out.println(hw.affineCipherDecryption(hw.affineCipherEncryption(input, keyArr)));
		/*
		for (Entry<Character, ArrayList<int[]>> entry : temp.entrySet()) {
			for (int i = 0; i < entry.getValue().size(); i++) {
				for (int j = 0; j < entry.getValue().get(i).length; j++)
				System.out.println(entry.getKey() + " : " + entry.getValue().get(i)[0] + "," + entry.getValue().get(i)[1] + "\n");
				//System.out.println(entry.getKey() + " : " + entry.getValue().get(i)[1] + "\n");
			}
		}*/
		
		System.out.println(hw.vigenereCipherEncryption(input, input2));
		
		
		
	}
}