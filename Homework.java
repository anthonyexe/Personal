import java.util.*;
import java.util.Map.Entry;
import java.text.DecimalFormat;
import java.lang.Math;

public class Homework {
	
	public HashMap<Character, Double> frequencyAnalysis(String ciphertext) {
		HashMap<Character, Integer> frequencies = new HashMap<Character, Integer>();
		HashMap<Character, Double> rFrequencies = new HashMap<Character, Double>(frequencies.size());
		DecimalFormat df = new DecimalFormat("#.000");
		double count = 0;
		
		for (int i = 0; i < ciphertext.length(); i++) {
			count++;
			Character current = Character.toLowerCase(ciphertext.charAt(i));
			if (!Character.isWhitespace(current)) {
				if (!frequencies.containsKey(current)) {
					frequencies.put(current, 1);
				}
				
				else {
					frequencies.put(current, frequencies.get(current) + 1);
				}
			}
		}
		Set<Character> keys = frequencies.keySet();
		
		for (Character currentChar : keys) {
			if (!rFrequencies.containsKey(currentChar)) {
				Double currentRelativeFrequency = Double.parseDouble(df.format(frequencies.get(currentChar) / count));
				rFrequencies.put(currentChar, currentRelativeFrequency);
			}
		}
		return rFrequencies;
	}
	
	public HashMap<Integer, Character> initializeAlphabet() {
		final int alphabetSize = 26;
		HashMap<Integer, Character> alphabet = new HashMap<Integer, Character>(alphabetSize);
		
		Character ch = 'a';
		for (Integer i = 0; i < alphabetSize; i++) {
			if (ch == 'a') {
				alphabet.put(i, ch);
				ch++;
			}
			else {
				alphabet.put(i, ch);
				ch++;
			}
		}
		return alphabet;
	}
	
	public String alphabeticShift(String text, int key) {
		HashMap<Integer, Character> alphabet = initializeAlphabet();
		String shiftedText = "";
		
		for (int i = 0; i < text.length(); i++) {
			Character current = Character.toLowerCase(text.charAt(i));
			
			if (!Character.isWhitespace(current)) {
				Integer currentIndex = current - 'a' + 1;
				Integer shiftedIndex = (currentIndex - key) % 26;
				if (shiftedIndex < 0)
					shiftedIndex += 26;
				
				Character shiftedChar = alphabet.get(shiftedIndex);
				shiftedText += shiftedChar;
			}
			else {
				shiftedText += " ";
			}
		}
		return shiftedText;
	}
	
	public String shiftCipherEncryption(String plaintext, int key) {
		String ciphertext = "";
		
		HashMap<Integer, Character> alphabet = initializeAlphabet();
		
		if (key > 25 || key < 1) {
			return "Invalid Key";
		}
		
		for (int i = 0; i < plaintext.length(); i++) {
			Character current = Character.toLowerCase(plaintext.charAt(i));
			
			if (!Character.isWhitespace(current)) {
				Integer currentIndex = current - 'a';
				Integer shiftedIndex = (currentIndex + key) % 26;
				
				Character shiftedChar = alphabet.get(shiftedIndex);
				ciphertext += shiftedChar;
			}
			else {
				ciphertext += " ";
			}
		}
		return ciphertext;
	}
	
	public int checkFrequentTwoLetterWords(String text) {
		ArrayList<String> twoLetterWords = new ArrayList<String>(List.of("of", "to", "in", "it", "is", "be", "as", "at", "so", "we", "he", "by", "or", "on", "do", "if", "me", "my", "up", "an", "go", "no", "us", "am"));
		int count = 0;
		
		for (String word : twoLetterWords) {
			if (text.contains(word))
				count++;
		}
		
		return count;
	}
	
	public LinkedHashMap<Character, Double> sortFrequencyHashMap(HashMap<Character, Double> frequencyMap) {
		LinkedHashMap<Character, Double> sortedFrequencies = new LinkedHashMap<Character, Double>();
		ArrayList<Double> frequencies = new ArrayList<Double>();
		
		for (Map.Entry<Character, Double> entry : frequencyMap.entrySet()) {
			frequencies.add(entry.getValue());
		}
		
		Collections.sort(frequencies);
		
		for (Double value : frequencies) {
			for(Entry<Character, Double> entry : frequencyMap.entrySet()) {
				if (entry.getValue().equals(value)) {
					sortedFrequencies.put(entry.getKey(), value);
				}
			}
		}
		
		return sortedFrequencies;

	}
	
	public String shiftCipherDecryption(String ciphertext) {
		String plaintext;
		int key;
		
		LinkedHashMap<Character, Double> sortedRelativeFrequencies = sortFrequencyHashMap(frequencyAnalysis(ciphertext));
		Set<Character> sortedKeys = sortedRelativeFrequencies.keySet();
		ArrayList<Character> listOfSortedKeys = new ArrayList<Character>(sortedKeys);
		ArrayList<Character> mostCommonChars = new ArrayList<Character>();
		
		for (int i = 0; i < 5; i++) {
			mostCommonChars.add(listOfSortedKeys.get(listOfSortedKeys.size() - (1 + i)));
		}
		
		
		int greatestTwoLetterFrequency = 0;
		Character topKey = 'a';
		for (int i = 0; i < 5; i++) {
			Character currentCommonChar = mostCommonChars.get(i);
			Integer currentIndex = currentCommonChar - 'a' + 1;
			Integer currentKey = Math.abs(currentIndex - 4);
			
			plaintext = alphabeticShift(ciphertext, currentKey);
			int currentTwoLetterFrequency = checkFrequentTwoLetterWords(plaintext);
			
			if (i == 0) {
				greatestTwoLetterFrequency = currentTwoLetterFrequency;
				topKey = currentCommonChar;
			}
			else if(greatestTwoLetterFrequency < currentTwoLetterFrequency) {
				greatestTwoLetterFrequency = currentTwoLetterFrequency;
				topKey = currentCommonChar;
			}
		}
		
		Integer greatestIndex = topKey - 'a' + 1;
		key = Math.abs(greatestIndex - 4);
		
		plaintext = alphabeticShift(ciphertext, key);
		
		return plaintext;
	}
	
