#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from workflow import Workflow
from libs.parser import Parser
from libs.options import Options


def main(workflow):
    # Try to read configuration from local disk
    config = workflow.stored_data("configuration")
    if config is None:
        Options.warning("Didn't find your configuration", "Please supply your cheat sheet path using 'cf ~/your/path'", workflow)
        workflow.send_feedback()
        return -1

    parser = Parser(config.getPath())
    # Note: by pasing workflow as a variable, its state is changed in Options.py logic
    options = Options(parser, workflow)

    # Query is whatever comes after "cheat". Stored in one single variable
    query = "" if len(workflow.args) == 0 else workflow.args[0]
    # Split the query into two parts: sheetName and searchTerm
    query_tokens = query.strip().split(" ")
    query_tokens = [i.strip() for i in query_tokens if i != ""]

    # If the query is empty, show available sheets
    if len(query_tokens) == 0:
        options.showAvailable()
        workflow.send_feedback()
        return None
    # If the query is "--search" or "-s", show hint for global search
    elif len(query_tokens) == 1 and query_tokens[0] in ("--search", "-s"):
        Options.hint("Globally searching for ...?", "In global mode", workflow)
        workflow.send_feedback()
        return None
    # If the query is a global search, create a search term
    elif query_tokens[0] in ("--search", "-s"):
        sheetName = None
        searchTerm = ''.join(query_tokens[1:])
    # Search for a sheet name and a search term
    else:
        sheets_tokens = [i.split(" ") for i in parser.availableSheets()]
        sheetName = None
        searchTerm = None
        search_term_index = 0
        # Iterate over all available sheets sorted by length.
        # This is to find the longest sheet name that matches the query
        # and to avoid false positives.
        # For example, if the query is "Fancy Query" and there are sheets "Fancy"
        # and "Fancy Query", we want to match "Fancy Query" and not "Fancy".
        # This is to avoid false positives.
        for sheet_tokens in sorted(sheets_tokens, key=len):
            count_tokens = len(sheet_tokens)

            for index, query_token in enumerate(query_tokens):
                if query_token != sheet_tokens[index]:
                    break

                if index == count_tokens - 1:
                    search_term_index = index + 1
                    sheetName = ' '.join(sheet_tokens)
                    workflow.logger.debug(f"found sheet name '{sheetName}' in query '{query}'")
                    break

        if sheetName is None:
            options.showAvailable(' '.join(query_tokens))
            workflow.send_feedback()
            return None
        # If there is still more than one option as sheet name, show available sheets
        elif len(options.filterSheetName(' '.join(query_tokens))) - 1 > 0:
            options.showAvailable(' '.join(query_tokens))
            searchTerm = ' '.join(query_tokens[search_term_index:])
            workflow.logger.debug(f"extract search term '{searchTerm}' from query '{query}'")
        elif len(query_tokens[search_term_index:]) == 0:
            options.list(sheetName)
            workflow.send_feedback()
            return None
        else:
            searchTerm = ' '.join(query_tokens[search_term_index:])
            workflow.logger.debug(f"extract search term '{searchTerm}' from query '{query}'")

    options.searchInSheetByKeyword(sheetName, searchTerm)
    workflow.send_feedback()
    return None


if __name__ == "__main__":
    workflow = Workflow()
    sys.exit(workflow.run(main))
