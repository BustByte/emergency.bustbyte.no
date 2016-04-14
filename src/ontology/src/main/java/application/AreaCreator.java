package main.java.application;

import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLClassAssertionAxiom;
import org.semanticweb.owlapi.model.OWLNamedIndividual;
import org.semanticweb.owlapi.model.parameters.ChangeApplied;

public class AreaCreator {

	Manager manager;
	
	public void init(Manager manager){
		this.manager = manager;
	}
	
	/**
	 * Use "enum-type" areaType to always have consistent classes of areas
	 * @param name
	 * @param areaType
	 */
	public void addAreaIndividual(String individualName, String areaType){
		OWLNamedIndividual individual = manager.getNamedIndividual(individualName);
		OWLClass specificAreaSubclass = getAreaClass(areaType);
		ChangeApplied changeApplied = manager.createAndAddClassAssertion(specificAreaSubclass, individual);
		manager.saveOntology();
	}
	
	private OWLClass getAreaClass(String areaName){
		return manager.getClass(areaName);
	}
	
}
