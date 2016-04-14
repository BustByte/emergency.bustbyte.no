package main.java.application;

import java.util.List;

import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLNamedIndividual;
import org.semanticweb.owlapi.model.OWLObjectProperty;
import org.semanticweb.owlapi.model.parameters.ChangeApplied;

import models.Statement;
import ontologyCategories.StatementType;

public class StatementCreator {
	
	Manager manager;
	final static String hasLocationPropertyName = "hasLocation";
	final static String hasEventPropertyName = "hasEvent";
	final static String hasEvidencePropertyName = "hasEvidence";
	final static String isEvidenceOfName = "isEvidenceOf";
	OWLNamedIndividual individualStatement;
	
	public StatementCreator(Manager manager){
		init(manager);
	}
	
	public void init(Manager manager){
		this.manager = manager;
	}

	/**
	 * This method is supposed to add all statement individual and then add object properties to area and event 
	 * @param statement
	 * @return
	 */
	public boolean addStatement(Statement statement){
		
		
		// create statement individual
		individualStatement = createStatementInidividual(statement.getStatementName());
		
		// set weekday on statement
		if(statement.getDay() != null){
			manager.addDataPropAssertion("hasDay", individualStatement, statement.getDay());
		}
		
		// get area
		if(statement.getArea() != null){
			System.out.println("About to add area: "+statement.getArea());
			OWLNamedIndividual area = manager.getNamedIndividual(statement.getArea());
			OWLObjectProperty hasLocation = manager.getObjectProperty(hasLocationPropertyName);
			manager.createAndAddPropertyAssertion(individualStatement, area, hasLocation);			
		}
		
		// add event assertions
		if(statement.getEventTypes().size() != 0){
			addEventsAssertion(statement.getEventNames(), statement.getEventTypes());
		}
		
		// get evidence
		if(statement.getEvidenceType() != null){
			OWLNamedIndividual evidence = manager.getNamedIndividual(statement.getEvidenceType()+"Individual");			
			OWLObjectProperty isEvidenceOf = manager.getObjectProperty(isEvidenceOfName);
			//OWLObjectProperty hasEvidence = manager.getObjectProperty(hasEvidencePropertyName);
			manager.createAndAddPropertyAssertion(evidence, individualStatement, isEvidenceOf);
		}

		return true;
	}
	
	private OWLNamedIndividual createStatementInidividual(String name){
		OWLNamedIndividual individual = manager.getNamedIndividual(name);
		OWLClass statementClass = getStatementClass();
		ChangeApplied change = manager.createAndAddClassAssertion(statementClass, individual);
		return individual;
	}
	
	private OWLClass getStatementClass(){
		return manager.getClass(StatementType.STATEMENT);
	}
	
	public void addEventIndividual(String eventName, String eventType){
		EventCreator eventCreator = new EventCreator();
		eventCreator.init(manager);
		eventCreator.addEventIndividual(eventName, eventType);
	}
	
	public void addEventsAssertion(List<String> events, List<String> eventTypes){
		for (int i = 0; i<events.size(); i++) {
			OWLClass eventType = manager.getClass(eventTypes.get(i));
			OWLNamedIndividual eventIndividual = manager.getNamedIndividual(events.get(i));
			OWLObjectProperty hasEvent = manager.getObjectProperty(hasEventPropertyName);
			
			manager.createAndAddClassAssertion(eventType, eventIndividual);
			manager.createAndAddPropertyAssertion(individualStatement, eventIndividual, hasEvent);
			
		}
	}
	
	
}
