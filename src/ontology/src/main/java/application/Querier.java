package main.java.application;

import org.semanticweb.owlapi.model.OWLNamedIndividual;
import org.semanticweb.owlapi.model.OWLObjectProperty;
import org.semanticweb.owlapi.model.OWLObjectPropertyExpression;
import org.semanticweb.owlapi.reasoner.NodeSet;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.OWLReasonerFactory;
import org.semanticweb.owlapi.reasoner.structural.StructuralReasonerFactory;

import ontologyCategories.EventType;
import ontologyCategories.PropertyTypes;

public class Querier {
	
	Manager manager;
	OWLReasoner reasoner;
	boolean consistent;
	
	public void init(Manager manager){
		this.manager = manager;
		consistent = initReasoner();
	}
	
	private boolean initReasoner(){
		OWLReasonerFactory reasonerFactory = new StructuralReasonerFactory();
		OWLReasoner reasoner = reasonerFactory.createReasoner(manager.ontology);
		reasoner.precomputeInferences();
		this.reasoner = reasoner;
		return reasoner.isConsistent();
	}
	
	public NodeSet<OWLNamedIndividual> getEventWithType(String eventType){
		
		// Trying to get all NamedIndividuals that hasLocation "Trondheim"
		OWLObjectProperty prop = manager.getObjectProperty(PropertyTypes.hasLocationPropertyName);
		OWLNamedIndividual location = manager.getNamedIndividual("Trondheim");
		
		NodeSet<OWLNamedIndividual> individuals = reasoner.getObjectPropertyValues(location, prop);
		return individuals;
		
	}
	
}
