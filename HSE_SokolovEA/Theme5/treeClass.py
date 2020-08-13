import numpy as np
from sklearn.base import BaseEstimator
from collections import Counter


def find_best_split(feature_vector, target_vector, min_samples_split=None):
    """
    Используется критерий Джини.

    :param feature_vector: вещественнозначный вектор значений признака
    :param target_vector: вектор классов объектов,  len(feature_vector) == len(target_vector)
    
    :return thresholds: отсортированный по возрастанию вектор со всеми возможными порогами, по которым объекты можно
     разделить на две различные подвыборки, или поддерева
    :return ginis: вектор со значениями критерия Джини для каждого из порогов в thresholds len(ginis) == len(thresholds)
    :return threshold_best: оптимальный порог (число)
    :return gini_best: оптимальное значение критерия Джини (число)
    """

    if min_samples_split is None:
        min_samples_split = 1
 
    sorted_indecies = feature_vector.argsort()
    feature_vector = feature_vector[sorted_indecies]
    target_vector = target_vector[sorted_indecies]
    
    sorted_feature, indecies = np.unique(feature_vector, return_index=True)
    thresholds = (sorted_feature[:-1] + sorted_feature[1:]) / 2
    
    m = thresholds.shape[0]
    n = feature_vector.shape[0]

    Rls = indecies[1:]
    Rrs = n - Rls
    pos_numb = target_vector.sum()
    
    pos_l = np.cumsum(target_vector)[indecies[1:] - 1]
    neg_l = Rls - pos_l
    pos_r = pos_numb - pos_l
    neg_r = Rrs - pos_r
    gini = - 2 / n * ( pos_l * neg_l / Rls + pos_r * neg_r / Rrs )
    
    indecies = (Rls >= min_samples_split) & (Rrs >= min_samples_split)
    gini_best = None
    threshold_best = None
    
    if np.sum(indecies) > 0:
        gini_best = np.amax(gini[indecies])
        threshold_best = np.amin(thresholds[gini == gini_best])
        
    return thresholds[indecies], gini[indecies], threshold_best, gini_best


class DecisionTree(BaseEstimator):
    def __init__(self, feature_types, max_depth=None, min_samples_split=2, min_samples_leaf=1):
        if np.any(
                list(
                    map(
                        lambda x: x != "real" and x != "categorical", feature_types
                        )
                     )
                  ):
            raise ValueError("There is unknown feature type")

        self._tree = {}
        self._feature_types = feature_types
        self._max_depth = max_depth
        self._min_samples_split = min_samples_split
        self._min_samples_leaf = min_samples_leaf
        
    def _fit_node(self, sub_X, sub_y, node, depth):
        # conditions for early exit: y is equal, depth is max or too little number of samples
        if np.all(sub_y == sub_y[0]) or \
           (self._max_depth is not None and depth == self._max_depth) or \
           (self._min_samples_split is not None and sub_y.shape[0] < self._min_samples_split):
                node["type"] = "terminal"
                node["class"] = Counter(sub_y).most_common(1)[0][0]
                
                return

        # Otherwise we are searching for the best split
        feature_best, threshold_best, gini_best, split = None, None, None, None
        
        for feature in range(sub_X.shape[1]):
            feature_type = self._feature_types[feature]
            categories_map = {}

            if feature_type == "real":
                feature_vector = sub_X[:, feature]
            elif feature_type == "categorical":
                counts = Counter(sub_X[:, feature])
                clicks = Counter(sub_X[sub_y == 1, feature])
                ratio = {}
                
                for key, current_count in counts.items():
                    if key in clicks:
                        current_click = clicks[key]
                    else:
                        current_click = 0
                    ratio[key] = current_click / current_count
                
                categories_map = ratio
                feature_vector = np.array(list(map(lambda x: ratio[x], sub_X[:, feature])))
            else:
                raise ValueError
            
            # if we can not split -- we skip it
            if len(np.unique(feature_vector)) == 1:
                continue
             
            _, _, threshold, gini = find_best_split(feature_vector, sub_y, self._min_samples_leaf)
            
            if gini is not None and (gini_best is None or gini > gini_best):
                feature_best = feature
                gini_best = gini
                split = feature_vector < threshold

                if feature_type == "real":
                    threshold_best = threshold
                elif feature_type == "categorical":
                    threshold_best = list(map(lambda x: x[0],
                                              list(filter(
                                                          lambda x: x[1] < threshold, categories_map.items()
                                                          )
                                                    )))
                else:
                    raise ValueError
 
        # if we can not split using any feature -- finish
        if feature_best is None:
            node["type"] = "terminal"
            node["class"] = Counter(sub_y).most_common(1)[0][0]
            return

        # otherwise split it!
        node["type"] = "nonterminal"

        node["feature_split"] = feature_best
        if self._feature_types[feature_best] == "real":
            node["threshold"] = threshold_best
        elif self._feature_types[feature_best] == "categorical":
            node["categories_split"] = threshold_best
        else: 
            raise ValueError
            
        # start building recursively
        node["left_child"], node["right_child"] = {}, {}
        self._fit_node(sub_X[split], sub_y[split], node["left_child"], depth+1)
        self._fit_node(sub_X[np.logical_not(split)], sub_y[np.logical_not(split)], node["right_child"], depth+1)

    def _predict_node(self, x, node):
        if node["type"] == "terminal":
            return node["class"]
        
        feature_best = node["feature_split"]             
        next_node = {}
        
        if self._feature_types[feature_best] == 'real':
            if x[feature_best] < node["threshold"]:
                next_node = node["left_child"]
            else:
                next_node = node["right_child"]
        elif self._feature_types[feature_best] == "categorical":
            if x[feature_best] in node["categories_split"]:
                next_node = node["left_child"]
            else:
                next_node = node["right_child"]
        else:
            raise ValueError
            
        return self._predict_node(x, next_node)

    def fit(self, X, y):
        self._fit_node(X, y, self._tree, 0)
        return self
    

    def predict(self, X):
        predicted = []
        for x in X:
            predicted.append(self._predict_node(x, self._tree))
            
        return np.array(predicted)