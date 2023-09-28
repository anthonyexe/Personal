import java.util.*;
import java.text.DecimalFormat;

public class Homework {
	public HashMap<Character, Double> relativeFrequencies(String plaintext) {
		HashMap<Character, Integer> frequencies = new HashMap<Character, Integer>();
		HashMap<Character, Double> rFrequencies = new HashMap<Character, Double>(frequencies.size());
		DecimalFormat df = new DecimalFormat("#.000");
		double count = 0;
		
		for (int i = 0; i < plaintext.length(); i++) {
			count++;
			Character current = Character.toLowerCase(plaintext.charAt(i));
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
	
	public String shiftCipherEncryption(String plaintext, int key) {
		final int alphabetSize = 26;
		HashMap<Integer, Character> alphabet = new HashMap<Integer, Character>(alphabetSize);
		String ciphertext = "";
		
		if (key > 25 || key < 0) {
			return "Invalid Key";
		}
		
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
		
		for (int i = 0; i < plaintext.length(); i++) {
			Character current = Character.toLowerCase(plaintext.charAt(i));
			
			if (!Character.isWhitespace(current)) {
				Integer currentIndex = current - 'a' + 1;
				Integer shiftedIndex = (currentIndex + key) % 26;
				
				Character shiftedChar = alphabet.get(shiftedIndex);
				ciphertext += shiftedChar;
			}
		}
		return ciphertext;
	}
	
	public String shiftCipherDecryption(String ciphertext) {
		String plaintext = "";
		
		
		return plaintext;
	}
}
