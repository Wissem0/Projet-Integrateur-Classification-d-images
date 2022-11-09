# A game in Python that matches a celebrity's face with yours. 
Relies on unsupervised machine learning trained using https://www.kaggle.com/datasets/jessicali9530/celeba-dataset (40 features)

Before release : 
- Training & Testing ( Building classification tree with linear classification from list_atr_celebra) 
- Tra
Game : 
- Uploading photo
- Determining existing features with CNN -> feature vector [1,-1,....,]
- Searching the classification tree 
- Score = 100%
- Searching classification tree to find a matching celebrity
- IF stuck in search tree change feature in feature vector -> lowers ressemblance score
- Get a filename and display it with ressemblance score (Ex: 68%)
