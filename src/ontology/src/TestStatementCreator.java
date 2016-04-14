import static org.junit.Assert.assertTrue;

import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.semanticweb.owlapi.model.OWLDataProperty;
import org.semanticweb.owlapi.model.OWLIndividualAxiom;
import org.semanticweb.owlapi.model.OWLNamedIndividual;

import main.java.application.Manager;
import main.java.application.StatementCreator;
import models.Statement;
import ontologyCategories.AreaType;
import ontologyCategories.DayType;
import ontologyCategories.EvidenceType;
import sparql.SparqlQuerier;

public class TestStatementCreator {

	static Manager manager;
	static Statement testStatement;
	static SparqlQuerier querier;
	final static String TEST_STATEMENT_NAME = "tweet1337";
	final static String TEST_STATEMENT_EVENT_NAME = "pizzaBrann";
	final static String TEST_STATEMENT_LOC = "Trondheim";
	final static String TEST_STATEMENT_EVIDENCE = EvidenceType.DRUGS;
	
	@BeforeClass
	public static void readOntology(){
		String fileName = "res/EmergencyOntology.owl";
		
		manager = new Manager();
		manager.init();
		manager.loadOntology(fileName);
		getTestStatement();
		
		querier = new SparqlQuerier(fileName);
		
		StatementCreator sc = new StatementCreator(manager);
		sc.addStatement(testStatement);
	}
	
	@AfterClass
	public static void tearDownAll(){
		Set<OWLNamedIndividual> individuals = new HashSet<>();
		OWLNamedIndividual i = manager.getNamedIndividual(TEST_STATEMENT_NAME);
		individuals.add(i);
		manager.removeIndividuals(individuals);
		manager.saveOntology();
	}
	
	public static void getTestStatement(){
		testStatement = new Statement();
		testStatement.setArea(TEST_STATEMENT_LOC);
		testStatement.setAreaType(AreaType.CITY);
		
		List<String> eventNames = Arrays.asList("personerSkadd","houseFire");
		List<String> eventTypes = Arrays.asList("Injuri","Fire");		
		
		testStatement.setEventNames(eventNames);
		testStatement.setEventTypes(eventTypes);
		testStatement.setEvidenceType(TEST_STATEMENT_EVIDENCE);
		testStatement.setStatementName(TEST_STATEMENT_NAME);
		testStatement.setDay(DayType.FRIDAY);
		
	}
	
	@Before
	public void setUp() throws Exception {
		
	}
	
	@After
	public void tearDown(){
		
		
	}

	@Test
	public void testStatementInstanceIsAdded(){
		Set<OWLNamedIndividual> individuals = manager.getAllIndividuals();
		boolean statementFound = false;
		
		for (OWLNamedIndividual owlNamedIndividual : individuals) {
			String shortClassName = owlNamedIndividual.getIRI().getShortForm();
			if(shortClassName.equals(TEST_STATEMENT_NAME)){
				statementFound = true;
				break;
			}
		}
		
		assertTrue(statementFound);
	}
	
	@Test
	public void testLocationAxiom() {
		OWLNamedIndividual testStatement = manager.getNamedIndividual(TEST_STATEMENT_NAME);
		OWLNamedIndividual trondheim = manager.getNamedIndividual(TEST_STATEMENT_LOC);
		Set<OWLIndividualAxiom> axiom = manager.getAxioms(testStatement);
		
		boolean locFound = false;
		for (OWLIndividualAxiom owlIndividualAxiom : axiom) {
			if(owlIndividualAxiom.containsEntityInSignature(trondheim)){
				locFound = true;
			}
		}
		// location == Trondheim
		// locationType == CITY
		assertTrue(locFound);
	}
	
	@Test
	public void testEventAxiom(){
		OWLNamedIndividual testStatment = manager.getNamedIndividual(TEST_STATEMENT_NAME);
		
		OWLNamedIndividual personerSkadd = manager.getNamedIndividual("personerSkadd");
		OWLNamedIndividual houseFire = manager.getNamedIndividual("houseFire");
		
		Set<OWLIndividualAxiom> axioms = manager.getAxioms(testStatment);
		boolean personerSkaddFound = false;
		boolean houseFireFound = false;
		for (OWLIndividualAxiom owlIndividualAxiom : axioms) {
			if (owlIndividualAxiom.containsEntityInSignature(personerSkadd)){
				personerSkaddFound = true;
			}
			if(owlIndividualAxiom.containsEntityInSignature(houseFire)){
				houseFireFound = true;
			}
		}
		assertTrue(personerSkaddFound);
		assertTrue(houseFireFound);
	}
	
	@Test
	public void testEvidenceAxiom(){
		OWLNamedIndividual testStatment = manager.getNamedIndividual(TEST_STATEMENT_NAME);
		OWLNamedIndividual evidence = manager.getNamedIndividual(TEST_STATEMENT_EVIDENCE+"Individual");
		Set<OWLIndividualAxiom> axioms = manager.getAxioms(testStatment);
		boolean locationFound = false;
		for (OWLIndividualAxiom owlIndividualAxiom : axioms) {
			if (owlIndividualAxiom.containsEntityInSignature(evidence)){
				locationFound = true;
				break;
			}
		}
		assertTrue(locationFound);
	}
	
	@Test
	public void testDataPropertAssumtions(){
		OWLNamedIndividual testStatment = manager.getNamedIndividual(TEST_STATEMENT_NAME);
		OWLDataProperty hasDay = manager.getDataProperty("hasDay");
		Set<OWLIndividualAxiom> axioms = manager.getAxioms(testStatment);
		boolean foundProp = false;
		for (OWLIndividualAxiom owlIndividualAxiom : axioms) {
			if(owlIndividualAxiom.containsEntityInSignature(hasDay)){
				System.out.println(owlIndividualAxiom);
				foundProp = true;
			}
		}
		assertTrue(foundProp);
		
	}
	
	

}
