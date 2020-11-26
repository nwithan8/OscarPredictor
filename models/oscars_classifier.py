from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import pickle

def main():
    movies_file = pd.read_csv("movies_input.csv", encoding = "ISO-8859-1")
    actors_file = pd.read_csv('actors.csv', encoding = "ISO-8859-1")
    directors_file = pd.read_csv('directors.csv', encoding = "ISO-8859-1")
    mpaaRatings_file = pd.read_csv('mpaaRatings.csv', encoding = "ISO-8859-1")

    actors = actors_file['Actors'].values.tolist()
    directors = directors_file['Directors'].values.tolist()
    mpaaRatings = mpaaRatings_file['MPAARating'].values.tolist()

    n = len(movies_file.index)
    X = []

    for i in range(0,n):
        item = list(movies_file.iloc[i])
	director = item[9]
    	actor1 = item[13]
    	actor2 = item[17]
    	actor3 = item[21]
    	mpaaRating = item[5]

        if not(director in directors):
            directors.append(director)
        item[9] = directors.index(director)
        item[10] = int(item[10])
    
        if not(actor1 in actors):
            actors.append(actor1)
        item[13] = actors.index(actor1)
        item[14] = int(item[14])
    
    	if not(actor2 in actors):
            actors.append(actor2)
        item[17] = actors.index(actor2)
    	item[18] = int(item[18])
    
    	if not(actor3 in actors):
            actors.append(actor3)
    	item[21] = actors.index(actor3)
    	item[22] = int(item[22])
    
    	if not(mpaaRating in mpaaRatings):
            mpaaRatings.append(mpaaRating)
    	item[5] = mpaaRatings.index(mpaaRating)

        movie = item[0:4] + item[9:] + [item[5]] + [item[4]] + item[6:9]
        X.append(movie)
    
    classifier_file = open("oscars_classifier.pkl", 'rb')
    classifier = pickle.load(classifier_file)
    file.close()

    predictions = classifier.predict(X)
    predictions_file = open("predictions.csv",'w')
    for prediction in predictions:
    	predictions_file.write(r + ",")
    predictions_file.close()

if __name__ == "__main__":
    main()