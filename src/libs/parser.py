#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path

from workflow import MATCH_ALL, MATCH_ALLCHARS


class Parser:
    def __init__(self, path):
        self._path = path
        self._sheetMapping = {}  # {cheatsheet: /home/somedir/cheatsheet}
        self._available = self._enumAvailableSheets()
        return None

    def availableSheets(self):
        return self._available

    def _enumAvailableSheets(self):
        sheets = []
        for root, dirname, files in os.walk(self._path, followlinks=True):
            # Ignore hidden directories
            dirname[:] = [d for d in dirname if not d.startswith(".")]
            # Only visible markdown files
            md_files = [f for f in files if not f.startswith(".") and f.endswith(".md")]

            for f in md_files:
                rel_path = os.path.relpath(os.path.join(root, f), self._path)
                cheatsheet_name = os.path.splitext(rel_path)[0]
                sheets.append(cheatsheet_name)

        # Update the cheat sheet mapping so that we can find the file location
        self._sheetMapping.update({sheet: os.path.join(self._path, sheet + ".md") for sheet in sheets})

        return sheets

    def list(self, sheetName):
        return [] if sheetName not in self._available else self.__parseSheet(sheetName)  # return value: [{}, {}, {}, ...]

    def searchAcrossAll(self, keyword, wf):
        ret = []
        for sheet in self._available:
            ret.extend(self.__parseSheet(sheet))
        return self.filter(ret, keyword, wf)  # [{}, {}, {}...]

    def searchInSheet(self, keyword, sheetName, wf):
        return self.filter(self.__parseSheet(sheetName), keyword, wf)

    def __parseSheet(self, filename):
        with open(self._sheetMapping.get(filename), 'r') as f:
            content = f.read().strip()
        # Tokenize to get each "item" by spliting the "\n\n". This rule must be repspected
        content = [item.strip() for item in content.split("\n\n")]
        # ASSUME the item pattern is "comment, comment, comment ..., command"
        # An item doesn't have to contain comments but must have a command
        items = []
        for item in content:
            try:
                comment, command = item.rsplit("\n", 1)
            except ValueError:
                continue
            # Or you wanna see which line doesn't comform to the format
            #   comment=""
            #   command="Fail to parse: {}".format(item)
            # cleanup "#" and \n
            comment = comment.replace("#", "").replace("\n", ". ").strip()
            command = command.strip()
            items.append((comment, command))
        return [dict(comment=comment, command=command) for comment, command in items]  # [{}, {}, {}...]

    def filter(self, content, keyword, wf):
        def searchIndex(item):
            return " ".join([item["comment"], item["command"]])
        return wf.filter(keyword, content, key=searchIndex, match_on=MATCH_ALL ^ MATCH_ALLCHARS, min_score=50)
