package fr.insa.projetint.Orchestrateur.service;

import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Service
public class CNNService {
	
	WebClient webClient = WebClient.create("http://cnn:8083");

	
	public String findAttribute(String img64) {
		String res = webClient.post()
				.uri("/receive")
				.header(HttpHeaders.CONTENT_TYPE,  MediaType.TEXT_PLAIN_VALUE)
				.body(Mono.just(img64), String.class)
				.retrieve()
				.bodyToMono(String.class).block();
		return res;
	}

}
