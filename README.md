# foodrhetoric
A network simulation of vegan food adoption using Theory of Planned Behavior.

The following is a work in progress.

## Background ##
The Theory of Planned Behavior (TBD) predicts that human behaviors largely depend on intentions to act (i.e. behavioral intentions), and that these intentions in turn depend on attitudes about those behaviors (i.e., behavioral attitudes) as well as beliefs about the attitudes of other people - often trusted or important people - about the behavior (i.e. subjective norms) [1]. It also holds that behavioral intentions depend on perceived behavioral control.

## Method ##
In this simulation, we randomly assign attitudes (between 0 and 1, where 1 is more positive) to two behaviors: eating real meat and eating vegan meat. We then create a random friendship network.  Using this social network of friends, we compute perceived subjective norms as the average behavioral attitude of each person's friends for each behavior.  Then we compute behavioral intentions as the average of the behavioral attitude and perceived subjective norm.  Finally, we treat the behavorial intention (which will be between 0 and 1) as the probability that the person will perform the behavior.  We then iterate multiple time steps and count up each behavior. finally, we export all the data to a CSV file.  This file also includes information about the friendship network in the form a dash-delimited sequence of friend ids.

## Analysis ##
To do.

## Discussion ##
To do. 

## References ##
[1] https://www.sciencedirect.com/science/article/abs/pii/074959789190020T

## Credit ##
This code was inspired and somewhat adapted from Damien Farrell's code here: 
https://dmnfarrell.github.io/bioinformatics/abm-mesa-network

