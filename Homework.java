import java.util.*;

public class Homework {
	public HashMap<Character, Double> relativeFrequencies(String plaintext) {
		HashMap<Character, Integer> frequencies = new HashMap<Character, Integer>();
		HashMap<Character, Double> rFrequencies = new HashMap<Character, Double>(frequencies.size());
		int count = 0;
		
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
				Double currentRelativeFrequency = Double.valueOf(frequencies.get(currentChar) / count);
				rFrequencies.put(currentChar, currentRelativeFrequency);
			}
		}
		return rFrequencies;
	}
}
