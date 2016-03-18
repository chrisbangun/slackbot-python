#ACB

from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
import os
import sys
import subprocess

PREV_DIR = "home"



def runCommand(command):
  process = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
  (out,err) = process.communicate()
  return out

def getArgument(param):
  arguments = ''
  for index in range(1,len(param)):
    arguments = arguments + param[index] + " "
  print arguments
  return str(arguments).strip()

@respond_to('git pull')
def git_pull(message):
  message.reply_webapi("*please wait*")
  command = "sh /home/ubuntu/analytics/repository/pull_datamigrations_schedule_15min.sh"
  try:
    commandResult = runCommand(command)
    message.reply_webapi("```%s```" %commandResult)
  except:
    message.reply_webapi("cannot execute command")

@respond_to('help',re.IGNORECASE)
def connectMongoscript03(message):
  message.reply_webapi("*welcome to production data access portal*")
  text = """
     You can access all data in mongoscript03:/analytics/repository/data-migrations/
     The following are some recognized commands:
     1. dir=[Directory] run=[executable file] [arg_1] [arg_2] ... [arg_n]
     2. dir=[Directory] ls
     3. mongo --eval/--port/--version [arg_1] [arg_2] ... [arg_n]
     4. dir=[home]/[subDir] ls/run=[executable file]
     5. git pull
   """
  message.reply_webapi("``` %s ```" % text)

@respond_to('mongo (.*)')
def mongoscriptMongo(message,param):
  message.reply_webapi("*please wait...*")
  command = "/home/ubuntu/mongobot/mongoscript03_command.py mongo "+param
  try:
    commandResult = runCommand(command)
    message.reply_webapi("```%s```" %commandResult)
  except:
    message.reply_webapi("*cannot create a connection to mongoscript03*")

@respond_to('dir=(.*) run=(.*)',re.IGNORECASE)
def mongoscript03Run(message,param1,param2):
  global PREV_DIR
  inputInParam2 = str(param2).split(' ')
  fileName = inputInParam2[0]
  arguments = getArgument(inputInParam2)
  Dirs = str(param1).split("/")
  if Dirs[0] == "prev" and len(Dirs) > 1:
    param1 = appendPrevDir(Dirs)
  elif param1 == "prev":
    param1 = PREV_DIR
  print param1
  print fileName
  command = "/home/ubuntu/mongobot/mongoscript03_command.py dir="+param1+" run="+fileName+" "+arguments
  print "argument: ",arguments
  message.reply_webapi("*Please wait*")
  try:
    commandResult = runCommand(command)
    message.reply_webapi("``` %s ```" % str(commandResult))
    PREV_DIR = param1
  except:
    message.reply_webapi("```cannot create a connection to mongoscript03 ```")

def appendPrevDir(Dirs):
  appendedDir = PREV_DIR
  for element in Dirs[1:]:
    appendedDir = appendedDir +"/"+element
  return appendedDir

@respond_to('dir=(.*) ls',re.IGNORECASE)
def mongoscript03LsInDir(message,directory):
  global PREV_DIR
  Dirs = str(directory).split("/")
  if Dirs[0] == "prev" and len(Dirs) > 1:
    directory = appendPrevDir(Dirs)
  elif directory == "prev":
    directory = PREV_DIR
  command = "/home/ubuntu/mongobot/mongoscript03_command.py dir="+directory+" ls"
  try:
    commandResult = runCommand(command)
    message.reply_webapi("``` %s ```" %str(commandResult))
    PREV_DIR = directory
  except:
    message.reply_webapi("``` cannot create a connection to mongoscript03 ```")
