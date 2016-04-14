import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import java.util.ArrayList;
import java.util.List;

import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;

import categoriser.Categorizer;
import database.Repo;
import models.Statement;
import models.Tweet;
import ontologyCategories.DayType;

public class TestCategorizer {

	static List<Tweet> tweets;
	static int tweetCount = 300000;
	
	
	public static void getExampleTweets(){
		Repo repo = new Repo();
		repo.connect();
		tweets = repo.getTweets(tweetCount);
	}
	
	@Before
	public void setUp() throws Exception {
	}

	@Ignore
	@Test
	public void testEventCategorizer() {
		List<Statement> statements = new ArrayList<>();
		//Scanner sc = new Scanner(System.in);
		for(Tweet t : tweets){
			Statement st = Categorizer.extractCategories(t);
			// Inspect statements here
			/*
			if(st == null){
				System.out.println("Uncategorized tweet :");
				System.out.println(t.getContent());
				//sc.nextLine();
			}*/
			
			
			if( st != null ) statements.add(st);
		}
		int categorized = statements.size();
		double percent = (double)categorized/(double)tweetCount;
		System.out.println("Tweets categorized by event: "+categorized);
		System.out.println(percent*100 + " prosent");
		
	}
	
	@Ignore
	@Test
	public void testEvidenceCategorizer() {
		List<Statement> statements = new ArrayList<>();
		//Scanner sc = new Scanner(System.in);
		for(Tweet t : tweets){
			Statement st = Categorizer.extractCategories(t);
			// Inspect statements here
			/*
			if(st == null){
				System.out.println("Uncategorized tweet :");
				System.out.println(t.getContent());
				//sc.nextLine();
			}*/
			
			
			if( st.getEvidenceType() != null ) statements.add(st);
		}
		int categorized = statements.size();
		double percent = (double)categorized/(double)tweetCount;
		System.out.println("Tweets categorized by event: "+categorized);
		System.out.println(percent*100 + " prosent");
		
	}
	
	@Ignore
	@Test
	public void testExample(){
		String content = "vi er på stedet, en mann pågrepet, funn av startpistol, forts";
		String evidence = Categorizer.extractEvidenceCategory(content);
		assertEquals(evidence,ontologyCategories.EvidenceType.GUN);
		//System.out.println(eventTypes);
	}

	@Ignore
	@Test
	public void testReturnNullWhenNoEventOrEvidence(){
		String message = "asdfasdf";
		String evidence = Categorizer.extractEvidenceCategory(message);
		boolean b = evidence == null;
		assertEquals(b, true);
		String message2 = "asdfjkasdjkf asdfjk gun asdfsjdf";
		String evidence2 = Categorizer.extractEvidenceCategory(message2);
		boolean b2 = evidence2 == null;
		assertEquals(b2, true);
		
	}

	@Ignore
	@Test
	public void testReturnRate(){
		List<Statement> sts = Categorizer.extractCategories(tweets);
		double rate = (double)sts.size()/(double)tweetCount;
		System.out.println("Total count : "+sts.size());
		System.out.println("Total extraction rate : "+rate);
	}
	
	@Ignore
	@Test
	public void testWeekDayExtractor(){
		String timestamp = "2016-02-19 16:35:06";
		String weekday = Categorizer.extractWeekday(timestamp);
		assertEquals(weekday, DayType.FRIDAY);
		
	}
	
	@Test
	public void testLegalPrefix(){
		String a = " asdf ";
		String b = ",asdf ";
		String c = ".asdf ";
		String d = "uasdf ";
		String e = "asdf ";
		int index = 1;
		
		assertTrue(Categorizer.legalPrefix(a, index ));	
		assertTrue(Categorizer.legalPrefix(b, index ));	
		assertTrue(Categorizer.legalPrefix(c, index ));
		assertFalse(Categorizer.legalPrefix(d, index ));	
		assertTrue(Categorizer.legalPrefix(e, index-1 ));
	}
	
	@Test
	public void testLegalSuffix(){
		String a = " asdf.";
		String b = " asdf ";
		String c = " asdf,";
		String d = " asdfu";
		String e = " asdf";
		int index = 1;
		int wordLength = 4;
		
		assertTrue(Categorizer.legalSuffix(a, index, wordLength));	
		assertTrue(Categorizer.legalSuffix(b, index, wordLength));	
		assertTrue(Categorizer.legalSuffix(c, index, wordLength));
		assertFalse(Categorizer.legalSuffix(d, index, wordLength));	
		assertTrue(Categorizer.legalSuffix(e, index, wordLength));
		
	}
}
