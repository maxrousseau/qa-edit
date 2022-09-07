from dataset import Dataset, Item
import json
import pickle

import random


def getValidSamples(full_set):
    valid = []
    with open(full_set, "rb") as f:
        d = json.load(f)
        for i in d:
            if i["label"] == "valid":
                valid.append(i)

    valid_set = Dataset()
    valid_set.populate_from_dict(valid)
    return valid_set


def pklExport(save_path, dataset):
    with open(save_path, "wb") as f:
        pickle.dump(dataset, f)


# def item_to_sample(item):
#     sample = {
#         "id" : item.qid,
#         "question" : item.q,
#         "answer" : item.answer
#     }

# load json
# format to squad
# randomize
# preprocess (lower case)


def squadFmt(path):
    """build a dict in squad format"""
    sqd = []
    random.seed(0)

    with open(path, "rb") as f:
        d = json.load(f)
        d = d[:200]
        for i in d:
            qid = i["id"]
            context = i["context"]
            question = i["question"]
            answer_start = context.find(i["answer"])
            assert answer_start != -1

            answers = {"answer_start": [answer_start], "text": [i["answer"]]}

            sqd.append(
                {
                    "id": qid,
                    "answers": answers,
                    "question": question,
                    "context": context,
                    "title": "oqa_v0.1_200",
                }
            )
    random.shuffle(sqd)
    train = sqd[:100]
    test = sqd[100:]
    return (train, test)


def jsonExport(path, sample_list):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sample_list, f, ensure_ascii=False, indent=2)


# format for retrieval (document and page)
# evaluate
