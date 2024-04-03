// Anthony D'Alessandro
import java.util.*;

public class HomeworkTest {
	public static void main(String[] args) {
		Homework4 hw = new Homework4();
		Scanner scan = new Scanner(System.in);
		
		System.out.println("Please enter LFSR degree: ");
		int degree = scan.nextInt();
		
		System.out.println("Please enter number of output bits: ");
		int bits = scan.nextInt();
		
		System.out.println(hw.keyStreamLFSR(bits, degree));
	}
}
