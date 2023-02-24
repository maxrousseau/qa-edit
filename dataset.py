import os
import json
import pickle
from datetime import datetime

from dataclasses import dataclass, field
import uuid

# @TODO :: add some logging functionalities (verbose and debug)


topic_list = [
    "none",
    "biomechanics",
    "biology",
    "anatomy",
    "pathology",
    "materials",
    "growth",
    "clinical",
    "other",
]


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


# @TODO make iterable for future use...
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

        self.n_samples = len(self.idx) - 1

        fields = [
            self.idx,
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
        try:
            assert all([len(x) == self.n_samples + 1 for x in fields])

        except:
            # delete corrupted samples @BUG modify this later on...
            self.idx = self.idx[: self.n_samples]
            self.labels = self.labels[: self.n_samples]
            self.topics = self.topics[: self.n_samples]
            self.questions = self.questions[: self.n_samples]
            self.answers = self.answers[: self.n_samples]
            self.contexts = self.contexts[: self.n_samples]
            self.context_ids = self.context_ids[: self.n_samples]
            self.top_passages = self.top_passages[: self.n_samples]
            self.top_passages_refs = self.top_passages_refs[: self.n_samples]

            fields = [
                self.idx,
                self.labels,
                self.topics,
                self.questions,
                self.answers,
                self.contexts,
                self.context_ids,
                self.top_passages,
                self.top_passages_refs,
            ]

            print(len(self.idx))
            print(len(self.labels))
            print(self.n_samples)

            return [len(x) == self.n_samples for x in fields]
            assert all([len(x) == self.n_samples for x in fields])

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

        # @BUG This is broken if not used with the full dataset because then the id could be duplicated. The whole
        # question id system needs to be re-written and use generated UUIDs and check for duplicates before adding a new
        # sample (fix this before moving to the curation phase of the valid samples)
        new_id = len(self.questions)

        self.idx.append(new_id)
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


@dataclass
class Sample:
    qid: int
    uuid: str
    question: str
    answer: str
    context: str
    topic: str
    subtopic: str
    source_page: str
    export: bool
    reference: dict = field(default_factory=lambda: None)  #

    def to_dict(self):
        # @NOTE :: make compatible with previously used fields
        return {
            "id": self.qid,
            "uuid": self.uuid,
            "question": self.question,
            "answer": self.answer,
            "passage": self.context,
            "topic": self.topic,
            "subtopic": self.subtopic,
            "reference_text": self.source_page,
            "meta": self.reference,
        }


@dataclass
class Dataset2:

    name: str = "oqa-v0.0"
    save_dir: str = os.path.abspath("./save_data/")
    export_dir: str = os.path.abspath("./exports/")
    save_path: str = None
    export_path: str = None

    samples: list = field(default_factory=lambda: [])

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, key):
        """returns a samples from location in list"""
        return self.samples[key]

    def __setitem__(self, key, value):
        """modifies a sample at location in list"""
        self.samples[key] = value

    def __delitem__(self, key):
        """deletes a sample at location in list"""
        # @TODO :: send to a trash list to retrieve if needed...
        self.samples[key] = value

    def __sample_from_dict(self, sample_dict):

        if "uuid" in sample_dict.keys():
            return Sample(
                qid=sample_dict["id"],
                uuid=sample_dict["uuid"],
                question=sample_dict["question"],
                answer=sample_dict["answer"],
                context=sample_dict["passage"],
                topic=sample_dict["topic"],
                subtopic=sample_dict["subtopic"],  # only after v0.3
                source_page=sample_dict["reference_text"],
                reference=sample_dict["meta"],
                export=True,
            )
        else:
            return Sample(
                qid=sample_dict["id"],
                uuid=str(uuid.uuid4()),
                question=sample_dict["question"],
                answer=sample_dict["answer"],
                context=sample_dict["passage"],
                topic=sample_dict["topic"],
                source_page=sample_dict["reference_text"],
                reference=sample_dict["meta"],
            )

    def load_from_json(self, path):
        """load json, create samples and append to sample_list"""
        if self.samples == []:
            with open(path, "rb") as f:
                d = json.load(f)
                for i in d:
                    self.samples.append(self.__sample_from_dict(i))
        else:
            raise Exception(
                "Samples already loaded, create an empty instance before loading from json."
            )

    def rename(self, newname):
        self.name = newname

    def add(self, loc):
        """create a new sample with fields from current samples"""
        self.samples.append(
            Sample(
                qid=self.samples[loc].qid
                + 900000,  # keep the last 4 numbers of the initial id
                uuid=str(uuid.uuid4()),
                question="[NEW] :: " + self.samples[loc].question,
                answer="[NEW] :: " + self.samples[loc].answer,
                context="[NEW] :: " + self.samples[loc].context,
                topic=self.samples[loc].topic,
                subtopic=self.samples[loc].subtopic,
                source_page=self.samples[loc].source_page,
                reference=self.samples[loc].reference,
                export=True,
            )
        )

    def export(self, fpath=None):
        """export the dataset to json"""
        sample_list = []
        for i in self.samples:
            if i.export == True:
                sample_list.append(i.to_dict())

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
        else:
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(sample_list, f, ensure_ascii=False, indent=2)
