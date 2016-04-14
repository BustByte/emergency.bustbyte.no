package main.java.application;

import java.util.Collection;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.IRI;
import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLClassAssertionAxiom;
import org.semanticweb.owlapi.model.OWLClassAxiom;
import org.semanticweb.owlapi.model.OWLDataFactory;
import org.semanticweb.owlapi.model.OWLDataProperty;
import org.semanticweb.owlapi.model.OWLDataPropertyAssertionAxiom;
import org.semanticweb.owlapi.model.OWLDeclarationAxiom;
import org.semanticweb.owlapi.model.OWLEntity;
import org.semanticweb.owlapi.model.OWLIndividualAxiom;
import org.semanticweb.owlapi.model.OWLLiteral;
import org.semanticweb.owlapi.model.OWLNamedIndividual;
import org.semanticweb.owlapi.model.OWLObjectProperty;
import org.semanticweb.owlapi.model.OWLObjectPropertyAssertionAxiom;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.model.OWLOntologyStorageException;
import org.semanticweb.owlapi.model.PrefixManager;
import org.semanticweb.owlapi.model.RemoveAxiom;
import org.semanticweb.owlapi.model.parameters.ChangeApplied;
import org.semanticweb.owlapi.util.DefaultPrefixManager;
import org.semanticweb.owlapi.util.OWLEntityRemover;

import main.java.loader.OntologyLoader;

public class Manager {

	OWLOntology ontology;
	OWLOntologyManager manager;
	IRI ontologyIRI;
	OWLDataFactory factory;
	PrefixManager prefixManager;
	
	/* OWLClasses that are commonly used */
	OWLClass fireEventClass;
	
	public void init(){
		manager = OWLManager.createOWLOntologyManager();
	}
	
	public void loadOntology(String filename){
		OntologyLoader.setManager(manager);
		ontology = OntologyLoader.loadOntology(filename);
//		ontologyIRI = manager.getOntologyDocumentIRI(ontology);
		ontologyIRI = ontology.getOntologyID().getOntologyIRI().get();
		factory = manager.getOWLDataFactory();
		//System.out.println(factory);
		prefixManager = new DefaultPrefixManager(null,null,ontologyIRI.toString());
		//System.out.println(prefixManager);
		//fireEventClass = getFireEventClass();
	}
	
	/**
	 * This method gets a given class , if it does not exist it is "created"
	 * @param className
	 * @return
	 */
	public OWLClass createClass(String className){/*
		System.out.println(factory);
		System.out.println("Createclass is called");
		OWLClass owlClass = factory.getOWLClass("#"+className, prefixManager);
		return owlClass;*/
		return null;
	}
	
	public OWLClass getClass(String className){
		//System.out.println(factory);
		OWLClass owlClass = factory.getOWLClass("#"+className, prefixManager);
		return owlClass;
		//return createClass(className);
	}
	
	public ChangeApplied saveEntity(OWLEntity owlEntity){
		OWLDeclarationAxiom declarationAxiom = factory.getOWLDeclarationAxiom(owlEntity);
		return manager.addAxiom(ontology, declarationAxiom);
	}
	
	public void saveOntology(){
		try {
			manager.saveOntology(ontology);
		} catch (OWLOntologyStorageException e) {
			e.printStackTrace();
		}
	}
	
	public Set<OWLEntity> getAllEntities(){		
		return ontology.getEntitiesInSignature(ontologyIRI);
	}
	
	public Set<OWLNamedIndividual> getAllIndividuals(){
		return ontology.getIndividualsInSignature();
	}
	
	public Set<OWLClass> getAllClasses(){
		return ontology.getClassesInSignature();
	}
	
	public Set<OWLObjectProperty> getAllObjectProperties(){
		return ontology.getObjectPropertiesInSignature();
	}

	public OWLNamedIndividual getNamedIndividual(String individualName){
		return factory.getOWLNamedIndividual("#"+individualName,prefixManager);
	}
	
