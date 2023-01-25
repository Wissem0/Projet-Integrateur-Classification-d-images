package fr.insa.projetint.Orchestrateur.ressource;

import java.io.File;
import java.io.IOException;
import java.util.Base64;

import org.apache.commons.io.FileUtils;

public class ImageRessource {
	
	private String path;
	
	public ImageRessource() {
		
	}
	
	public ImageRessource(String path) 	{
		this.path = path;
	}
	
	public String getEncStr() throws IOException {
		byte[] fileContent = FileUtils.readFileToByteArray(new File(this.path));
		String encodedString = Base64.getEncoder().encodeToString(fileContent);
		return encodedString;
	}
}
