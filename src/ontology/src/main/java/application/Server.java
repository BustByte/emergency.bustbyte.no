package main.java.application;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLNamedIndividual;
import org.semanticweb.owlapi.model.OWLObjectProperty;
import org.semanticweb.owlapi.reasoner.Node;
import org.semanticweb.owlapi.reasoner.NodeSet;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.google.common.collect.Sets;

import categoriser.Categorizer;
import config.Config;
import models.Statement;
import models.Tweet;
import ontologyCategories.EventType;
import ontologyCategories.EvidenceType;

@RestController
public class Server {
	
	static final String IS_EVIDENCE_OF = "isEvidenceOf";
	StandardQuerier querier;
	static Manager manager;
	StatementCreator statementCreator;
	
	public Server(){
		init();
	}
	
	public void init(){
		manager = new Manager();
		manager.init();
		manager.loadOntology(Config.ONTOLOGY_FILE_PATH);
		
		querier = new StandardQuerier();
		querier.init(manager.ontology);
		System.out.println("Setup finished");
	}
	
	public Set<String> getInstancesOfEvidenceType(String evidenceType){
		OWLNamedIndividual individual = manager.getNamedIndividual(evidenceType+"Individual");
		OWLObjectProperty isEvidenceOf = manager.getObjectProperty(IS_EVIDENCE_OF);
		NodeSet<OWLNamedIndividual> nodeSet = querier.getObjectPropertyDomainsValues(individual, isEvidenceOf);
		return getTweetIdsFromStatements(nodeSet);
	}
	
	
	public Set<String> getTweetIdsFromStatements(NodeSet<OWLNamedIndividual> inds){
		Set<String> ids = new HashSet<>();
		for (Node<OWLNamedIndividual> node : inds) {
			for(OWLNamedIndividual ind : node.getEntities()){
				String id = ind.getIRI().getShortForm().split("#")[1];
				ids.add(id);
			}
				
		}
		return ids;
	}
	
	public List<String> getInstancesOfClass(OWLClass cls){
		Set<OWLNamedIndividual> inds = querier.getInstances(cls, false);
		return getTweetIds(inds);
	}
	
	public static String getIdString(OWLNamedIndividual ind){
		String[] splitted = ind.getIRI().toString().split("#");
		if(splitted.length != 2) return null;
		String suffix = splitted[1];
		if(suffix.length()<18) return null;
		String id = suffix.substring(0, 18);
		return id;
	}
	
	public List<String> getTweetIds(Set<OWLNamedIndividual> individuals){
		List<String> tweetIds = new ArrayList<>();
		for (OWLNamedIndividual individual : individuals) {
			String id = getIdString(individual);
			if( id != null) tweetIds.add(id);
		}
		return tweetIds;
	}
	
	@RequestMapping(value= "/trafficCollision" , method = RequestMethod.GET)
	public List<String> getTrafficCollisionTweets(){
		OWLClass trafficCollision = manager.getClass(EventType.TRAFFIC_COLLISION);
		List<String> ids = getInstancesOfClass(trafficCollision);
		return ids;
	}
	
	@RequestMapping(value= "/injury" , method = RequestMethod.GET)
	public List<String> getInjuriTweets(){
		OWLClass injury = manager.getClass(EventType.INJURY);
		List<String> ids = getInstancesOfClass(injury);
		return ids;
	}
	
	@RequestMapping(value= "/violence" , method = RequestMethod.GET)
	public List<String> getViolenceTweets(){
		OWLClass violence = manager.getClass(EventType.VIOLENCE);
		List<String> ids = getInstancesOfClass(violence);
		System.out.println(ids.size());
		System.out.println("Returning tweets");
		return ids;
	}
	
	@RequestMapping(value= "/search" , method = RequestMethod.GET)
	public List<String> getSearchTweets(){
		OWLClass search = manager.getClass(EventType.SEARCH);
		List<String> ids = getInstancesOfClass(search);
		return ids;
	}
	
	@RequestMapping(value= "/crime" , method = RequestMethod.GET)
	public List<String> getCrimeTweets(){
		OWLClass crime = manager.getClass(EventType.CRIME);
		List<String> ids = getInstancesOfClass(crime);
		return ids;
	}
	
	@RequestMapping(value= "/robbery" , method = RequestMethod.GET)
	public List<String> getRobberyTweets(){
		OWLClass robbery = manager.getClass(EventType.ROBBERY);
		List<String> ids = getInstancesOfClass(robbery);
		return ids;
	}
	
	@RequestMapping(value= "/drugs" , method = RequestMethod.GET)
	public List<String> getDrugsTweets(){
		OWLClass drugs = manager.getClass(EvidenceType.DRUGS);
		List<String> ids = getInstancesOfClass(drugs);
		return ids;
	}
	
	@RequestMapping(value= "/gun" , method = RequestMethod.GET)
	public List<String> getGunTweets(){
		OWLClass gun = manager.getClass(EvidenceType.GUN);
		List<String> ids = getInstancesOfClass(gun);
		return ids;
	}
	
	@RequestMapping(value= "/owlapi" , method = RequestMethod.GET)
	public Collection<String> getTweets(@RequestParam Map<String,String> params){
		String event = params.get("event");
		String evidence = params.get("evidence");
		System.out.println("Event :"+event);
		System.out.println("Evidence :"+evidence);
		if(event == null && evidence == null ) return null;
		OWLClass eventCls = getEventClass(event);
		OWLClass evidenceCls = getEventClass(evidence);
		
		if(event == null ){
			return getInstancesOfEvidenceType(evidence);
		}
		else if(evidence == null){
			return getInstancesOfClass(eventCls);
		}
		else{
			Set<String> set = new HashSet<>(getInstancesOfClass(eventCls));
			Set<String> set2 = new HashSet<>(getInstancesOfEvidenceType(evidence));
			return Sets.intersection(set, set2);
		}
	}
	
	@RequestMapping(value= "/addTweet" , method = RequestMethod.POST)
	public void addTweet(@RequestBody List<Tweet> tweets){
		if(tweets == null) return;
		
		if(statementCreator == null){
			statementCreator = new StatementCreator(manager);
		}
		
		for(Tweet t : tweets){
			Statement st = Categorizer.extractCategories(t);
			statementCreator.addStatement(st);			
		}
		
	}
	
	public OWLClass getEventClass(String event){
		if(event == null) return null;
		if(event.equals(EventType.FIRE)){
			return manager.getClass(EventType.FIRE);
		}
		else if(event.equals(EventType.INJURY)){
			return manager.getClass(EventType.INJURY);
		}
		else if(event.equals(EventType.ROBBERY)){
			return manager.getClass(EventType.ROBBERY);
		}
		else if(event.equals(EventType.SEARCH)){
			return manager.getClass(EventType.SEARCH);
		}
		else if(event.equals(EventType.TRAFFIC_COLLISION)){
			return manager.getClass(EventType.TRAFFIC_COLLISION);
		}
		else if(event.equals(EventType.VIOLENCE)){
			return manager.getClass(EventType.VIOLENCE);
		}
		return null;
	}
	
	public OWLClass getEvidenceClass(String evidence){
		if(evidence == null) return null;
		if(evidence.equals(EvidenceType.DRUGS)){
			return manager.getClass(EvidenceType.DRUGS);
		}
		else if(evidence.equals(EvidenceType.GUN)){
			return manager.getClass(EvidenceType.GUN);
		}
		return null;
	}
	
	
	
	
	
}
