package fr.insa.projetint.Orchestrateur.service;

import java.util.ArrayList;

import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import fr.insa.projetint.Orchestrateur.model.SearchRes;

@Service
public class SearchService {
	
	WebClient webClient = WebClient.create("http://search:5000");
	
	public ArrayList<ArrayList<String>> searchImg(String attributes) {
		SearchRes test1 = webClient.get().uri("/search/" + attributes).retrieve().bodyToMono(SearchRes.class).block();
		return test1.getRes();
	}

}
