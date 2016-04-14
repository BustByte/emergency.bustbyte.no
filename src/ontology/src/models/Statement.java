package models;

import java.util.List;

public class Statement {

	String statementName;
	String victim;
	String evidence;
	String evidenceType;
	String area;
	String holder;
	List<String> eventType;
	String areaType;
	List<String> eventName;
	String day;
	
	public List<String> getEventNames(){
		return eventName;
	}
	public void setEventNames(List<String> eventName){
		this.eventName = eventName;
	}
	public List<String> getEventTypes() {
		return eventType;
	}
	public void setEventTypes(List<String> eventType) {
		this.eventType = eventType;
	}
	public String getAreaType() {
		return areaType;
	}
	public void setAreaType(String areaType) {
		this.areaType = areaType;
	}
	public String getStatementName() {
		return statementName;
	}
	public void setStatementName(String statementName) {
		this.statementName = statementName;
	}
	public String getVictim() {
		return victim;
	}
	public void setVictim(String victim) {
		this.victim = victim;
	}
	public String getEvidence() {
		return evidence;
	}
	public void setEvidence(String evidence) {
		this.evidence = evidence;
	}
	public String getEvidenceType() {
		return evidenceType;
	}
	public void setEvidenceType(String evidenceType) {
		this.evidenceType = evidenceType;
	}
	public String getArea() {
		return area;
	}
	public void setArea(String area) {
		this.area = area;
	}
	public String getHolder() {
		return holder;
	}
	public void setHolder(String holder) {
		this.holder = holder;
	}
	public String getDay(){
		return day;
	}
	public void setDay(String day){
		this.day = day;
	}
}
