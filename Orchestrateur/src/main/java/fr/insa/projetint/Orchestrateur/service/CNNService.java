package fr.insa.projetint.Orchestrateur.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.reactive.function.client.WebClient;
import fr.insa.projetint.Orchestrateur.model.Image;
import reactor.core.publisher.Mono;

@Service
public class CNNService {
	
	@Autowired
	private RestTemplate restTemplate;
	WebClient webClient = WebClient.create("http://localhost:8083");

	
	public String findAttribute(String img64) {
		String res = webClient.post()
				.uri("/receive")
				.header(HttpHeaders.CONTENT_TYPE,  MediaType.TEXT_PLAIN_VALUE)
				.body(Mono.just(img64), String.class)
				.retrieve()
				.bodyToMono(String.class).block();
		System.out.println(res);
		return res;
	}
	
	public String helloWorld() {
		Image test = webClient.get().uri("/a").retrieve().bodyToMono(Image.class).block();
		Image res = webClient.get().uri("/" + test.getEncoded()).retrieve().bodyToMono(Image.class).block();
		return res.getEncoded();
	}

}
