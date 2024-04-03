//Anthony D'Alessandro
import java.util.*;
import java.lang.Math;
import java.math.BigInteger;
public class Homework6 {
	public int eulerPhi(int num) {
		//Store the num parameter as a BigInteger
		BigInteger number =  BigInteger.valueOf(num);
		//Declare count and set it to 0
		int count = 0;
		//Loop through values from 1 --> num
		for (int i = 1; i <= num; i++) {
				//If the greatest common divisor of the current value and the given number is equal to 1, increment count
				if (number.gcd(BigInteger.valueOf(i)).equals(BigInteger.valueOf(1)))
					count++;
		}
		return count;
	}
	
	public String extendedEuclideanAlgorithm(int a, int b) {
		//Declare ArrayList to hold int arrays that represent each round of gcd calculations
		ArrayList<int[]> gcdList = new ArrayList<int[]>();
		//Declare int arrays of length 4 to store values from 2 set-up gcd rounds
		int[] row1 = new int[4];
		int[] row2 = new int[4];
		//Set second value in each array to given a value and b value respectively
		row1[1] = a;
		row2[1] = b;
		//Set third value in each array to 1 and 0 respectively
		row1[2] = 1;
		row2[2] = 0;
		//Set fourth value in each array to 0 and 1 respectively
		row1[3] = 0;
		row2[3] = 1;
		//Add each of the first 2 int arrays that represent the gcd set-up rounds to the ArrayList of gcd calculations
		gcdList.add(row1);
		gcdList.add(row2);
		
		//Declare int to represent the remainder to be used in do-while loop condition
		int r;
		do {
			int arrayListSize = gcdList.size();
			int[] recentRow = gcdList.get(arrayListSize - 1);
			int[] secondRecentRow = gcdList.get(arrayListSize - 2);
			
			int quotient = secondRecentRow[1] / recentRow[1];
			r = secondRecentRow[1] - quotient * recentRow[1];
			int s = secondRecentRow[2] - quotient * recentRow[2];
			int t = secondRecentRow[3] - quotient * recentRow[3];
			
			int[] newRow = new int[4];
			newRow[0] = quotient;
			newRow[1] = r;
			newRow[2] = s;
			newRow[3] = t;
			gcdList.add(newRow);
		} while(r != 0);
		
		int[] secondToLastRow = gcdList.get(gcdList.size() - 2);
		int gcd = secondToLastRow[1];
		String linearCombination = "GCD = " + gcd + "\n" + gcd + " = " + secondToLastRow[2] + " x " + a + " + " + secondToLastRow[3] + " x " + b;
		
		return linearCombination;
		
	}
}
