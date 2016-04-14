package sparql;

import org.apache.jena.atlas.lib.NotImplemented;
import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLNamedIndividual;

public class SparqlQueryConstructor {

	String query;
	int OBJECT_PROP = 1;
	int INDIVIDUAL = 2;
	int CLASS = 3;
	int TYPE = 4;
			
	public String getOWLClassSuffix(OWLClass owlClass){
		return owlClass.getIRI().getShortForm();
	}
	
	public String getOWLNamedIndividualSuffix(OWLNamedIndividual indi){
		return indi.getIRI().getShortForm();
	}
	
	public String getStatementsWithEventsOfType(OWLClass owlClass){
		return getStatementsWithEventsOfType(getOWLClassSuffix(owlClass));
	}
	
	public String getStatementsWithEventsOfType(String classSuffix){
		query = "";
		addPrefix(OBJECT_PROP);
		addPrefix(CLASS);
		addPrefix(TYPE);
		
		query += "SELECT ?statement WHERE { ?statement "
				+ "myOnt:EmergencyOntologyhasEvent ?type ."
				+ " ?type rdf:type myOntIndividual:"+classSuffix;
		query += " }";
		
		return query;
	}
	
	public String getStatementsWithLocation(OWLNamedIndividual individ){
		return getStatementsWithLocation(getOWLNamedIndividualSuffix(individ));
	}
	
	public String getStatementsWithLocation(String locationTypeSuffix){
		query = "";
		addPrefix(OBJECT_PROP);
		addPrefix(CLASS);
		addPrefix(TYPE);
		
		query += "SELECT ?statement WHERE { ?statement "
				+ "myOnt:EmergencyOntologyhasLocation ?locType ."
				+ " ?locType rdf:type myOntIndividual:"+locationTypeSuffix;
		query += " }";
		
		return query;
	}
	
	public String getStatementsWithEvidencesOfType(String type){
		query = "";
		addPrefix(OBJECT_PROP);
		addPrefix(CLASS);
		addPrefix(TYPE);
		
		query += "SELECT ?statement WHERE { "
			   + " ?statement myOntIndividual:hasEvidence myOnt:"+type+"Individual ";
		query += " }";
		
		return query;
	}
	
	public void and(){
		query += " . ";
	}
	
	public void addPrefix(int prefix){
		if(prefix == OBJECT_PROP){
			query += SparqlQueryStrings.PREFIX_OBJECT_PROPS + "\n";
		}
		else if(prefix == CLASS){
			query += SparqlQueryStrings.PREFIX_INDIVIDUALS + "\n";
		}
		else if(prefix == INDIVIDUAL){
			query += SparqlQueryStrings.PREFIX_INDIVIDUALS + "\n";
		}
		else if(prefix == TYPE){
			query += SparqlQueryStrings.PREFIX_RDF_TYPE + "\n";
		}
		
	}
	
	public void where(){
		
	}
	
	public String getSubjectWithHasDay(String day){
		query = "";
		addPrefix(OBJECT_PROP);
		addPrefix(CLASS);
		addPrefix(TYPE);
		
		query += "SELECT ?subject ?val WHERE { ?subject"
				+ " myOntIndividual:EmergencyOntologyhasDay ?val ";
		query += " }";
		
		return query;
	}
}
