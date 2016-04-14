package main.java.application;

import java.util.Collections;
import java.util.Set;

import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLClassExpression;
import org.semanticweb.owlapi.model.OWLNamedIndividual;
import org.semanticweb.owlapi.model.OWLObjectProperty;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.reasoner.Node;
import org.semanticweb.owlapi.reasoner.NodeSet;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.structural.StructuralReasonerFactory;

public class StandardQuerier {

	private OWLReasoner reasoner;
	
	public void init(OWLOntology ontology){
		StructuralReasonerFactory factory = new StructuralReasonerFactory();
		reasoner = factory.createReasoner(ontology);
	}
	
	public Set<OWLClass> getSuperClasses(OWLClassExpression classExpression, boolean direct) {
		if (classExpression == null) {
			return Collections.emptySet();
		}
		NodeSet<OWLClass> superClasses = reasoner
				.getSuperClasses(classExpression, direct);
		return superClasses.getFlattened();
	}

	public Set<OWLClass> getEquivalentClasses(OWLClassExpression classExpression) {
		if (classExpression == null) {
			return Collections.emptySet();
		}
		Node<OWLClass> equivalentClasses = reasoner.getEquivalentClasses(classExpression);
		Set<OWLClass> result = null;
		if (classExpression.isAnonymous()) {
			result = equivalentClasses.getEntities();
		} else {
			result = equivalentClasses.getEntitiesMinus(classExpression.asOWLClass());
		}
		return result;
	}

	public Set<OWLClass> getSubClasses(OWLClassExpression classExpression, boolean direct) {
		if (classExpression == null) {
			return Collections.emptySet();
		}
		NodeSet<OWLClass> subClasses = reasoner.getSubClasses(classExpression, direct);
		return subClasses.getFlattened();
	}

	public Set<OWLNamedIndividual> getInstances(OWLClassExpression classExpression,
			boolean direct) {
		if (classExpression == null) {
			return Collections.emptySet();
		}
		NodeSet<OWLNamedIndividual> individuals = reasoner.getInstances(classExpression,
				direct);
		return individuals.getFlattened();
	}

	public NodeSet<OWLNamedIndividual> getObjectPropertyDomainsValues(OWLNamedIndividual evidenceInd, OWLObjectProperty prop){
		return reasoner.getObjectPropertyValues(evidenceInd, prop);
	}
	

}
