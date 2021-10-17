'''
Linear regression

Main file for linear regression and model selection.
'''

import numpy as np
from sklearn.model_selection import train_test_split
import util


class DataSet(object):
    '''
    Class for representing a data set.
    '''

    def __init__(self, dir_path):
        '''
        Class for representing a dataset, performs train/test
        splitting.

        Inputs:
            dir_path: (string) path to the directory that contains the
              file
        '''

        parameters_dict = util.load_json_file(dir_path, "parameters.json")
        self.pred_vars = parameters_dict["predictor_vars"]
        self.name = parameters_dict["name"]
        self.dependent_var = parameters_dict["dependent_var"]
        self.training_fraction = parameters_dict["training_fraction"]
        self.seed = parameters_dict["seed"]
        self.labels, data = util.load_numpy_array(dir_path, "data.csv")
        self.training_data, self.testing_data = train_test_split(data,
            train_size=self.training_fraction, test_size=None,
            random_state=self.seed)

class Model(object):
    '''
    Class for representing a model.
    '''

    def __init__(self, dataset, pred_vars):
        '''
        Construct a data structure to hold the model.
        Inputs:
            dataset: an dataset instance
            pred_vars: a list of the indices for the columns (of the
              original data array) used in the model.
        '''
        self.training_data = dataset.training_data
        self.testing_data = dataset.testing_data
        self.dep_var = dataset.dependent_var
        self.training_dep_vars = self.training_data[:, self.dep_var]
        self.testing_dep_vars = self.testing_data[:, self.dep_var]
        self.pred_vars = pred_vars
        self.training_pred_vars = util.prepend_ones_column(self.training_data[:, pred_vars])
        self.testing_pred_vars = util.prepend_ones_column(self.testing_data[:, pred_vars])
        self.beta = self.compute_beta()
        self.R2 = self.compute_R2()
        self.testing_R2 = self.compute_R2(True)

    def __repr__(self):
        '''
        Format model as a string.
        '''

        return "This model has predictor variables at columns {}, dependent variable at column {},\
            and R2 value {}".format(self.pred_vars, self.dep_var, self.R2)

    def compute_beta(self):
        """
        Compute the beta value based on the training set
        """

    def compute_R2(self, testing=False):
        """
        Compute the R2 value for the training or
          testing set

        Inputs:
            testing (boolean): whether to use the
              training or testing set to compute the value
        """


def compute_single_var_models(dataset):
    '''
    Computes all the single-variable models for a dataset

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        List of Model objects, each representing a single-variable model
    '''


def compute_all_vars_model(dataset):
    '''
    Computes a model that uses all the predictor variables in the dataset

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A Model object that uses all the predictor variables
    '''


def compute_best_pair(dataset):
    '''
    Find the bivariate model with the best R2 value

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A Model object for the best bivariate model
    '''


def forward_selection(dataset):
    '''
    Given a dataset with P predictor variables, uses forward selection to
    select models for every value of K between 1 and P.

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A list (of length P) of Model objects. The first element is the
        model where K=1, the second element is the model where K=2, and so on.
    '''


def validate_model(dataset, model):
    '''
    Given a dataset and a model trained on the training data,
    compute the R2 of applying that model to the testing data.

    Inputs:
        dataset: (DataSet object) a dataset
        model: (Model object) A model that must have been trained
           on the dataset's training data.

    Returns:
        (float) An R2 value
    '''