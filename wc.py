#!/usr/bin/env python
#Filename: wc.py
#Makes a word count for the previous day.
#First version. Written by Thomas Riggs and released into the public domain. www.twostopsdown.com

import os, sys # to work with paths and files.
from datetime import date, timedelta # to work with dates.
import pickle # to save objects.

# Configuration
default_threshold = timedelta(days=1) # The default threshold for what is considered recent, as a timedelta.
default_path = os.path.expanduser('~/Writing') # Default path to search.

# Functions
def findRecentFiles(path = default_path, threshold = default_threshold):
     "This function recurses through a folder, and returns a list of files modified within the threshold value."
     cutoff = date.today() - threshold
     if path == None or threshold == None:
          print("findRecentFiles requires a path and threshold.")
          return void
          
     recentfiles = []
     
     for file in os.listdir(path):
          if file[0] == ".":
               continue
          
          filepath = path + "/" + file
          if date.fromtimestamp(os.path.getmtime(filepath)) > cutoff and os.path.isfile(filepath) == True and file[-3:] == 'txt':
               recentfiles.append(filepath)
          elif os.path.isdir(filepath) == True:
               for item in findRecentFiles(filepath):
                    recentfiles.append(item)
     
     return recentfiles

def countWords(files = []):
     "This function returns a dictionary of files and their current word count."
     if files == None:
          print("countWords requires a list of file paths.")
          return void
     
     wordcounts = {}
     
     for file in files:
          words = []
          data = open(file)
          lines = data.readlines()
          for line in lines:
                 for word in line.split(None):
                      words.append(word)
                      
          wordcounts[file] = len(words)
          
     return wordcounts

def writeWordCounts(wordcounts = {}, path = default_path):
     "Writes the given wordcounts object using Pickle."
     wordcountfile = path + "/" + ".wordcount"
     data = open(wordcountfile, 'wb')
     pickle.dump(wordcounts, data)
     data.close()

def loadWordCounts(path = default_path):
     "Uses Pickle to open a path's wordcount object."
     wordcountfile = path + "/" + ".wordcount"
     try:
          data = open(wordcountfile, 'rb')
          wordcounts = pickle.load(data)
          return wordcounts
          data.close()
     except IOError:
          print("No .wordcount file. You need to run 'wc.py init'")
          sys.exit()

def updateWordCounts(old = {}, new = {}):
     "Combines an old set of word counts with a current one. Replaces existing file's data and keeps unupdated ones."
     updated = old
     updated.update(new)
     writeWordCounts(updated)

def relativePath(path, root = default_path):
     "Gives the given file path, minus a starting root, by counting the directory tree branches of the root. Assumes path is within root."
     rootlength = len(root.split("/"))
     relativepathparts = path.split("/")
     relativepath = "/".join(relativepathparts[rootlength:])
     return relativepath

def currentWordCounts(path = default_path):
     "Chains together findRecentFiles and countWords into a single function."
     return countWords(findRecentFiles(path))

def recentChanges(raw = False, path = default_path):
     "This function takes a path and finds recent word counts for files, using currentWordCounts."
     currentwordcount = currentWordCounts(path)
     oldwordcount = loadWordCounts()
     
     filecount = 0
     totalwordcount = 0
     
     for (file, count) in currentwordcount.items():
          try:
               newwords = count - oldwordcount[file]
               if newwords <= 0:
                    continue
               status = str(newwords) + " new words."
               totalwordcount = totalwordcount + newwords
          except KeyError:
               status = str(count) + " words in total, but no previous record."
               totalwordcount = totalwordcount + count
               
          if raw == False:
               print(relativePath(file), "has", status)
               
          filecount = filecount + 1
          
     if raw == True:
          print(totalwordcount)
          return 
     
     if filecount == 0 or totalwordcount == 0:
          print("No updates today!")
     else:
          print("In total,", str(totalwordcount), "words have been written today!")

# On with the show!

try:
     arg = sys.argv[1]
except IndexError:
     recentChanges()
     sys.exit()

if arg == "update":
     updateWordCounts(loadWordCounts(), currentWordCounts())
elif arg == "raw":
     recentChanges(True)
elif arg == "init":
     updateWordCounts(currentWordCounts(), currentWordCounts())
elif arg == "help":
     print('''WC.PY
A Python script for daily word counts.
Usage:
     wc.py          Show the current word count;
     wc.py update   Update the recorded word count;
     wc.py init     Create the .wordcount data file;
     wc.py help     This screen.

(C) Thomas Riggs 2011, Creative Commons Att-NC''')
