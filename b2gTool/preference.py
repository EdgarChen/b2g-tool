#!/usr/bin/env python
# vim:fileencoding=utf-8:noet

import re
import ast
import json

class Preference(object):
  __slots__ = ("__key", "__value", "__type")

  def __init__(self, type=None, key=None, value=None):
    if type not in (None, "pref", "user_pref"):
      raise Exception("'type' should be 'pref' or 'user_pref'")

    self.__type = type
    self.__key = key
    self.__value = value  

  def __str__(self):
    value = self.__value
    if isinstance(value, str):
      value = "\"%s\"" % (value)
    else:
      value = str(value).lower()

    return "%s(\"%s\", %s);" % (self.__type, self.__key, value)

  def parse(self, string):
    match_pre = re.compile(r"^pref\(\s*[\'\"](.*)[\'\"]\s*,\s*(.*)\s*\);\s*$")
    match_user_pre = re.compile(r"^user_pref\(\s*[\'\"](.*)[\'\"]\s*,\s*(.*)\s*\);\s*$")

    # Parse preference setting
    m = match_pre.match(string)
    if m != None and m.lastindex == 2:
      self.__type = "pref"
    else:
      m = match_user_pre.match(string)
      if m != None and m.lastindex == 2:
        self.__type = "user_pref"
      else:
        Exception("Invalid format: " + string)

    self.__key,value = m.groups()

    # Try to parse value by literal_eval() first
    try:
      self.__value = ast.literal_eval(value)
      return
    except ValueError:
      pass

    # Try to parse value by json.load()
    try:
      self.__value = json.loads(value)
    except:
      raise Exception("Invalid format: " + string)

  def getType(self):
    return self.__type

  def getKey(self):
    return self.__key

  def getValue(self):
    return self.__value

  def setValue(self, value):
    self.__value = value

class PreferenceManager(object):
  __slots__ = ("__dictionary", "__sequence")

  def __init__(self):
    self.__dictionary = {}
    self.__sequence = []

  def add(self, preference):
    key = preference.getKey()
    if key in self.__dictionary.keys():
      raise Exception("Key '" + key + "' is already exist")

    self.__dictionary[key] = preference
    self.__sequence.append(preference)

  # Load preference setting from file
  def load(self, fileName):
    if fileName == None:
      raise Exception("Invalid file name")

    match_ws = re.compile(r"\s*$")
    match_comment = re.compile(r"\s*#(.*)$")
    match_comment_start = re.compile(r"\s*\/\*(.*)$")
    match_comment_end = re.compile(r"(.*)\*\/\s*$")
    in_multi_line_comment = False
    dictionay = {}
    sequance = []

    f = open(fileName, "r")
    for line in f:
      # Skip multi-line comment
      if in_multi_line_comment:
        m = match_comment_end.match(line)
        if m != None:
          in_multi_line_comment = False
        continue
      else:
        m = match_comment_start.match(line)
        if m != None:
          in_multi_line_comment = True
          continue

      # Skip single line comment 
      m = match_comment.match(line)
      if m != None:
        continue

      # Skip empty line
      m = match_ws.match(line)
      if m != None:
        continue

      pref = Preference()
      pref.parse(line)
      self.add(pref)

  def update(self, key, value):
    try:
      pref = self.__dictionary[key]
      pref.setValue(value)
    except KeyError:
      raise Exception("Key '" + key + "' is not exist")

  def dump(self, fileName):
    f = open(fileName, "w")
    for pref in self.__sequence:
      f.write(str(pref) + "\n")
