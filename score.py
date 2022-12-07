def calc_mrr(predict, answer):
    for i in range(len(predict)):
        if predict[i] == answer:
            return 1. / (i + 1)
    return 0

max_prediction_len = 100

def calc_score(target_path, predict_path):
    with open(target_path) as f:
        y_true = [int(x.strip()) for x in f.readlines()]

    with open(predict_path) as f:
        y_pred = [[int(x) for x in line.strip().split(' ')] for line in f.readlines()]

    mrr_score = 0
    for (pred, answer) in zip(y_pred, y_true):
        if len(pred) > max_prediction_len:
            raise ValueError('$maximum prediction length is {}, got {}$'.format(max_prediction_len, len(y_pred[i])))
        mrr_score += calc_mrr(pred, answer)

    print("MRR@100 = {}".format(mrr_score / len(y_true)))

calc_score("true_answers.csv", "result")