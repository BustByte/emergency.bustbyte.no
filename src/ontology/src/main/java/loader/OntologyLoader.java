package main.java.loader;

import java.io.File;

import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;
import org.semanticweb.owlapi.model.OWLOntologyManager;

public class OntologyLoader {
	
	static OWLOntologyManager manager;
	
	public static void setManager(OWLOntologyManager m){
		manager = m;
	}
	
	public static OWLOntology loadOntology(String filename){
		
		File ontologyFile = new File(filename);
		OWLOntology ontology = loadOntology(ontologyFile);
		return ontology;
	}
	
	public static OWLOntology loadOntology(File ontologyFile){
		try {
			//System.out.println(manager);
			//System.out.println(ontologyFile);
			return manager.loadOntologyFromOntologyDocument(ontologyFile);
		} catch (OWLOntologyCreationException e) {
			e.printStackTrace();
			return null;
		}
	}
	
	
	
	
	
	
}
