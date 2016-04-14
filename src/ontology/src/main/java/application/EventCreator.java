package main.java.application;

import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLClassAssertionAxiom;
import org.semanticweb.owlapi.model.OWLNamedIndividual;
import org.semanticweb.owlapi.model.parameters.ChangeApplied;

public class EventCreator {

	Manager manager;
	
	public void init(Manager manager){
		this.manager = manager;
	}
	
	public void addEventIndividual(String eventName, String eventType){
		OWLNamedIndividual event = manager.getNamedIndividual(eventName);
		OWLClass eventClass = getEventClass(eventType);
		
		// Save individual to ontology
		manager.saveNamedIndividal(event);

		// Save class assertion to ontology
		ChangeApplied change = manager.createAndAddClassAssertion(eventClass, event);
		// Save ontology
		manager.saveOntology();
	}
	
	private OWLClass getEventClass(String eventClass){
		return manager.getClass(eventClass);
	}
	
	
}
