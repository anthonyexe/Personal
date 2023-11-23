// Anthony D'Alessandro
import java.util.*;

public class Tester {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		MidtermExam ex = new MidtermExam();
		Homework5 hw5 = new Homework5();
		
		
		
		System.out.println("Please enter the highest polynomial degree: ");
		int m = scan.nextInt();
		
		System.out.println("Please enter the coefficients of the first polynomial starting from the left:");
		int[] poly1 = new int[m];
		for (int i = 0; i < m; i++) {
			System.out.println("Coefficient " + (m-i) + ": ");
			poly1[i] = scan.nextInt();
		}
		
		System.out.println("Please enter the coefficients of the second polynomial starting from the left:");
		int[] poly2 = new int[m];
		for (int i = 0; i < m; i++) {
			System.out.println("Coefficient " + (m-i) + ": ");
			poly2[i] = scan.nextInt();
		}
		
		System.out.println("Please enter the degree of the irreducible polynomial to be used in multiplication: ");
		int n = scan.nextInt();
		
		System.out.println("Please enter the coefficients of the irreducible polynomial starting from the left:");
		int[] irrPoly = new int[m];
		for (int i = 0; i < m; i++) {
			System.out.println("Coefficient " + (m-i) + ": ");
			irrPoly[i] = scan.nextInt();
		}
		
		System.out.print("Polynomial 1 + Polynomial 2 =  ");
		int[] sum = hw5.polynomialAddition(poly1, poly2, m);
		for (int i = 0; i < m; i++) {
			if (i < m - 1)
				System.out.print(sum[i] + "x^" + (m - (i + 1)) + " + ");
			else
				System.out.print(sum[i] +"\n");
		}
		
		System.out.print("Polynomial 1 * Polynomial 2 = ");
		int[] product = hw5.polynomialMultiplication(poly1, poly2, m);
		int productLength = product.length;
		for (int i = 0; i < productLength; i++) {
			if (product[i] != 0) {
				if (i < productLength - 1)
					System.out.print("x^" + (productLength - (i + 1)) + " + ");
				else
					System.out.print(product[i]);
			}
		}
		
		/*
		 * 
		//Solve Problem 1
		System.out.println("-------- Problem 1 --------\n");
		System.out.println("Enter plaintext for Playfair Encryption: ");
		String plaintext = scan.nextLine();
		
		System.out.println("Enter the encryption key: ");
		String key = scan.nextLine();
		
		System.out.println("Ciphertext: " + ex.solveNumber1(plaintext, key));
		System.out.println("\n-------- End of Problem 1 --------\n");
		
		
		//Solve Problem 3
		System.out.println("-------- Problem 3 --------\n");
		System.out.println("Enter affine ciphertext: ");
		String ciphertext = scan.nextLine();
		
		System.out.println("Plaintext & Key: " + ex.solveNumber3(ciphertext));
		System.out.println("\n-------- End of Problem 3 --------\n");
		
		
		//Solve Problem 4
		System.out.println("-------- Problem 4 --------\n");
		System.out.println("Enter text for Index of Coincidence Test: ");
		String text = scan.nextLine();
		
		System.out.println("Index of Coincidence: " + ex.solveNumber4(text));
		System.out.println("\n-------- End of Problem 4 --------");
		
		*/
	}
}