package main.java.application;

import static org.junit.Assert.assertTrue;

import java.util.Scanner;
import java.util.Set;

import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLNamedIndividual;

import config.Config;
import ontologyCategories.EvidenceType;

public class TestStandardQuerier {

	static StandardQuerier querier;
	static Manager manager;
	
	@BeforeClass
	public static void init(){
		manager = new Manager();
		manager.init();
		manager.loadOntology(Config.ONTOLOGY_FILE_PATH);
		
		querier = new StandardQuerier();
		querier.init(manager.ontology);
	}
	
	@Before
	public void setUp() throws Exception {
		
	}

	@Test
	public void testGetInstances() {
		OWLClass trafficCollision = manager.getClass(EvidenceType.DRUGS);
		Scanner sc = new Scanner(System.in);
		String command = "";
		while(!command.equals("exit")){
			command = sc.nextLine();
			OWLClass cls = manager.getClass(command);
			Set<OWLNamedIndividual> inds = querier.getInstances(cls, false);
			System.out.println("Amount :"+inds.size());
			System.out.println("Print ? (y/n)");
			command = sc.nextLine();
			if(command.equals("y")){
				for(OWLNamedIndividual i : inds){
					System.out.println(i);
				}
			}
		}
		Set<OWLNamedIndividual> instances = querier.getInstances(trafficCollision, true);
		assertTrue(instances.size()>0);
		
	}

	@Test
	public void testGetSuperClasses() {

	}
	
	@Test
	public void testGetSubClasses() {

	}
	
	@Test
	public void testGetEquivalentClasses() {

	}
}
