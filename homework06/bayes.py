from collections import defaultdict
from math import log
import csv
import string

class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha
        pass

    def train(self, data, labels):
        """Train Naive Bayes classifier on labeled strings."""
        classes = defaultdict(lambda: 0)
        freq = defaultdict(lambda: 0)
        for label, text in zip(labels, data):
            classes[label] += 1
            for trait in str(text).split():
                freq[label, trait] += 1
        for label, trait in freq:
            freq[label, trait] /= classes[label]
        for c in classes:
            classes[c] /= len(labels)
        self.predictor = classes, freq

    def predict(self, data):
        """ Perform classification on an array of test vectors X. """
        classes, freq = self.predictor
        print(data)
        return min(classes.keys(),  # calculate argmin(-log(C|O))
                   key=lambda cl: -log(classes[cl]) + \
                                  sum(-log(freq.get((cl, feat), 10 ** (-7))) for feat in str(X)))
        # for string in data:
        #    for label_num in classes.values():
        #        print(label_num)
        #        val = log(label_num) + sum(log(freq.get((cl, feat), 10 ** (-7))) for feat in string.split())
        #        if val > max_val:
        #            max_val = val


    def score(self, x_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        score = 0
        for current_X, current_Y in zip(x_test, y_test):
            if self.predict(current_X) == current_Y:
                score += 1
        score /= len(x_test)
        return score

def clean(sentence):
    translator = str.maketrans("", "", string.punctuation)
    return sentence.translate(translator)

if __name__ == '__main__':
    # features = get_features()
    # X = [i[0] for i in features]
    # Y = [i[1] for i in features]

    X, Y = [], []
    with open("SMSSpamCollection") as f:
        data = list(csv.reader(f, delimiter="\t"))
    for target, msg in data:
        X.append(msg)
        Y.append(target)

    X = [clean(x).lower() for x in X]

    X_train, Y_train, X_test, Y_test = X[:500], Y[:500], X[500:], Y[500:]

    model = NaiveBayesClassifier()
    model.train(X_train, Y_train)

    print(model.score(X_test, Y_test))

