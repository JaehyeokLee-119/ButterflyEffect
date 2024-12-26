import re
import string
import pandas as pd
from collections import Counter

def normalize_answer(s: str):
    def remove_articles(text):
        return re.sub(r"\b(a|an|the)\b", " ", text)
    
    def white_space_fix(text):
        return " ".join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))

def exact_match_score(prediction, ground_truth):
    return (normalize_answer(prediction) == normalize_answer(ground_truth))

def f1_score(prediction, ground_truth):
    normalized_prediction = normalize_answer(prediction)
    normalized_ground_truth = normalize_answer(ground_truth)

    ZERO_METRIC = (0, 0, 0)

    if normalized_prediction in ['yes', 'no', 'noanswer'] and normalized_prediction != normalized_ground_truth:
        return ZERO_METRIC
    if normalized_ground_truth in ['yes', 'no', 'noanswer'] and normalized_prediction != normalized_ground_truth:
        return ZERO_METRIC

    prediction_tokens = normalized_prediction.split()
    ground_truth_tokens = normalized_ground_truth.split()
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return ZERO_METRIC
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1, precision, recall

def update_answer(metrics, prediction, gold):
    em = exact_match_score(prediction, gold)
    f1, prec, recall = f1_score(prediction, gold)
    metrics['em'] += float(em)
    metrics['f1'] += f1
    metrics['prec'] += prec
    metrics['recall'] += recall
    return em, prec, recall

def update_sp(metrics, prediction, gold):
    cur_sp_pred = set(map(tuple, prediction))
    gold_sp_pred = set(map(tuple, gold))
    tp, fp, fn = 0, 0, 0
    for e in cur_sp_pred:
        if e in gold_sp_pred:
            tp += 1
        else:
            fp += 1
    for e in gold_sp_pred:
        if e not in cur_sp_pred:
            fn += 1
    prec = 1.0 * tp / (tp + fp) if tp + fp > 0 else 0.0
    recall = 1.0 * tp / (tp + fn) if tp + fn > 0 else 0.0
    f1 = 2 * prec * recall / (prec + recall) if prec + recall > 0 else 0.0
    em = 1.0 if fp + fn == 0 else 0.0
    metrics['sp_em'] += em
    metrics['sp_f1'] += f1
    metrics['sp_prec'] += prec
    metrics['sp_recall'] += recall
    return em, prec, recall


def evaluate(df):
    answer_metric = {'em':0, 'f1':0, 'prec':0, 'recall':0}
    sp_metric = {'sp_em':0, 'sp_f1':0, 'sp_prec':0, 'sp_recall':0}
    for i in range(len(df)):
        gold = df.iloc[i]['answer']
        pred = df.iloc[i]['predict']
        gold_sp = df.iloc[i]['supporting_documents']
        pred_sp = df.iloc[i]['search_documents']
        update_answer(answer_metric, pred, gold)
        update_sp(sp_metric, pred_sp, gold_sp)
    for k in answer_metric.keys():
        answer_metric[k] /= len(df)
    for k in sp_metric.keys():
        sp_metric[k] /= len(df)
    return answer_metric, sp_metric

def make_df(dataset):
    df = pd.DataFrame()
    df['question'] = dataset['question']
    df['answer'] = dataset['answer']
    supporting_documents = []
    for sf in dataset['supporting_facts']:
        title_list = []
        for title in sf['title']:
            if title not in title_list:
                title_list.append(title)
        supporting_documents.append(title_list)
    df['supporting_documents'] = supporting_documents
    df['predict'] = [""] * len(df)
    df['search_documents'] = [""] * len(df)
    df= df[['question', 'predict', 'answer', 'search_documents', 'supporting_documents']]
    
    return df


