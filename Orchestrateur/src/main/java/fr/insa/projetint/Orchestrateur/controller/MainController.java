package fr.insa.projetint.Orchestrateur.controller;

import java.util.ArrayList;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import fr.insa.projetint.Orchestrateur.service.CNNService;
import fr.insa.projetint.Orchestrateur.service.SearchService;

@RestController
@RequestMapping("/transfert_cnn")
public class MainController {
	
	@Autowired
	private CNNService cnnService;
	
	@Autowired
	private SearchService searchService;

	@PostMapping()
	public ArrayList<ArrayList<String>> match(@RequestBody String img64) {
		String attributes = this.cnnService.findAttribute(img64);
		ArrayList<ArrayList<String>> res = this.searchService.searchImg(attributes);
		System.out.println(res);
		return res;
	}
}
