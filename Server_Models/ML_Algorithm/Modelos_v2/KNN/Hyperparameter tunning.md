Hyperparameter Tuning:
    This is the process of adjusting the hyperparameters of a machine learning model to improve its performance. Hyperparameters are settings that aren't learned from the data; instead, they are set by the model developer before training starts. For K-NN, the hyperparameter in question is k (i.e., the number of neighbors).
    The main goal is to find the hyperparameter values that give the best performance on the validation set (or during cross-validation).
    Methods to perform hyperparameter tuning include grid search, random search, Bayesian optimization, and gradient-based optimization.

Cross-Validation:
    Cross-validation is a technique to assess how well a model will perform on an independent dataset.
    The most common method is k-fold cross-validation, where the training dataset is split into k folds. The model is trained on k-1 of those folds and tested on the remaining fold. This process is repeated k times, each time using a different fold as the test set. The final performance metric is the average of the performance metrics from each iteration.
    Cross-validation is used during hyperparameter tuning. For example, during a grid search for k in K-NN, each potential value of k will be evaluated using cross-validation to see how well the model performs with that value of k.

In essence, hyperparameter tuning is the broader task of finding the best settings for your model. Cross-validation is a technique used during this process to evaluate how good different hyperparameter settings are


