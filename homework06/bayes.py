from collections import defaultdict


class NaiveBayesClassifier:

    def __init__(self, alpha):
        pass

    def fit(self, x, y):
        """ Fit Naive Bayes classifier according to X, y. """
        classes = defaultdict(lambda:0)
        freq = defaultdict(lambda:0)
        for label in y:
            classes[label] += 1
            for trait in str(x).split():
                freq[label, trait] += 1
        for label, trait in freq:
            freq[label, trait] /= classes[label]
        for c in classes:
            classes[c] /= len(y)
        pass

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        classes, prob = self.predictor
        return min(classes.keys(),  # calculate argmin(-log(C|O))
                   key=lambda cl: -log(classes[cl]) + \
                                  sum(-log(prob.get((cl, feat), 10 ** (-7))) for feat in feats))
        pass

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        pass