	void saveNamedIndividal(OWLNamedIndividual individual){
		saveEntity(individual);
	}
	
	public void addNamedIndividual(String individualName){
		saveEntity(getNamedIndividual(individualName));
	}
	
	
	/*
	public void addFireEvent(String fireEventName){
		OWLNamedIndividual fireEvent = getNamedIndividual(fireEventName);
		
		// Save individual to ontology
		saveNamedIndividal(fireEvent);

		// Save class assertion to ontology
		OWLClassAssertionAxiom assertion = createClassAssertion(fireEventClass, fireEvent);
		addClassAssertionToOntology(assertion);
		
		// Save ontology
		saveOntology();
	}
	
	public OWLClass getFireEventClass(){
		return getClass("Fire");
	}*/
	
	/**
	 * Use this method to specify that a given individual is a instance of the given class
	 * @param owlClass
	 * @param individual
	 * @return
	 */
	private OWLClassAssertionAxiom createClassAssertion(OWLClass owlClass, OWLNamedIndividual individual){
		return factory.getOWLClassAssertionAxiom(owlClass, individual);
	}
	
	private ChangeApplied addClassAssertionToOntology(OWLClassAssertionAxiom assertion){
		return manager.addAxiom(ontology, assertion);
	}
	
	public OWLObjectProperty getObjectProperty(String propertyName){
		return factory.getOWLObjectProperty("#"+propertyName, prefixManager);
	}
	
	public ChangeApplied createAndAddClassAssertion(OWLClass owlClass, OWLNamedIndividual individual){
		OWLClassAssertionAxiom assertion = createClassAssertion(owlClass, individual);
		ChangeApplied change = addClassAssertionToOntology(assertion);
		return change;
	}
	
	public ChangeApplied createAndAddPropertyAssertion(OWLNamedIndividual subject, OWLNamedIndividual object , OWLObjectProperty property){
		OWLObjectPropertyAssertionAxiom axiom = factory.getOWLObjectPropertyAssertionAxiom(property, subject, object);
		return manager.addAxiom(ontology , axiom);
	}
	
	public void removeClasses(Set<OWLClass> owlClasses){
		Set<OWLOntology> ontologies = new HashSet<>();
		ontologies.add(ontology);
		OWLEntityRemover remover = new OWLEntityRemover(ontologies);
		for(OWLClass owlClass : owlClasses){
			remover.visit(owlClass);			
		}
		List<RemoveAxiom> changes = remover.getChanges();
		manager.applyChanges(changes);
	}
	public void removeIndividuals(Set<OWLNamedIndividual> individuals){
		Set<OWLOntology> ontologies = new HashSet<>();
		ontologies.add(ontology);
		OWLEntityRemover remover = new OWLEntityRemover(ontologies);
		for(OWLNamedIndividual individual: individuals){
			remover.visit(individual);			
		}
		List<RemoveAxiom> changes = remover.getChanges();
		manager.applyChanges(changes);
	}
	
	public Set<OWLIndividualAxiom> getAxioms(OWLNamedIndividual in){
		Set<OWLIndividualAxiom> axioms = ontology.getAxioms(in,null);
		return axioms;
	}
	
	public Set<OWLClassAxiom> getAxioms(OWLClass cls){
		Set<OWLClassAxiom> classAxioms = ontology.getAxioms(cls,null);
		return classAxioms;
	}
	
	public OWLDataProperty getDataProperty(String propName){
		return factory.getOWLDataProperty(propName, prefixManager);
	}
	public void addDataPropAssertion(String dataPropName, OWLNamedIndividual indi, String literalString){
		OWLLiteral literal = factory.getOWLLiteral(literalString);
		OWLDataProperty dataProp = factory.getOWLDataProperty("#"+dataPropName,prefixManager);
		OWLDataPropertyAssertionAxiom assertion = factory.getOWLDataPropertyAssertionAxiom(dataProp, indi, literal);
		manager.addAxiom(ontology, assertion);
	}
	
}
