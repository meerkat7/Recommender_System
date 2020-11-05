Technique for Recommender System

Course Number: CS F469

Language: Python 3

This project is about implementing collaborative filtering for building a recommender system. 
It outputs the time taken for prediction, root mean square error, precision on top k and spearman rank 
correlation for this technique. 

The two implementations of a recommender system in this project are:-
1) Collaborative
2) Collaborative with baseline approach
3) SVD
4) SVD with 90% energy retained
5) CUR
6) CUR with 90% energy retained

Evaluation Metrics: RMSE, Spearman Rank Correlation, Precision at Top K External Libraries used: Numpy, Pandas, sci-kit learn

Dependencies: numpy, re, heapq, timeit, math, scipy, sklearn, random

Working:
1. Run CF.ipynb, CF_baseline.ipynb for collaborative filtering and 
 collaborative with baseline respectively.
2. After few minutes, the output will be displayed.


Acknowledgements:
I have used the ml-100k dataset for getting the user-movie ratings which can be downloaded from https://grouplens.org/datasets/movielens/100k/ link.


