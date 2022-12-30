import config

from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

from dataset import Dataset, Item
from config import Config


app = FastAPI()

cfg = Config.load()


def init_dataset():
    # initialization logic here
    if cfg.init_mode == "latest":
        oqa = Dataset.load_from_pickle(cfg.latest_save)
        oqa.update_meta()
    elif cfg.init_mode == "json":
        oqa = Dataset()
        oqa.load_from_json(cfg.load_file)
    elif cfg.init_mode == "pickle":
        oqa = Dataset.load_from_pickle(cfg.load_file)
        oqa.update_meta()
    else:
        print("error")

    return oqa


oqa = init_dataset()

templates = Jinja2Templates(directory="./")

app.mount("/static", StaticFiles(directory="./static"), name="static")
app.mount("/js", StaticFiles(directory="./js"), name="js")


class sampleForm(BaseModel):
    qid: int
    question: str
    answer: str
    context: str
    context_id: Union[int, None] = None
    topic: str
    label: str


@app.get("/")
def read_root():
    return {"Hello": "Machine"}


@app.post("/posting/")
def update_sample(sample: sampleForm):
    # HERE update from item
    item = Item(
        qid=sample.qid,
        q=sample.question,
        a=sample.answer,
        c=sample.context,
        c_id=sample.context_id,
        t=sample.topic,
        label=sample.label,
    )
    oqa.update_from_item(item)

    return sample


@app.post("/export/")
def export_dataset(sample: sampleForm):
    """create the new sample based on the last question and add to the
    dataset"""
    item = Item(
        qid=sample.qid,
        q=sample.question,
        a=sample.answer,
        c=sample.context,
        c_id=sample.context_id,
        t=sample.topic,
        label=sample.label,
    )
    oqa.update_from_item(item)
    oqa.json_export()

    return 0


@app.post("/serialize/")
def serialize_dataset(sample: sampleForm):
    """create the new sample based on the last question and add to the
    dataset"""
    item = Item(
        qid=sample.qid,
        q=sample.question,
        a=sample.answer,
        c=sample.context,
        c_id=sample.context_id,
        t=sample.topic,
        label=sample.label,
    )
    oqa.update_from_item(item)
    oqa.serialize()

    return 0


@app.post("/new/")
def new_sample(sample: sampleForm):
    """create the new sample based on the last question and add to the
    dataset"""
    item = Item(
        qid=sample.qid,
        q=sample.question,
        a=sample.answer,
        c=sample.context,
        c_id=sample.context_id,
        t=sample.topic,
        label=sample.label,
    )
    oqa.update_from_item(item)
    new_id = oqa.new_sample(item)

    item = oqa.item_from_id(new_id)

    return new_id


@app.get("/sample/{loc}", response_class=HTMLResponse)
async def read_item(request: Request, loc: int):
    # from dataset
    item = oqa.item_from_loc(loc)

    qid = item.qid
    question = item.q
    answer = item.a
    context = item.c
    context_id = item.c_id
    label = item.label
    topic = item.t
    top_passages = list(zip(item.refs, item.passages))

    # format passages/references

    d = {
        "request": request,
        "loc": loc,
        "qid": qid,
        "question": question,
        "answer": answer,
        "context": context,
        "context_id": context_id,
        "label": label,
        "topic": topic,
        "top_passages": top_passages,
        "topics": oqa.topic_list,
        "labels": oqa.label_list,
    }

    return templates.TemplateResponse("ui_template.html", d)


# @app.get("/curate/{loc}", response_class=HTMLResponse)
# async def read_item(request: Request, loc: int):
