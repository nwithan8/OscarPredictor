from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import pickle

def main(movies):
    file = open("oscars_classifier.pkl", 'rb')
    classifier = pickle.load(file)
    file.close()
    predictions = classifier.predict(movies)
    return predictions

if __name__ == "__main__":
    main(movies)