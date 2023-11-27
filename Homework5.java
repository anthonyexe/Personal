//Anthony D'Alessandro
public class Homework5 {
	public int[] polynomialAddition(int[] poly1, int[] poly2) {
		if (poly1.length > poly2.length) {
			int[] newPoly2 = new int[poly1.length];
			int difference = poly1.length - poly2.length;
			for (int i = 0; i < newPoly2.length; i++) {
				if (i < difference) {
					newPoly2[i] = 0;
				}
				else {
					newPoly2[i] = poly2[i - difference];
				}
			}
			int[] finalPolynomial = new int[poly1.length];
			for (int i = 0; i < finalPolynomial.length; i++) {
				finalPolynomial[i] = ((poly1[i] + newPoly2[i]) % 2);
			}
			return finalPolynomial;
		}
		
		else if (poly2.length > poly1.length) {
			int[] newPoly1 = new int[poly2.length];
			int difference = poly2.length - poly1.length;
			for (int i = 0; i < newPoly1.length; i++) {
				if (i < difference) {
					newPoly1[i] = 0;
				}
				else {
					newPoly1[i] = poly2[i - difference];
				}
			}
			int[] finalPolynomial = new int[poly2.length];
			for (int i = 0; i < finalPolynomial.length; i++) {
				finalPolynomial[i] = ((poly1[i] + newPoly1[i]) % 2);
			}
			return finalPolynomial;
		}
		else {
			int[] finalPolynomial = new int[poly1.length];
			for (int i = 0; i < finalPolynomial.length; i++)
				finalPolynomial[i] = (poly1[i] + poly2[i]) % 2;
			
			return finalPolynomial;
		}
	}
	
	public int[] standardPolynomialMultiplication(int[] poly1, int[] poly2, int m) {
		final int finalMaxLength = (m * 2) - 1;
		int[] finalPolynomial = new int[finalMaxLength];
		
		for (int i = 0; i < m; i++) {
			for (int j = 0; j < m; j++) {
				if (poly1[i] == 1 && poly2[j] == 1) {
					int tempIndex = (m - (i + 1)) + (m - (j + 1));
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
	
	public int[] GF2MPolynomialMultiplication(int[] product, int[] irrPoly, int m) {
		int[] reducedProduct;
		int productHighestDegree = 0;
		for (int i = 0; i < product.length; i++) {
			if (product[i] == 1) {
				productHighestDegree = product.length - (i + 1);
				break;
			}
		}
		
		if (productHighestDegree < m)
			return product;
		
		int irrPolyLength = irrPoly.length;
		int degreeDifference = productHighestDegree - (irrPolyLength - 1);
		if (degreeDifference > 0) {
			int[] tempArray = new int[irrPolyLength + degreeDifference];
			for (int i = 0; i < irrPolyLength; i++) {
				if (irrPoly[i] == 1) {
					tempArray[i] = 1;	
				}
			}
			reducedProduct = polynomialAddition(product, tempArray);
			if (productHighestDegree >= m - 1)
				reducedProduct = GF2MPolynomialMultiplication(reducedProduct, irrPoly, m);
		}
		else {
			reducedProduct = polynomialAddition(product, irrPoly);
			return reducedProduct;
		}
		
		return reducedProduct;
	}
}