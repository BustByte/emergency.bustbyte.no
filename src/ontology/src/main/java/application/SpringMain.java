package main.java.application;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.context.web.SpringBootServletInitializer;

@SpringBootApplication
public class SpringMain extends SpringBootServletInitializer{

	protected SpringApplicationBuilder 	configure(SpringApplicationBuilder builder){
		return builder.sources(SpringMain.class);
	}
	
	public static void main(String[] args) {
		SpringApplication.run(SpringMain.class, args);
	}

}