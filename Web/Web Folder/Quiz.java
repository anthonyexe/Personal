//Ant
import java.util.*;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.IOException;


public class Quiz {
	private String artist;
	private int songCount = 0;
	private HashMap<String, String[]> songQuotes = new HashMap<String, String[]>();
	private ArrayList<String> songTitles = new ArrayList<String>();
	
	public Quiz(String artistName, String file) {
		artist = artistName;
		
		try (BufferedReader br = new BufferedReader(new FileReader(file))) {
			String line;
			while((line = br.readLine()) != null) {
				List<String> values = new LinkedList<String>(Arrays.asList(line.split(";")));
				String song = values.get(0);
				values.remove(0);
				String[] quotes = new String[values.size()];
				quotes = values.toArray(quotes);
				songQuotes.put(song, quotes);
				songTitles.add(song);
				songCount++;
			}
		}
		catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public void printSongQuotes() {
		System.out.println(songCount);
		for (String name: songQuotes.keySet()) {
			String key = name.toString();
			String[] quotes = songQuotes.get(key);
			System.out.println(key + "\n" + "---------------------");
			for (int i = 0; i < quotes.length; i++) {
				System.out.println(quotes[i] + "\n");
			}
		}
	}
	
	public void printSongTitles() {
		for (int i = 0; i < songTitles.size(); i++) {
			System.out.println(songTitles.get(i));
		}
	}
	
	public String[][] generateQuiz() {
		// Random object
		Random rand = new Random();
		// 2-D Array to hold song names and a random quote from each song
		String[][] lyricQuiz = new String[songCount][2];
		int rowCount = 0;
		// Loop through keySet of songQuote HashMap
		for (String name: songQuotes.keySet()) {
			// Store current key in String variable
			String key = name.toString();
			// Store current String array at current Key value
			String[] quotes = songQuotes.get(key);
			// Generate random number in range of current String array length
			int randNum = rand.nextInt(quotes.length);
			// Store current song name in first column position of the current row
			lyricQuiz[rowCount][0] = key;
			// Store random quote in the second column position of the current row
			lyricQuiz[rowCount][1] = quotes[randNum];
			rowCount++;
		}
		
		int lyricQuizLength = lyricQuiz.length; 
		ArrayList<Integer> indexList = new ArrayList<Integer>(lyricQuizLength);
		for (int i = 0; i < lyricQuizLength; i++) {
			indexList.add(i);
		}
		
		Collections.shuffle(indexList);
		String[][] shuffledQuiz = new String[songCount][2];
		
		for (int i = 0; i < lyricQuizLength; i++) {
			int shuffledIndex = indexList.get(i);
			shuffledQuiz[i][0] = lyricQuiz[shuffledIndex][0];
			shuffledQuiz[i][1] = lyricQuiz[shuffledIndex][1];
		}
		return shuffledQuiz;
	}
	
	public void takeQuiz() {
		Scanner scan = new Scanner(System.in);
		String[][] lyricQuiz = generateQuiz();
		int totalQuestions = lyricQuiz.length;
		double correctCount = 0.0;
		double percentageResults;
		for (int i = 0; i < lyricQuiz.length; i++) {
			System.out.println(lyricQuiz[i][1]);
			System.out.println("----------------------------------------");
			for (int j = 0; j < songTitles.size(); j++) {
				System.out.println(songTitles.get(j));
			}
			System.out.println("\nEnter the correct song title: ");
			String input = scan.nextLine();
			
			if (input.equals(lyricQuiz[i][0])) {
				System.out.println("Correct!");
				correctCount++;
			}
			else {
				System.out.println("Incorrect!");
			}
			songTitles.remove(lyricQuiz[i][0]);
		}
		percentageResults = (correctCount / totalQuestions) * 100;
		System.out.println("----------------------------------------");
		System.out.println("Your results are: " + percentageResults + "%");
	}
}
