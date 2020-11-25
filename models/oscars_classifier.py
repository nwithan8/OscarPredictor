from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import pickle

def main(movies):
    file = open("oscars_classifier.pkl", 'rb')
    classifier = pickle.load(file)
    file.close()
    
    X = []
    for item in movies:
        movie = item[0:4] + item[9:] + [item[5]] + [item[4]] + item[6:9]
        X.append(movie)
        
    predictions = classifier.predict(X)
    return predictions

if __name__ == "__main__":
    main(movies)