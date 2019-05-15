#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# In[2]:


dataset = pd.read_csv('/home/deepanshu/Downloads/finaldataCopy.csv')


# dataset.columns

# In[ ]:


dataset.info()


# In[5]:


# dataset.drop('Unnamed: 21', axis='columns', inplace=True)
dataset.drop('URL', axis='columns', inplace=True)


# In[6]:


labels = np.array(dataset['sales_rank'])
features = dataset.drop(['sales_rank', 'bank_offer',
       'months', '5_rating', '4_rating', '3_rating', '2_rating', '1_rating',
       'feature2', 'feature3'], axis=1)
# Saving feature names for later use
feature_list = list(features.columns)
features = np.array(features)


# In[7]:


feature_list


# In[8]:


# Using Skicit-learn to split data into training and testing sets
from sklearn.model_selection import train_test_split

# Split the data into training and testing sets
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.2, random_state = 0)


# ## RandomizedSearchCV

# In[9]:


from sklearn.model_selection import RandomizedSearchCV


# In[25]:


# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 20, stop = 1000, num = 20)]
# Number of features to consider at every split
# max_features = ['auto', 'sqrt'] /'max_features': max_features,
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]
# Method of selecting samples for training each tree
# bootstrap = [True, False] /'bootstrap': bootstrap

# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
                }

print(random_grid)


# In[26]:


from sklearn.ensemble import RandomForestRegressor


# In[27]:


# Use the random grid to search for best hyperparameters
# First create the base model to tune
rf = RandomForestRegressor()
# Random search of parameters, using 3 fold cross validation, 
# search across 100 different combinations, and use all available cores
rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)

# Fit the random search model
rf_random.fit(features, labels)

"""The most important arguments in RandomizedSearchCV are n_iter, 
which controls the number of different combinations to try, and cv which is the number of folds to use for cross validation (we use 100 and 3 respectively). 
More iterations will cover a wider search space and more cv folds reduces the chances of overfitting, but raising each will increase the run time. 
Machine learning is a field of trade-offs, and performance vs time is one of the most fundamental."""


# In[28]:


# We can view the best parameters from fitting the random search:
rf_random.best_params_


# In[29]:


predictions = rf_random.predict(test_features)


# In[30]:


# Calculate the absolute errors
errors = abs(predictions - test_labels)

# Print out the mean absolute error (mae)
print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')


# In[31]:


# Calculate mean absolute percentage error (MAPE)
mape = 100 * (errors / test_labels)

# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')


# In[32]:


rf.fit(train_features, train_labels);


# In[33]:


# Get numerical feature importances
importances = list(rf.feature_importances_)

# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]

# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)

# Print out the feature and importances 
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];


# In[34]:


# Import matplotlib for plotting 
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')

# Set the style
plt.style.use('fivethirtyeight')

# list of x locations for plotting
x_values = list(range(len(importances)))

# Make a bar chart
plt.bar(x_values, importances, orientation = 'vertical')

# Tick labels for x axis
plt.xticks(x_values, feature_list, rotation = 'vertical')

# Axis labels and title
plt.ylabel('Importance')
plt.xlabel('Variable')
plt.title('Variable Importances');