	public String affineCipherEncryption(String plaintext, int[] key) {
		String ciphertext = "";
		
		HashMap<Integer, Character> alphabet = initializeAlphabet();
		int[] coprimeKeys = {1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25};
		ArrayList<Integer> coprimeKeyList = new ArrayList<Integer>();
		
		for (int i = 0; i < coprimeKeys.length; i++) {
			coprimeKeyList.add(coprimeKeys[i]);
		}
		
		if (key.length != 2 || !(coprimeKeyList.contains(key[0])) || (key[1] > 25 || key[1] < 1)) {
			return "Invalid Key";
		}
		
		for (int i = 0; i < plaintext.length(); i++) {
			Character current = Character.toLowerCase(plaintext.charAt(i));
			
			if (!Character.isWhitespace(current)) {
				Integer currentIndex = current - 'a';
				Integer shiftedIndex = ((currentIndex * key[0]) + key[1]) % 26;
				
				Character shiftedChar = alphabet.get(shiftedIndex);
				ciphertext += shiftedChar;
			}
			else {
				ciphertext += " ";
			}
		}
		
		return ciphertext;
	}
	
	public HashMap<Character, ArrayList<int[]>> affineCipherDecryption(String ciphertext) {
		String plaintext = " ";
		
		LinkedHashMap<Character, Double> sortedRelativeFrequencies = sortFrequencyHashMap(frequencyAnalysis(ciphertext));
		Set<Character> sortedKeys = sortedRelativeFrequencies.keySet();
		ArrayList<Character> listOfSortedKeys = new ArrayList<Character>(sortedKeys);
		ArrayList<Character> mostCommonChars = new ArrayList<Character>();
		
		for (int i = 0; i < 5; i++) {
			mostCommonChars.add(listOfSortedKeys.get(listOfSortedKeys.size() - (1 + i)));
		}
		
		HashMap<Character, ArrayList<int[]>> possibleKeys = new HashMap<Character, ArrayList<int[]>>();
		int[] possibleKeyMultipliers = {1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25};
		
		for (int i = 0; i < mostCommonChars.size(); i++) {
			int currentIndex = mostCommonChars.get(i) - 'a' + 1;
			ArrayList<int[]> currentPossibleKeys = new ArrayList<int[]>();
			
			for (int j = 0; j < possibleKeyMultipliers.length; j++) {
				for (int k = 0; k < 26; k++) {
					if (4 == ((currentIndex * possibleKeyMultipliers[j]) + k) % 26) {
						int[] key = {possibleKeyMultipliers[j], k};
						currentPossibleKeys.add(key);
					}
				}
			}
			possibleKeys.put(mostCommonChars.get(i), currentPossibleKeys);
		}
		
		return possibleKeys;
	}
	
	public int modMultiplicativeInverse(int num) {
		int inverse = 1;
		
		for (int i = 1; i < 26; i++) {
			if (((num % 26) * (i % 26)) % 26 == 1) {
				inverse =  i;
				return inverse;
			}
		}
		return inverse;
	}
	
	public String bruteForceAffineCipherDecryption(String ciphertext) {
		String plaintext = "";
		HashMap<Integer, Character> alphabet = initializeAlphabet();
		ArrayList<int[]> possibleKeys = new ArrayList<int[]>();
		ArrayList<String> plaintexts = new ArrayList<String>();
		int[] possibleMultipliers = {1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25};
		
		for (int i = 0; i < possibleMultipliers.length; i++) {
			for (int j = 0; j < 26; j++) {
				if (i == 0 && j == 0) {
					continue;
				}
				else {
					int[] tempKey = {possibleMultipliers[i], j};
					possibleKeys.add(tempKey);
				}
			}
		}
		
		// decryption key sum value = 26 - key[1]
		// decryption key multiplier = multiplicative inverse
		
		for (int i = 0; i < possibleKeys.size(); i++) {
			String tempPlaintext = "";
			int[] currentKey = possibleKeys.get(i);
			int additiveInverse = 26 - currentKey[1];
			int multiplicativeInverse = modMultiplicativeInverse(currentKey[0]);
			
			for (int j = 0; j < ciphertext.length(); j++) {
				Character current = Character.toLowerCase(ciphertext.charAt(j));
				if (!Character.isWhitespace(current)) {
					int currentIndex = current - 'a' + 1;
					int shiftedIndex = (current + additiveInverse) * multiplicativeInverse;
					
					Character shiftedChar = alphabet.get(shiftedIndex);
					tempPlaintext += shiftedChar;
				}
				else {
					tempPlaintext += " ";
				}
			}
			plaintexts.add(tempPlaintext);
		}
		
		
		
		return plaintext;
	}
}