//Anthony D'Alessandro
import java.lang.Math;
import java.math.BigInteger;
import java.util.*;
public class FinalExam {
	//Helper method for #1 & solver for #5
	public void groupElementOrdersAndGenerators(int z) {
		//ArrayList to hold list of group generators
		ArrayList<Integer> generators = new ArrayList<Integer>();
		//Display group with 'subscript' z
		System.out.println("Group Z" + z + "\n----------");
		//Loop from 1 up to and including z - 1
		for (int i = 1; i < z; i++) {
			/*Loop from 1 up to and including z - 1 unless order of current element
			 * is found which results in a loop break
			 */
	          for (int j = 1; j < z; j++) {
	        	  //Store value of i raised to the power of j in a BigInteger
	        	  BigInteger exponentiation = BigInteger.valueOf(i).pow(j);
	        	  //Store the result of i^j (mod z)
	        	  BigInteger modResult = exponentiation.mod(BigInteger.valueOf(z));
	        	  //If the result of i^j (mod z) is equal to 1, then the order of i is found
	              if (modResult.equals(BigInteger.valueOf(1))) {
	            	  //Print the order of the current element i
	                  System.out.println("Order of " + i + " = " + j);
	                  //If the order of i is equal to z - 1, then i is also a generator of the group
	                  if (j == z - 1) {
	                	  //Store i in a generator variable of type Integer
	                	  Integer generator = Integer.valueOf(i);
	                	  //Add the generator to the list of generators
	                	  generators.add(generator);
	                  }
	                  //Break if order of current element is found
		              break;
	              }
	          }
	      }
		//Print list of generators for the group
		System.out.println("\nGenerators of Z" + z + ": " + generators);
	}
	
	//(#2b) Square-and-Multiply Method
	public int squareAndMultiply(int base, int exp, int mod) {
		String binaryExp = Integer.toBinaryString(exp);
		double product = (double) base;
		for (int i = 1; i < binaryExp.length(); i++) {
			String currentValue = "" + binaryExp.charAt(i);
			if (Integer.valueOf(currentValue).equals(1))
				product = ((Math.pow(product, 2)) * base) % mod;
			else
				product = (Math.pow(product, 2)) % mod;
		}
		return (int) product;
	}
}
