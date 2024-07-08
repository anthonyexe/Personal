
public class Tester {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Quiz q = new Quiz("Drake", "Drake.csv");
		
		//q.printSongQuotes();
		//String[][] lyricQuiz = q.generateQuiz();
		
		//for (int i = 0; i < lyricQuiz.length; i++) {
			//for (int j = 0; j < lyricQuiz[i].length; j++) {
				//System.out.println(lyricQuiz[i][j]);
			//}
			//System.out.println("------------------------------------------");
		//}
		//q.printSongTitles();
		q.takeQuiz();
	}

}
