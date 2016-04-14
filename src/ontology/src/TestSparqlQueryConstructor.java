

import static org.junit.Assert.assertEquals;

import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLNamedIndividual;

import main.java.application.Manager;
import ontologyCategories.EventType;
import sparql.SparqlQueryConstructor;

public class TestSparqlQueryConstructor {

	static OWLClass owlClass;
	static OWLNamedIndividual individual;
	static SparqlQueryConstructor constructor;
	
	
	@BeforeClass
	public static void initOnce(){
		String fileName = "res/EmergencyOntologyTest.owl";
		Manager manager = new Manager();
		manager.init();
		manager.loadOntology(fileName);
		owlClass = manager.getClass(EventType.TRAFFIC_COLLISION);
		individual = manager.getNamedIndividual("Trondheim");
	}
	
	@Before
	public void setUp() throws Exception {
		constructor = new SparqlQueryConstructor();
	}

	@Test
	public void testGetOwlClassSuffix() {
		String classSuffix = constructor.getOWLClassSuffix(owlClass);
		assertEquals(classSuffix, EventType.TRAFFIC_COLLISION);
	}
	
	@Test
	public void testGetOWLIndividSuffix(){
		String indSuffix = constructor.getOWLNamedIndividualSuffix(individual);
		assertEquals(indSuffix, "Trondheim");
	}
	
	@Test
	public void testGetStatementWithType(){
		String query = constructor.getStatementsWithEventsOfType(owlClass);
		//System.out.println(query);
		
	}
	
	@Test
	public void testGetStatementsWithLocation(){
		String query = constructor.getStatementsWithLocation(individual);
		System.out.println(query);
	}
	
	@Test
	public void testGetSubjectsWithHasDay(){
		String query = constructor.getSubjectWithHasDay("adskl");
		System.out.println(query);
		
	}

}
