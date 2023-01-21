package fr.insa.projetint.Orchestrateur.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.reactive.function.client.WebClient;

import fr.insa.projetint.Orchestrateur.model.SearchRes;

@Service
public class SearchService {
	
	@Autowired
	private RestTemplate restTemplate;
	WebClient webClient = WebClient.create("http://127.0.0.1:5000");
	
	public String searchImg(String attributes) {
		SearchRes test1 = webClient.get().uri("/search/" + attributes).retrieve().bodyToMono(SearchRes.class).block();
		return test1.getFirstImageName();
	}
	
	public List<String> searchAllImg(String attributes) {
		SearchRes test1 = webClient.get().uri("/search/" + attributes).retrieve().bodyToMono(SearchRes.class).block();
		return test1.getAllImageName();
	}
	
	public ArrayList<ArrayList<String>> helloWorld(String attributes) {
		SearchRes test1 = webClient.get().uri("/search/" + attributes).retrieve().bodyToMono(SearchRes.class).block();
		return test1.getRes();
	}

}
