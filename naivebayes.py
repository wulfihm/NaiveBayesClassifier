"""
This file is for the methods concerning everything naive bayes

1. separate it in 2 clusters(1 Training , 2 Test) [DONE]
2. calculate all probabilities from training data [DONE]
3. afterwards make a function to use this probabilities and to decide to which class it is belonged
4. calculate error rate
5. Determine the mean error rate over 100 different random samples of training data.
"""


def calculate_probabilities(classes: list, attributes: list, attribute_values: list, instances: list):
    """
    function for calculation of probabilities of classes and attributes and their corresponding classes

    :param classes: is a one-dimensional list containing the class names
    :param attributes: is one dimensional list that contains the names of attributes
    :param attribute_values: is a two-dimensional list where each row respresents
            one attribute(in the order of 'attributes') and the possible values
    :param instances: is a two-dimensional list where each row respresents
          one attribute(in the order of 'attributes') and the possible values
    :return:
    numclassinstances: a 2-dimensional list containg the classes, the total frequency, the number of total instances
    and the fraction of instances being that class
    attributeline:  a x-dimensional list containg the attributes with their values and how many of these values
    correspond to a specific class
    """
    if len(instances) == 0:
        return 0, []
    classinstances = [row[-1] for row in instances]
    numclassinstances = []
    num_instances = len(classinstances)
    for dclass in classes:
        classfrequency = sum(inst[0] == dclass[0] for inst in classinstances)
        classprobline = [dclass, classfrequency, num_instances, classfrequency/num_instances]
        numclassinstances.append(classprobline)

    attributeline = []
    for i in range(0, len(attributes)):
        valueslines = []
        for k in range(0, len(attribute_values[i])):
            classprob = []
            for p in range(0, len(classes)):
                classattrbfrequency = sum((inst[-1] == classes[p] and inst[i] == attribute_values[i][k]) for inst in instances)
                # attribute probability with laplace smoothing and assuming uniform distribution
                attrbprobability = (classattrbfrequency + 1/len(attribute_values[i])) / (numclassinstances[p][1] + 1)
                # without laplace smoothing
                # attrbprobability = (classattrbfrequency) / (numclassinstances[p][1])
                classprob.append([classes[p], attrbprobability])

            valueline = [attribute_values[i][k], classprob]
            valueslines.append(valueline)

        attributeline.append([attributes[i], valueslines])

    return numclassinstances, attributeline


def class_probability(numclassinstances: list, attributeline: list, inputvector):
    probs = []
    for i in range(len(numclassinstances)):  # iterate over classes
        probofclass = numclassinstances[i][3]  # get class probability
        for j in range(len(attributeline)):  # iterate over attributes
            for k in range(len(attributeline[j][1])):  # iterate over attribute values
                if attributeline[j][1][k][0] == inputvector[j]:
                    probofclass *= attributeline[j][1][k][1][i][1] # get value-class probability
        probs.append(probofclass)
    return probs


def choosing_of_class(probs: list, numclassinstances: list):
    maxprob = 0
    index = 0
    for i in range(len(probs)):
        if probs[i] > maxprob:
            maxprob = probs[i]
            index = i
    return numclassinstances[index], maxprob
