package fr.insa.projetint.Orchestrateur.model;

public class Image {
	private String encoded;
	public Image(String encoded) {
		super();
		this.encoded = encoded;
	}
	
	public Image() {
		}


	public String getEncoded() {
		return encoded;
	}

	public void setEncoded(String encoded) {
		this.encoded = encoded;
	}
}
