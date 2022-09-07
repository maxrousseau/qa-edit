import os
import json
import pickle
from datetime import datetime

from dataclasses import dataclass, field

# @TODO :: add some logging functionalities (verbose and debug)


@dataclass
class Item:
    qid: int
    q: str
    a: str
    c: str
    c_id: int
    t: str
    label: str
    passages: list = field(default_factory=lambda: None)
    refs: list = field(default_factory=lambda: None)


@dataclass
class Dataset:
    """A dynamic dataset stored in this class"""

    name: str = "oqa"
    save_dir: str = os.path.abspath("./save_data/")
    export_dir: str = os.path.abspath("./exports/")
    save_path: str = None
    export_path: str = None

    # sample arrays
    idx: list = field(default_factory=lambda: [])
    labels: list = field(default_factory=lambda: [])
    topics: list = field(default_factory=lambda: [])
    questions: list = field(default_factory=lambda: [])
    answers: list = field(default_factory=lambda: [])
    contexts: list = field(default_factory=lambda: [])
    context_ids: list = field(default_factory=lambda: [])
    top_passages: list = field(default_factory=lambda: [])
    top_passages_refs: list = field(default_factory=lambda: [])

    n_samples: int = 0
    n_unlabeled: int = 0
    n_valid: int = 0
    n_review: int = 0
    n_discard: int = 0

    topic_list: list = field(
        default_factory=lambda: [
            "none",
            "biomechanics",
            "biology",
            "anatomy",
            "pathology",
            "materials",
            "growth",
            "clinical",
            "tmj",
        ]
    )

    label_list: list = field(
        default_factory=lambda: [
            "unlabeled",
            "valid",
            "review",
            "discard",
        ]
    )

    def populate_from_dict(self, dataset_dict):
        """populate the fields of the datastructure from a dict containing correct fields"""
        for i in dataset_dict:
            self.idx.append(i["id"])
            self.labels.append(i["label"])
            self.topics.append(i["topic"])
            self.questions.append(i["question"])
            self.answers.append(i["answer"])
            self.contexts.append(i["context"])
            self.context_ids.append(i["context_id"])
            self.top_passages.append([x[1] for x in i["top_passages"]])
            self.top_passages_refs.append([x[0] for x in i["top_passages"]])

    def update_meta(self):
        """update the statistics from the current dataset"""
        self.n_samples = len(self.labels)

        self.n_valid = self.n_discard = self.n_review = self.n_unlabeled = 0

        for i in range(self.n_samples):
            label = self.labels[i]
            if label == "valid":
                self.n_valid += 1
            elif label == "review":
                self.n_review += 1
            elif label == "discard":
                self.n_discard += 1
            elif label == "unlabeled":
                self.n_unlabeled += 1
            else:
                print("[ERROR] :: label not found at index {}".format(i))

        fields = [
            self.labels,
            self.topics,
            self.questions,
            self.answers,
            self.contexts,
            self.context_ids,
            self.top_passages,
            self.top_passages_refs,
        ]

        # make sure that the number of items in each field match the number of
        # samples
        assert all([len(x) == self.n_samples for x in fields])

    @staticmethod
    def load_from_pickle(path):
        with open(path, "rb") as f:
            return pickle.load(f)

    def load_from_json(self, path):
        # @TODO :: should check if all attributes are unpopulated other this will
        # keep appending data to the class
        with open(path, "rb") as f:
            d = json.load(f)
            self.populate_from_dict(d)
        self.update_meta()
        return self

    def rename(self, n):
        self.name = n

    def item_from_loc(self, loc):
        item = Item(
            qid=self.idx[loc],
            label=self.labels[loc],
            t=self.topics[loc],
            q=self.questions[loc],
            a=self.answers[loc],
            c=self.contexts[loc],
            c_id=self.context_ids[loc],
            passages=self.top_passages[loc],
            refs=self.top_passages_refs[loc],
        )
        return item

    def item_from_id(self, sample_id):
        # @BUG use loc variable to map to the location of the id in the array
        loc = self.idx.index(sample_id)
        item = Item(
            qid=sample_id,
            label=self.labels[loc],
            t=self.topics[loc],
            q=self.questions[loc],
            a=self.answers[loc],
            c=self.contexts[loc],
            c_id=self.context_ids[loc],
            passages=self.top_passages[loc],
            refs=self.top_passages_refs[loc],
        )
        return item

    def update_from_item(self, item):
        """only update label, question, answer and context"""
        loc = self.idx.index(item.qid)
        self.answers[loc] = item.a
        self.questions[loc] = item.q
        self.topics[loc] = item.t
        self.contexts[loc] = item.c
        self.context_ids[loc] = item.c_id
        self.labels[loc] = item.label

    def new_sample(self, last_sample):
        """create a new sample and appends to dataset"""
        # @BUG could be broken if not used with the full dataset because then
        # the id could be duplicated
        new_id = len(self.questions)

        self.labels.append(self.label_list[0])
        self.topics.append(self.topic_list[0])
        self.answers.append("[NEW] :: " + last_sample.a)
        self.questions.append("[NEW] :: " + last_sample.q)
        self.contexts.append("[NEW] :: " + last_sample.c)
        self.context_ids.append(None)
        self.top_passages.append(self.top_passages[last_sample.qid])
        self.top_passages_refs.append(self.top_passages_refs[last_sample.qid])

        self.update_meta()

        return new_id

    def serialize(self):
        """specify path to write dump dataset object to, will overwrite"""
        # if the fpath is not specified overwrite the current file
        self.save_path = os.path.join(self.save_dir, (self.name + ".pkl"))

        if os.path.isdir(self.save_dir):
            pass
        else:
            os.makedirs(self.save_dir)

        with open(self.save_path, "wb") as f:
            pickle.dump(self, f)

    def json_export(self, fpath=None):
        """export the dataset to a language agnostic format (JSON)"""
        # create a dict with all the elements
        sample_list = []

        for i in range(self.n_samples):
            sample = {}
            sample["id"] = self.idx[i]
            sample["label"] = self.labels[i]
            sample["topic"] = self.topics[i]
            sample["question"] = self.questions[i]
            sample["answer"] = self.answers[i]
            sample["context"] = self.contexts[i]
            sample["context_id"] = self.context_ids[i]
            sample["top_passages"] = list(
                zip(self.top_passages_refs[i], self.top_passages[i])
            )
            sample_list.append(sample)

        if os.path.isdir(self.export_dir):
            pass
        else:
            os.makedirs(self.export_dir)

        if fpath is None:
            t = datetime.today()
            timestamp = "{}-{}-{}-{}h{}".format(
                t.year, t.month, t.day, t.hour, t.minute
            )
            self.export_path = os.path.abspath(
                os.path.join(self.export_dir, "{}_{}.json".format(self.name, timestamp))
            )
        with open(self.export_path, "w", encoding="utf-8") as f:
            json.dump(sample_list, f, ensure_ascii=False, indent=2)
