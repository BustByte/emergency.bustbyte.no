import static org.junit.Assert.assertTrue;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLClassAxiom;
import org.semanticweb.owlapi.model.OWLIndividualAxiom;
import org.semanticweb.owlapi.model.OWLNamedIndividual;

import main.java.application.Manager;
import main.java.application.StatementCreator;
import models.Statement;
import ontologyCategories.AreaType;
import ontologyCategories.EventType;
import ontologyCategories.StatementType;

public class TestManager {

	static Manager manager;
	static Statement testStatement;
	final static String TEST_STATEMENT_NAME = "tweet1337";
	
	@BeforeClass
	public static void init(){
		String fileName = "res/EmergencyOntology.owl";
		manager = new Manager();
		manager.init();
		manager.loadOntology(fileName);
		getTestStatement();
		StatementCreator sc = new StatementCreator(manager);
		sc.addStatement(testStatement);
	}
	
	
	public static void tearDownAll(){
		Set<OWLNamedIndividual> individuals = new HashSet<>();
		OWLNamedIndividual i = manager.getNamedIndividual(TEST_STATEMENT_NAME);
		individuals.add(i);
		manager.removeIndividuals(individuals);
		manager.saveOntology();
	}
	
	public static void getTestStatement(){
		testStatement = new Statement();
		testStatement.setArea("Trondheim");
		testStatement.setAreaType(AreaType.CITY);
		String[] eventNames = {"pizzaBrann"};
		testStatement.setEventNames(Arrays.asList(eventNames));
		String[] eventTypes = {EventType.FIRE};
		testStatement.setEventTypes(Arrays.asList(eventTypes));
		//testStatement.setEvidence(evidence);
		//testStatement.setEventType(eventType);
		testStatement.setStatementName(TEST_STATEMENT_NAME);
	}
	
	@Before
	public void setUp() throws Exception {
		
	}

	@Test
	public void testGetIndividualAxioms() {
		OWLNamedIndividual in = manager.getNamedIndividual(TEST_STATEMENT_NAME);
		Set<OWLIndividualAxiom> axioms = manager.getAxioms(in);
		
		boolean foundClass = false;
		for(OWLIndividualAxiom axiom : axioms){
			OWLNamedIndividual trondheim = axiom.getIndividualsInSignature().iterator().next();
			if(trondheim.getIRI().getShortForm().equals("Trondheim")){
				foundClass = true;
				break;
			}
			
		}
		assertTrue(foundClass);
	}
	
	@Test
	public void testGetClassAxioms() {
		OWLNamedIndividual in = manager.getNamedIndividual(TEST_STATEMENT_NAME);
		Set<OWLIndividualAxiom> axioms = manager.getAxioms(in);
		
		boolean foundClass = false;
		for(OWLIndividualAxiom axiom : axioms){
			OWLClass statementClass = axiom.getClassesInSignature().iterator().next();
			System.out.println(statementClass);
			if(statementClass.getIRI().getShortForm().equals(StatementType.STATEMENT)){
				foundClass = true;
				break;
			}
			
		}
		assertTrue(foundClass);
	}
	
	
	
	

}
