// Anthony D'Alessandro
import java.util.*;

public class Tester {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		Homework5 hw5 = new Homework5();
		
		System.out.println("Please enter the highest polynomial degree: ");
		int m = scan.nextInt() + 1;
		
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
		int n = scan.nextInt() + 1;
		
		System.out.println("Please enter the coefficients of the irreducible polynomial starting from the left:");
		int[] irrPoly = new int[n];
		for (int i = 0; i < n; i++) {
			System.out.println("Coefficient " + (n-i) + ": ");
			irrPoly[i] = scan.nextInt();
		}
		
		System.out.print("Polynomial 1 + Polynomial 2 (GF2^M) =  ");
		int[] sum = hw5.polynomialAddition(poly1, poly2);
		ArrayList<String> printedSum = new ArrayList<String>();
		for (int i = 0; i < sum.length; i++) {
			if (sum[i] != 0) {
				String value;
				if (i == sum.length - 1) {
					value = "1";
				}
				else if (i == sum.length - 2) {
					value = "x";
				}
				else {
					value = "x^" + (sum.length - (i + 1));
				}
				printedSum.add(value);
			}
		}
		
		for (int i = 0; i < printedSum.size(); i++) {
			if (i < printedSum.size() - 1)
				System.out.print(printedSum.get(i) + " + ");
			else
				System.out.print(printedSum.get(i));
		}
		
		System.out.println();
		
		System.out.print("Polynomial 1 * Polynomial 2 = ");
		int[] product = hw5.standardPolynomialMultiplication(poly1, poly2, m);
		ArrayList<String> printedProduct = new ArrayList<String>();
		for (int i = 0; i < product.length; i++) {
			if (product[i] != 0) {
				String value;
				if (i == product.length - 1) {
					value = "1";
				}
				else if (i == product.length - 2) {
					value = "x";
				}
				else {
					value = "x^" + (product.length - (i + 1));
				}
				printedProduct.add(value);
			}
		}
		
		for (int i = 0; i < printedProduct.size(); i++) {
			if (i < printedProduct.size() - 1)
				System.out.print(printedProduct.get(i) + " + ");
			else
				System.out.print(printedProduct.get(i));
		}
		
		System.out.println();
		
		System.out.print("Polynomial 1 * Polynomial 2 (GF2^M) = ");
		int[] finalProduct = hw5.GF2MPolynomialMultiplication(product, irrPoly, m);
		ArrayList<String> printedProduct2 = new ArrayList<String>();
		for (int i = 0; i < finalProduct.length; i++) {
			if (finalProduct[i] != 0) {
				String value;
				if (i == finalProduct.length - 1) {
					value = "1";
				}
				else if (i == finalProduct.length - 2) {
					value = "x";
				}
				else {
					value = "x^" + (finalProduct.length - (i + 1));
				}
				printedProduct2.add(value);
			}
		}
			
		for (int i = 0; i < printedProduct2.size(); i++) {
			if (i < printedProduct2.size() - 1)
				System.out.print(printedProduct2.get(i) + " + ");
			else
				System.out.print(printedProduct2.get(i));
		}
	}
}