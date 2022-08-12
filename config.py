from dataclasses import dataclass
import pickle


@dataclass
class Config:
    save_path: str
    export_path: str
    latest_save: str = None
    load_file: str = None
    init_mode: str = "latest"

    def dump(self):
        with open("./.conf.pkl", "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load():
        with open("./.conf.pkl", "rb") as f:
            return pickle.load(f)
