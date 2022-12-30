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


def retrievalFmt(meta_path, dataset_path):
    """create dataset for retrieval evaluation"""
    examples = []

    f = open(meta_path, "rb")
    meta_list = json.load(f)
    f.close()

    with open(dataset_path, "rb") as f:
        d = json.load(f)
        d = d[:200]
        for i in d:
            qid = i["id"]
            context = i["context"]
            question = i["question"]
            answer = i["answer"]
            c_id = int(i["context_id"])

            # import IPython ; IPython.embed() ; quit()
            meta_string = i["top_passages"][c_id][0]["meta"]

            context_key = None
            for m in meta_list:
                if m["meta"] == meta_string:
                    context_key = m["article_id"]
                    break

            if context_key == None:
                print("unresolved context key")
                break
            examples.append(
                {
                    "id": qid,
                    "question": question,
                    "answer": answer,
                    "context": context,
                    "context_key": context_key,
                }
            )

    return examples


def jsonExport(path, sample_list):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sample_list, f, ensure_ascii=False, indent=2)


# format for retrieval (document and page)
# evaluate


def get_valid(ds):
    valid_set = []
    for i in range(ds.n_samples):
        sample = ds.item_from_id(i)
        if sample.label == "valid":
            try:
                valid_sample = {}
                valid_sample["id"] = sample.qid
                valid_sample["topic"] = sample.t
                valid_sample["question"] = sample.q
                valid_sample["answer"] = sample.a
                valid_sample["passage"] = sample.c
                valid_sample["meta"] = sample.refs[int(sample.c_id)]
                valid_sample["reference_text"] = sample.passages[int(sample.c_id)]
                # valid_sample["document"] =  # @TODO path to pdf (images to be created on the fly?)

                valid_set.append(valid_sample)
            except:
                raise TypeError("sample {}".format(i))

    return valid_set


# ds = Dataset.load_from_pickle("./save_data/oqa.pkl")
# docpath = "C:/Users/roum5/source/data"
# ds.update_meta()
# test_val = get_valid(ds)
