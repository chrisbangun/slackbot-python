#!/usr/bin/env python
#ACB

import argparse
import sys
import os
import re
import subprocess

currentDir = 0

workingDirs = ["/home/ubuntu/analytics/repository/data-migrations/"]

commandTypes = ['sh','python','mongo <','mongo']

mongoMethods = ['--eval','--port','--host','--shell','--version']

firstInstructions=['dir','ls','mongo']

secondInstructions=['ls','mongo','run']



def runCommand(command):
  process = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  (out,err) = process.communicate()
  #print process.returncode
  return out
 
def constructor():
  listDir = set()
  setOfFiles = set()
  #cmd = 'ssh mongoscript03' + " 'ls -p "+workingDirs[currentDir]+"'"
  cmd = "ls -p "+workingDirs[currentDir]
  try:
    commandResult = runCommand(cmd)
    resultPerLine = commandResult.splitlines()
    for line in resultPerLine:
      if str(line).endswith('/'):
        listDir.add(str(line))
      else:
        setOfFiles.add(str(line))
  except:
    print "Could not run ", cmd
  return listDir,setOfFiles

# to validate if the given directory exist
def validateDir(givenDir,listDir,setOfFiles):
  global currentDir
  givenDir = givenDir.strip()
  splitDirs = givenDir.split('/')
  for _dir in splitDirs:
    if _dir:
      if _dir in listDir or _dir+"/" in listDir:
        currentDir = currentDir + 1
        workingDirs.append(workingDirs[currentDir-1] + _dir+'/')
        #print workingDirs[currentDir]
        listDir, setOfFiles = constructor()
      else:
        #listDir, setOfFiles = constructor()
        return None,[]
  print "============= ",givenDir, "=============="
  return listDir,setOfFiles

# to check if the given file exist
def doesFileExist(givenFile,setOfFiles):
  return givenFile in setOfFiles or givenFile+"*" in setOfFiles

def concatArgument(startIndex):
  argument=''
  argForMongo = False
  withFile = False
  for index in range(startIndex,len(sys.argv)):
    #print "argument: ", sys.argv[index]
    if sys.argv[index] in mongoMethods and argForMongo == False:
      argForMongo = True
      argument = argument + sys.argv[index]+ ' "'
    else:
      if ".js" in sys.argv[index]:
        withFile = True
        argument = argument.strip()+'" '+sys.argv[index]
      else:
        argument = argument + sys.argv[index]+" "
 
  if argForMongo and not withFile:
    print "masuk ga sini"
    argument = argument.strip()
    argument = argument+'"'
  #print "concat argument: ", argument
  return argument.strip()

def executeCommand(fileToRun,commandId,isFile,startIndex):
  argument = concatArgument(startIndex)
  #print argument
  if isFile:
    #command = 'ssh mongoscript03'+" ' "+commandTypes[commandId]+" "+workingDirs[currentDir]+fileToRun+" "+argument+"'"
    command =commandTypes[commandId]+" "+workingDirs[currentDir]+fileToRun+" "+argument
  else:
    #command = 'ssh mongoscript03'+ " ' "+commandTypes[commandId]+" "+argument+"'"
    command = commandTypes[commandId]+" "+argument  
  #print command
  commandResult = runCommand(command)
  print commandResult

def validateRunCommand(instruction,setOfFiles):
  fileToRun = instruction.split('=')[1]
  if doesFileExist(fileToRun,setOfFiles):
    fileToRuns = fileToRun.split('.')
    fileExtention = fileToRuns[len(fileToRuns)-1]
    #print fileExtention
    if fileExtention.startswith("sh"):
      executeCommand(fileToRun,0,True,3)
    elif fileExtention.startswith("py"):
      executeCommand(fileToRun,1,True,3)
    elif fileExtention.startswith("js"):
      executeCommand(fileToRun,2,True,3)
  elif fileToRun == "mongo":
    executeCommand(fileToRun,3,False,3);
  else:
    print fileToRun, "does not exist in ",workingDirs[currentDir]


def runLS(listDir,setOfFiles):
  for dir in listDir:
    print dir
  for file in setOfFiles:
    print file

def completeInstruction(firstInstruction,secondInstruction,listDir,setOfFiles):
  if firstInstruction == "dir":
    givenDir='home'
    try:
      givenDir = sys.argv[1].split('=')[1]
    except:
      print "no dir is given"
    if givenDir != 'home':
      listDir,setOfFiles = validateDir(givenDir,listDir,setOfFiles)
    if listDir is not None:
      if secondInstruction == "ls":
        runLS(listDir,setOfFiles)
      elif secondInstruction == "run":
        validateRunCommand(sys.argv[2],setOfFiles)
      else:
        executeCommand("mongo",2,False,3)
    else:
      print givenDir, "does not exist"
  else:
    print "type --help for help"

def leftInstruction(firstInstruction,listDir,setOfFiles):
  if firstInstruction == "ls":
    runLS(listDir,setOfFiles)
  elif firstInstruction == "mongo":
    executeCommand("mongo",3,False,2)
  else:
    print "unrecognized command"

def init():
   listDir,setOfFiles = constructor()
   numberOfArguments = len (sys.argv)
  
   if numberOfArguments > 1:
     firstInstruction = sys.argv[1]
     if len(sys.argv[1].split('=')) > 1:
       firstInstruction = sys.argv[1].split('=')[0]
     secondInstruction = "#"
     
     try:
       secondInstruction = sys.argv[2]
       if len(secondInstruction.split('=')) > 1:
         secondInstruction = secondInstruction.split('=')[0]
     except:
       secondInstruction = "#"

     if firstInstruction in firstInstructions and secondInstruction in secondInstructions:
        completeInstruction(firstInstruction,secondInstruction,listDir,setOfFiles)
     elif firstInstruction in firstInstructions:
       leftInstruction(firstInstruction,listDir,setOfFiles)
     else:
       print "type --help for help"
   else:
     print "type --help for help"
init()

