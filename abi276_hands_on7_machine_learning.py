# -*- coding: utf-8 -*-
"""abi276_Hands_on7_Machine_Learning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FW6bfLJ6-V1Dje-kJn-AQ1cK72pAV3CL

# Hands_on9: Machine_Learning - Classification

*Note: This session is graded (binary grading "Complete/Incomplete"). Complete all the exercises and submit the ipynb to canvas under assignment Hands-on7: Machine Learning

Hands-on9 submission by **Tomorrow (Friday) (10/20), 11:59 PM**

## 0. The Diabetes Dataset
Take a look at the dataset here: https://www.kaggle.com/datasets/mathchi/diabetes-data-set

Description from the website:

"This dataset is originally from the National Institute of Diabetes and Digestive and Kidney Diseases. The objective is to predict based on diagnostic measurements whether a patient has diabetes."

Read the description ("Content" section) from the website. As per the website, the columns of the datasets are:

- Pregnancies: Number of times pregnant
- Glucose: Plasma glucose concentration a 2 hours in an oral glucose tolerance test
- BloodPressure: Diastolic blood pressure (mm Hg)
- SkinThickness: Triceps skin fold thickness (mm)
- Insulin: 2-Hour serum insulin (mu U/ml)
- BMI: Body mass index (weight in kg/(height in m)^2)
- DiabetesPedigreeFunction: Diabetes pedigree function
- Age: Age (years)
- Outcome: Class variable (0 or 1)

### Today's Task:
**To build classification models than can predict whether the person will have diabetes or not (i.e., Outcome) based on the inputs.**

I have split the data into two:

1. **train.csv** This is to train our machine learning classifiers.
2. **test.csv** This will be used to evaluate our classifiers' performance.

Download these two files from **Canvas->Files->Week9->train.csv** and **Canvas->Files->Week9->test.csv**

**VVIMP: PUT THESE TWO FILES IN THE SAME DIRECTORY AS THIS NOTEBOOK TO AVOID FILENOTFOUND ERROR**

## 1. Load and Preprocess Data
Let's load the data into a Pandas DataFrame. Check and remove duplicates. Check and clean rows with NULL entries.
"""

import pandas as pd

train_df = pd.read_csv("train.csv")
train_df.head()

"""### 1.1. Feature and Label
We will select coumns that will act as input ($x_1,x_1,..,x_N$) and output ($y_{actual}$).
"""

train_features = train_df[["Pregnancies","Glucose","BloodPressure",
                          "SkinThickness","Insulin","BMI",
                           "DiabetesPedigreeFunction","Age"]]

train_labels = train_df["Outcome"]

train_features.head()
train_labels.head()

"""## 2. Defining and training Classifiers

Let's define Logistic regression and Neural Network with default configurations.

A neural network is also called as a MultiLayered Perceptron (MLP)
"""

# Now let's define our models
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier


lr_classifier = LogisticRegression(solver='lbfgs',max_iter=10000)
mlp_classifier = MLPClassifier(solver='lbfgs', alpha=1e-5,
                               hidden_layer_sizes=(8, 2), random_state=11,max_iter=10000)


# train our models
lr_classifier.fit(train_features.to_numpy(),train_labels.to_numpy())
mlp_classifier.fit(train_features.to_numpy(),train_labels.to_numpy())

"""### 3. Evaluating our models' performance
We define accuracy metric as follows:

$$acc = \frac{Number~of~times~predicted~class~=~actual~class}{Total~number~of~examples}$$
"""

from sklearn.metrics import accuracy_score

#load test data
test_df = pd.read_csv("test.csv")

# Extract the input features
test_inputs = test_df[["Pregnancies","Glucose","BloodPressure",
                          "SkinThickness","Insulin","BMI",
                           "DiabetesPedigreeFunction","Age"]]

y_actual = test_df["Outcome"]

# predict using logistic regression model
y_predicted_lr = lr_classifier.predict(test_inputs.to_numpy())
lr_accuracy_score = accuracy_score(y_predicted_lr,y_actual)

# predict using logistic regression model
y_predicted_mlp = mlp_classifier.predict(test_inputs.to_numpy())
mlp_accuracy_score = accuracy_score(y_predicted_mlp,y_actual)

