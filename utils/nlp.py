#!/usr/bin/env python

"""
Parse human-readable request including date or location
"""

import utils.parsedatetime as pdt
import utils.parsedatetime_consts as pdc
from utils import transform
from time import mktime
from datetime import date
from item.models import ItemCommand


class Parser(object):
    def __init__(self):
        c = pdc.Constants()
        c.BirthdayEpoch = 12
        self.parser = pdt.Calendar(c)

    def parse(self, text_input):
        chunks = text_input.split(' ')
        name = chunks[0]
        date_struct = self.parser.parse(chunks[1])
        return_date = date.fromtimestamp(mktime(date_struct[0]))
        return name, return_date

    def parse_command(self, command_input):
        chunks = command_input.lower().split(' ')
        command = ItemCommand()
        result = {"what": []}
        when = transform.tree()
        current = ""
        for index, chunk in enumerate(chunks):
            if chunk == "with":
                current = "who"
                result[current] = []
            elif chunk == "at":
                current = when["date"]
                result[current] = []
            elif chunk == "on":
                current = when["time"]
                result[current] = []
            elif len(current):
                result[current].append(chunk)
            else:
                result["what"].append(chunk)
        for key in result:
            setattr(command, key, ' '.join(result[key]))

        return command
