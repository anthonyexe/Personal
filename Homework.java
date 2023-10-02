import java.util.*;
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
	
	public HashMap<Character, Double> sortFrequencyHashMap(HashMap<Character, Double> frequencyMap) {
		HashMap<Character, Double> sortedFrequencies = new HashMap<Character, Double>();
		ArrayList<Double> frequencies = new ArrayList<Double>();
		
		for(Map.Entry<Character, Double> entry : sortedFrequencies.entrySet()) {
			frequencies.add(entry.getValue());
		}
		
		Collections.sort(frequencies);
		
		for(Double num : frequencies) {
			
		}
	}
	
	public ArrayList<Character> shiftCipherDecryption(String ciphertext) {
		HashMap<Integer, Character> alphabet = initializeAlphabet();
		HashMap<Character, Double> relativeFrequencies = frequencyAnalysis(ciphertext);
		ArrayList<Character> mostCommonChars = new ArrayList<Character>(5);
		String plaintext;
		int key;
		
		Set<Character> keys = relativeFrequencies.keySet();
		
		int count = 0;
		Character greatestKey = 'a';
		Character lastGreatestKey = null;
		Double greatestFrequency = 0.0;
		Integer greatestIndex;
		for (int i = 0; i < 5; i++) {
			for (Character currentChar : keys) {
				if (currentChar != lastGreatestKey) {
					if (count == 0) {
						greatestKey = currentChar;
						greatestFrequency = relativeFrequencies.get(currentChar);
					}
					else if (greatestFrequency < relativeFrequencies.get(currentChar)) {
						greatestKey = currentChar;
						greatestFrequency = relativeFrequencies.get(currentChar);
					}
				}
				
				count++;
				lastGreatestKey = greatestKey;
			}
			mostCommonChars.add(greatestKey);
			//keys.remove(greatestKey);
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
		
		
		greatestIndex = topKey - 'a' + 1;
		key = Math.abs(greatestIndex - 4);
		
		plaintext = alphabeticShift(ciphertext, key);
		
		return mostCommonChars;
	}
	
	public String affineCipherEncryption(String plaintext, int[] key) {
		String ciphertext = "";
		
		HashMap<Integer, Character> alphabet = initializeAlphabet();
		int[] coprimeKeys = {1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25};
		List coprimeKeyList = Arrays.asList(coprimeKeys);
		
		if (key.length != 2 || (!coprimeKeyList.contains(key[0])) || (key[1] > 25 || key[1] < 1)) {
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
	
	public String affineCipherDecryption(String ciphertext) {
		String plaintext = " ";
		
		return plaintext;
	}
}
