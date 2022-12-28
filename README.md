# A web game that matches the user with the celebrity they most resemble. 
Relies on unsupervised machine learning trained using https://www.kaggle.com/datasets/jessicali9530/celeba-dataset (40 features)

![Project Architechture Diagram](architechture.drawio.svg)

## Sequence of actions : 
Before release : 
### Training & Testing 
- Train and test CNN (Microservice 1)
- Eventually build search data structure (Microservice 2)

### Playing the game : 
- Upload photo
- Determine existing features with CNN -> user attribute vector [1,-1,....,]
- Run the search algorithm from list_atr_celebra using user attribute vector. Score = percentage of common features between user and celebrity
- Display celebrity image with the ressemblance score (e.g. 68%) and mismatched attributes (e.g. Glasses, Pale Skin)
