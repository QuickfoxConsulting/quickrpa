*** Settings ***
Documentation     Template robot main suite.
Library           Collections
Library           EntryPoint.py
Library           BotLogger.py
Resource          keywords.robot
Variables         MyVariables.py

*** Tasks ***
Example Task
    Main
