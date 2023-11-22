//Anthony D'Alessandro
public class Homework5 {
	public int[] polynomialAddition(int[] poly1, int[] poly2, int m) {
		int[] finalPolynomial = new int[m];
		
		for (int i = 0; i < m; i++)
			finalPolynomial[i] = (poly1[i] + poly2[i]) % 2;
		
		return finalPolynomial;
	}
	
	public int[] polynomialMultiplication(int[] poly1, int[] poly2, int[] irrPoly, int m) {
		final int finalMaxLength = (m * 2) - 1;
		int[] finalPolynomial = new int[finalMaxLength];
		
		for (int i = 0; i < m; i++) {
			for (int j = 0; j < m; j++) {
				int tempIndex = (m - (i + 1)) + (m - (j + 1));
				if (poly1[i] == 1 && poly2[j] == 1) {
					finalPolynomial[(finalMaxLength - 1) - tempIndex] += 1;
				}
			}
		}
		
		for (int i = 0; i < finalPolynomial.length; i++) {
			if (finalPolynomial[i] > 1)
				finalPolynomial[i] = finalPolynomial[i] % 2;
		}
		
		return finalPolynomial;
	}
}
