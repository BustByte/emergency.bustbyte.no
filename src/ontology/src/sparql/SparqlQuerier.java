package sparql;

import org.mindswap.pellet.jena.PelletReasonerFactory;

import com.clarkparsia.pellet.sparqldl.jena.SparqlDLExecutionFactory;
import com.hp.hpl.jena.ontology.OntModel;
import com.hp.hpl.jena.query.Query;
import com.hp.hpl.jena.query.QueryExecution;
import com.hp.hpl.jena.query.QueryFactory;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.query.ResultSetFormatter;
import com.hp.hpl.jena.rdf.model.ModelFactory;

public class SparqlQuerier {
	
	OntModel model;
	
	public SparqlQuerier(String pathToOntology){
		init(pathToOntology);
	}
	
	public SparqlQuerier(OntModel model){
		this.model = model;
	}
	
	public void init(String pathToOntology){
		this.model = ModelFactory.createOntologyModel( PelletReasonerFactory.THE_SPEC);
		this.model.read(pathToOntology);
		
	}
	
	public OntModel getModel(){
		return model;
	}
	
	public QueryExecution setupQuery(String queryString){
		Query query = QueryFactory.create(queryString);
		if( query == null || model == null ) throw new IllegalStateException() ;
		QueryExecution qe = SparqlDLExecutionFactory.create( query, model);
		return qe;
	}
	
	public ResultSet querySelect(String queryString){
		QueryExecution qe = setupQuery(queryString);
		ResultSet rs = qe.execSelect();
		return rs;
	}
	
	
	
	
}
