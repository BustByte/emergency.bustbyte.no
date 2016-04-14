package main.java.application;

import java.io.File;
import java.io.IOException;
import java.util.List;

import categoriser.Categorizer;
import config.Config;
import database.Repo;
import models.Statement;
import models.Tweet;

public class Main {

	public static void main(String[] args) {/*
		System.out.println("Application started !");
	
		EventCreator eventCreator = new EventCreator();
		eventCreator.init(manager);
		AreaCreator areaCreator = new AreaCreator();
		areaCreator.init(manager);
		StatementCreator statementCreator = new StatementCreator(manager);
		
		statementCreator.addStatement(createTestStatement());
		
		System.out.println("Manager initiated !");
		
		Set<OWLClass> classes = manager.getAllClasses();
		for(OWLClass owlClass: classes){
			System.out.println(owlClass);
		}
		
//		eventCreator.addEventIndividual("tweet1statement", EventType.FIRE);
//		areaCreator.addAreaIndividual("Trondheim", AreaType.city);
		
		Set<OWLNamedIndividual> individuals= manager.getAllIndividuals();
		Set<OWLObjectProperty> properties = manager.getAllObjectProperties();
		
		System.out.println("Added fireEvent");
		
		System.out.println("Individuals:");
		for(OWLNamedIndividual individual: individuals){
			System.out.println(individual);
		}
		System.out.println("Result after query:");
		Querier querier = new Querier();
		querier.init(manager);
		System.out.println("Getting nodes with type fire");
		NodeSet<OWLNamedIndividual> result = querier.getEventWithType(EventType.TRAFFIC_COLLISION);
		for(Node<OWLNamedIndividual> individual: result){
			System.out.println(individual.getEntities());
		}
		
		StandardQuerier q = new StandardQuerier();
		q.init(manager.ontology);*/
		/*
		try {
			//int good = Runtime.getRuntime().exec("del res\\EmergencyOntologyTest.owl").exitValue();
			int good2= Runtime.getRuntime().exec("copy res\\EmergencyOntology.owl res\\EmergencyOntologyTest.owl").exitValue();
			if(good2 != 0 ) return ;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return;
		}*/

		Manager manager = new Manager();
		manager.init();
		manager.loadOntology(Config.ONTOLOGY_FILE_PATH);
		
		StatementCreator stCreator = new StatementCreator(manager);
		
		Repo repo = new Repo();
		repo.connect();
		
		List<Tweet> tweets = repo.getTweets(-1);
		List<Statement> sts = Categorizer.extractCategories(tweets);
		System.out.println("Inserting statements");
		int count = 1;
		for (Statement statement : sts) {
			if(count % 100 == 0){
				System.out.println(count);
			}
			stCreator.addStatement(statement);
			count++;
		}
		manager.saveOntology();
		System.out.println("Finished");
	}
	
	public static void reCreateOntology(){
		Manager manager = new Manager();
		manager.init();
		manager.loadOntology(Config.ONTOLOGY_FILE_PATH);
		
		StatementCreator stCreator = new StatementCreator(manager);
		
		Repo repo = new Repo();
		repo.connect();
		
		List<Tweet> tweets = repo.getTweets(-1);
		List<Statement> sts = Categorizer.extractCategories(tweets);
		System.out.println("Inserting statements");
		int count = 1;
		for (Statement statement : sts) {
			if(count % 100 == 0){
				System.out.println(count);
			}
			stCreator.addStatement(statement);
			count++;
		}
		manager.saveOntology();
		System.out.println("Finished");
	}
	
	public static Statement createTestStatement(){
		/*
		Statement statement = new Statement();
		statement.setStatementName("tweet1statement");
		statement.setArea("Trondheim");
		statement.setEventName("tweet1event");
		statement.setEventType(EventType.TRAFFIC_COLLISION);
		*/
		return null;
	}
	
	
	
}
