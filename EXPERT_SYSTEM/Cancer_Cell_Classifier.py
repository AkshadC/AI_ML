import numpy as np
import pandas as pd
import seaborn
from sklearn.model_selection import train_test_split
from sklearn import svm

seaborn.set()


class cancer_cell:

    def __init__(self, cancer_data):
        self.data = cancer_data

    def preprocess(self):
        self.data = self.data[pd.to_numeric(self.data['BareNuc'], errors='coerce').notnull()]
        self.data['BareNuc'] = self.data['BareNuc'].astype('int')
        inputs_df = self.data[
            ['Clump', 'UnifSize', 'UnifShape', 'MargAdh', 'SingEpiSize', 'BareNuc', 'BlandChrom', 'NormNucl', 'Mit']]
        inputs = np.asarray(inputs_df)

        targets = np.asarray(self.data['Class'])
        return inputs, targets

    def svm_classifier(self, x_train, y_train):
        clf = svm.SVC(kernel='linear')
        clf.fit(x_train, y_train)
        return clf

    def predict(self, clf_obj, test):
        test = test.reshape(1, -1)
        return clf_obj.predict(test)


def main():
    cancer_obj = cancer_cell(pd.read_csv('cell_samples.csv'))
    inputs, targets = cancer_obj.preprocess()

    x_train, x_test, y_train, y_test = train_test_split(inputs, targets, test_size=0.2, random_state=4)

    clf = cancer_obj.svm_classifier(x_train, y_train)
    print("ENTER THE REQUIRED CELL VALUES FOR FURTHER DETECTION: ")

    Clump = int(input("Enter the value for Clump thickness: "))
    UnifSize = int(input("Enter the value for Uniformity of cell size: "))
    UnifShape = int(input("Enter the value for Uniformity of cell shape: "))
    MargAdh = int(input("Enter the value for Marginal adhesion: "))
    SingEpiSize = int(input("Enter the value for Single epithelial cell size: "))
    BareNuc = int(input("Enter the value for Bare nuclei: "))
    BlandChrom = int(input("Enter the value for Bland chromatin: "))
    NormNucl = int(input("Enter the value for Normal nucleoli: "))
    Mit = int(input("Enter the value for Mitoses:  "))
    temp = [Clump, UnifSize, UnifShape, MargAdh, SingEpiSize, BareNuc, BlandChrom, NormNucl, Mit]
    test1 = np.asarray(temp)

    prediction = cancer_obj.predict(clf, test1)

    if prediction == 2:
        print("THE CELL IS Malignant!")
    else:
        print("THE CELL IS Benign")


if __name__ == "__main__":
    main()
