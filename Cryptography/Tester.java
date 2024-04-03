// Anthony D'Alessandro
import java.util.*;
import java.lang.Math;
public class Tester {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		FinalExam exam = new FinalExam();
		
		System.out.println("Please enter the group subscript: ");
		int subscript = scan.nextInt();
		
		exam.groupElementOrdersAndGenerators(subscript);
		
		System.out.println("\n------------------------------------\n");
		
		System.out.println("Please enter the base, exponent, and modulus for the Square-and-Multiply Algorithm:");
		System.out.println("Base: ");
		int base = scan.nextInt();
		System.out.println("Exponent: ");
		int exp = scan.nextInt();
		System.out.println("Modulus: ");
		int mod = scan.nextInt();
		
		int result = exam.squareAndMultiply(base, exp, mod);
		System.out.println(base + "^" + exp + " (mod " + mod + ")" + " = " + result);
	}
}
