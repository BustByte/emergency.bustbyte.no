import static org.junit.Assert.*;

import org.junit.Before;
import org.junit.Test;

import database.Repo;

public class TestRepo {

	Repo repo;
	
	@Before
	public void setUp() throws Exception {
		repo = new Repo();
	}

	@Test
	public void testConnect() {
		repo.connect();
	}

	@Test
	public void testFillStatement(){
		// indexes : 0 = area, 1 = event, 2 = eventType, 3 = evidenceType
		/*
		String[] info = {"Trondheim", "husBrann", "Robbery", "Evidence"};
		models.Statement st = Repo.fillStatement(info);
		assertEquals("Trondheim", st.getArea());
		assertEquals("husBrann", st.getEventNames().get(0));
		assertEquals("Robbery", st.getEventTypes().get(0));
		assertEquals("Evidence", st.getEvidenceType());*/
		
	}
	
	@Test
	public void testGetTweets(){
		repo.connect();
		repo.getTweets(10);
		// Test that there is no errors
	}
}