print (f"Accuracy of the Logistic Classifier = {lr_accuracy_score}")
print (f"Accuracy of the MLP Classifier = {mlp_accuracy_score}")

"""### 3.1. Insights:
For our dataset and configurations, we see that Logistic Regression models is 74.6% accurate on our test data. It is a better model than the Neural Network model

## 4. Saving our best model for future use

We can store our best model on our hard drive and load it as and when we need it.
"""

# Storing
import pickle

file_to_write = open("diabetes_best_model.saved","wb")
pickle.dump(lr_classifier,file_to_write)
file_to_write.close()

"""## 5. Loading our best model and testing it"""

import pickle
import numpy

model_file = open("diabetes_best_model.saved","rb")
model = pickle.load(model_file)
model_file.close()

# Let's prepare a sample input
pregnancies = 1
glucose = 200
bp = 66
skin_thickness = 20
insulin = 95
bmi = 32.9
diabetes_pedigree = 0.6
age = 28

input_data =numpy.array([[pregnancies,glucose,bp,
                        skin_thickness,insulin,bmi,
                        diabetes_pedigree,age]])

y_predicted_lr = lr_classifier.predict(input_data)

if y_predicted_lr[0]==1:
    print ("The person is likely to have diabetes in the near future")
if y_predicted_lr[0]==0:
    print ("The person will not have diabetes")

"""## E1. Exercise: Let's work on a different set of features "Age" and repeat

**Create a new Jupyter Notbook and do the following**

Following the above hands-on, initialize and train Logistic Regression and MLP classifiers for predicting diabetes using the following columns:

**Feature Columns (Input):**
- Glucose: Plasma glucose concentration a 2 hours in an oral glucose tolerance test
- BloodPressure: Diastolic blood pressure (mm Hg)
- Insulin: 2-Hour serum insulin (mu U/ml)
- BMI: Body mass index (weight in kg/(height in m)^2)
- Age: Age (years)

**Label (Output):**
- Outcome: Class variable (0 or 1)

What accuracy figures are you getting for the two classifiers? Are they very different from the accuracy figures we for in Section 3 above? Write down in a markdown block.
"""

#load dataframe of training data
import pandas as pd
train_df = pd.read_csv("train.csv")
train_df.head()
#create labels for dataframe
train_features = train_df[["Glucose","BloodPressure","Insulin","BMI","Age"]]
train_labels = train_df["Outcome"]

#create ML model
#Define our models
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
lr_classifier = LogisticRegression(solver='lbfgs',max_iter=10000)
mlp_classifier = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(8, 2), random_state=11,max_iter=10000)
#train models (a logisitc & a neural model)
lr_classifier.fit(train_features.to_numpy(),train_labels.to_numpy())
mlp_classifier.fit(train_features.to_numpy(),train_labels.to_numpy())

#load test data
test_df = pd.read_csv("test.csv")
#label test data
test_inputs = test_df[["Glucose","BloodPressure","Insulin","BMI","Age"]]
y_actual = test_df["Outcome"]

#test model
from sklearn.metrics import accuracy_score
# predict using logistic regression model
y_predicted_lr = lr_classifier.predict(test_inputs.to_numpy())
lr_accuracy_score = accuracy_score(y_predicted_lr,y_actual)
#predict using logistic regression model
y_predicted_mlp = mlp_classifier.predict(test_inputs.to_numpy())
mlp_accuracy_score = accuracy_score(y_predicted_mlp,y_actual)
#return accuracy score to user
print (f"Accuracy of the Logistic Classifier = {lr_accuracy_score}")
print (f"Accuracy of the MLP Classifier = {mlp_accuracy_score}")

"""We see that our logistic model has a higher accuracy than nueral network model (74% > 63%) - when using are test data. As our logistic model is better, should be the one saced for future use.

Accuracy of the two models with the features: Glucose, Blood Pressure, Insulin, BMI, and Age - is nearly identical to the accuracy of the two models using the features: Pregnancies Glucose Blood Pressure, SkinThickness, Insulin, BMI, Diabetes Pedigree Function, Age (Logisitic: 74% vs 75%; Neural: 63% vs 62%).
"""