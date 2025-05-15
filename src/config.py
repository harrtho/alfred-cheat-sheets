#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Separated unit for configuration, in case we have extra features in the future.
from workflow import Workflow
from libs.config import Config
from workflow.notify import notify

def main(wf):
    path=wf.args[0].strip()
    config=Config(path)
    if config.validate():
        # Behavior: overwrite existing data
        wf.store_data("configuration", config)
        notify(title="Success!", message="Cheat sheets updated to {}".format(config.getPath()))
    else:
        notify(title="Error:(", message="The path doesn't exist")
    return 0

if __name__=="__main__":
    wf=Workflow()
    exit(wf.run(main))
