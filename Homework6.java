//Anthony D'Alessandro
import java.util.*;
public class Homework6 {
	public int[] extendedEuclideanAlgorithm(int a, int b) {
		int[] linearGCD;
		ArrayList<int[]> gcd = new ArrayList<int[]>();
		
		int[] row1 = new int[4];
		int[] row2 = new int[4];
		
		row1[1] = a;
		row2[1] = b;

		row1[2] = 1;
		row2[2] = 0;

		row1[3] = 0;
		row2[3] = 1;
		
		gcd.add(row1);
		gcd.add(row2);
		
		int r;
		do {
			int arrayListSize = gcd.size();
			int[] recentRow = gcd.get(arrayListSize - 1);
			int[] secondRecentRow = gcd.get(arrayListSize - 2);
			
			int quotient = secondRecentRow[1] / recentRow[1];
			r = secondRecentRow[1] - quotient * recentRow[1];
			int s = secondRecentRow[2] - quotient * recentRow[2];
			int t = secondRecentRow[3] - quotient * recentRow[3];
			
			int[] newRow = new int[4];
			newRow[0] = quotient;
			newRow[1] = r;
			newRow[2] = s;
			newRow[3] = t;
			gcd.add(newRow);
		} while(r != 0);
	}
}
