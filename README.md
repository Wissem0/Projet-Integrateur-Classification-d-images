# A game in Python that matches a celebrity's face with yours. 
Relies on unsupervised machine learning trained using https://www.kaggle.com/datasets/jessicali9530/celeba-dataset (40 features)


```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```

## Game V1 (Classification tree) : 
Before release : 
### Training & Testing 
- Building classification tree with linear classification from list_atr_celebra
- Training and testing CNN

### Playing the game : 
- Uploading photo
- Determining existing features with CNN -> feature vector [1,-1,....,]
- Searching the classification tree 
- Score = 100%
- Searching classification tree to find a matching celebrity
- IF stuck in search tree change feature in feature vector -> lowers ressemblance score
- Get a filename and display it with ressemblance score (Ex: 68%)


## Game V2 (KNN) : 
Before release : 
### Training & Testing 
- Training and testing CNN

### Playing the game : 
- Uploading photo
- Determining existing features with CNN -> feature vector [1,-1,....,]
- Running KNN on list_atr_celebra with vector
- Score = ratio between distance to nearest and longest distance
- Get a filename and display it with ressemblance score (Ex: 68%)
