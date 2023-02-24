import os
import glob

import uvicorn

from absl import app
from absl import flags

from config import Config

# should reload be set to false so it does not reload the pkl file if not saved?
FLAGS = flags.FLAGS
flags.DEFINE_string(
    "save_path", "./save_data/", "set the save directory for the current project"
)
flags.DEFINE_string(
    "export_path", "./exports/", "set the export directory for the current project"
)
flags.DEFINE_string("load_from", None, "select a dataset file to load")
flags.DEFINE_string("mode", None, "select UI mode (curate, filter or browse)")


def main(argv):
    # configure the dataset initialization
    if FLAGS.load_from is None:

        # load from the latest file in
        file_list = list(glob.glob(os.path.join(FLAGS.save_path + "*.pkl")))
        file_list.sort(key=lambda x: os.path.getmtime(x))
        cfg = Config(
            save_path=FLAGS.save_path,
            export_path=FLAGS.export_path,
            latest_save=file_list[0],
        )

    else:
        # check extension (pkl or json) and load the file specified
        if FLAGS.load_from.endswith(".json"):
            cfg = Config(
                save_path=FLAGS.save_path,
                export_path=FLAGS.export_path,
                load_file=os.path.abspath(FLAGS.load_from),
                init_mode="json",
                view_mode=FLAGS.mode,
            )

        # only load from JSON for now... maybe parquet at some point...
        #         elif FLAGS.load_from.endswith(".pkl"):
        #             cfg = Config(
        #                 save_path=FLAGS.save_path,
        #                 export_path=FLAGS.export_path,
        #                 load_file=os.path.abspath(FLAGS.load_from),
        #                 init_mode="pickle",
        #             )
        else:
            print("error")

    # start the app
    cfg.dump()
    uvicorn.run("app:app", port=8000, reload=False)


if __name__ == "__main__":
    app.run(main)
