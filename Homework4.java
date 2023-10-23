//Anthony D'Alessandro
import java.util.*;

public class Homework4 {
	public int[] stateLFSR(int degree) {
		int[] states = new int[degree];
		
		for (int i = 0; i < states.length; i++) {
			if (i == 0)
				states[i] = 1;
			else {
				states[i] = 0;
			}
		}
		
		return states;
	}
	
	
	public int[] feedbackCoefficientsLFSR(int degree) {
		int[] feedbackCoefficients = new int[degree];
		Scanner scan = new Scanner(System.in);
		System.out.println("Please enter either a 0 or a 1 to indicate each feedback coefficient");
		
		for (int i = 0; i < feedbackCoefficients.length; i++) {
			feedbackCoefficients[i] = scan.nextInt();
		}
		
		return feedbackCoefficients;
	}
	
	public int exclusiveOR(int num1, int num2) {
		if ((num1 == 1 && num2 == 0) || (num1 == 0 && num2 == 1))
			return 1;
		else
			return 0;
	}
	
	public ArrayList<Integer> keyStreamLFSR(int numOfBits, int degree) {
		int[] states = stateLFSR(degree);
		int[] feedbackCoefficients = feedbackCoefficientsLFSR(degree);
		ArrayList<Integer> keyStream = new ArrayList<Integer>(numOfBits);
		
		for (int i = 0; i < keyStream.size(); i++) {
			keyStream.add(states[states.length - 1]);
			for (int j = 1; j < states.length; j++) {
				states[states.length - j] = states[states.length - (j + 1)];
			}
			
			int temp = 0;
			for (int k = states.length; k >= 0; k--) {
				if ()
			}
		}
		
	}
}
