package fr.insa.projetint.Orchestrateur.controller;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;

import org.apache.commons.io.FileUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import fr.insa.projetint.Orchestrateur.model.Image;
import fr.insa.projetint.Orchestrateur.ressource.ImageRessource;
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
	public List<String> match(@RequestBody String img64) {
		String attributes = this.cnnService.findAttribute(img64);
		return this.searchService.searchAllImg(attributes);
	}
	
	@GetMapping("/match0")
	public String match0() throws IOException {
		String path = "./src/main/resources/images/000001.jpg";
		String imgEnc = new ImageRessource(path).getEncStr();
		String attributes = this.cnnService.findAttribute(imgEnc);
		return this.searchService.searchImg(attributes);
	}

	@GetMapping("/match1")
	public ArrayList<ArrayList<String>> match1() throws IOException {
		String path = "./src/main/resources/images/rostom.jpg";
		String img64 = new ImageRessource(path).getEncStr();
		String attributes = this.cnnService.findAttribute(img64);
		return this.searchService.helloWorld(attributes);
	}
}
