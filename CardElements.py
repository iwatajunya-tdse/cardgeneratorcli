import pandas as pd
import math
import json

class Card:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.items = []
    
    def addItem(self, item):
        self.items.append(item)
        
    def generate(self):
        """
        Generates a JSON code from the card properties
        """
        
        outerjson = json.loads('{"_plugin": {"type": "adaptivecards"}}')
        innerjson = json.loads('{"type": "AdaptiveCard","body": [], "$schema": "http://adaptivecards.io/schemas/adaptive-card.json","version": "1.0","actions": [{"type": "Action.Submit","title": "Send"}]}')
        
        titlejson = json.loads('{"type": "TextBlock","size": "Medium","weight": "Bolder","horizontalAlignment": "Center"}')
        titlejson['text'] = self.title
        descjson = json.loads('{"type": "TextBlock","wrap": "true", "size": "Small"}')
        descjson['text'] = self.description
        
        innerjson['body'].append(titlejson)
        innerjson['body'].append(descjson)
        
        for item in self.items:
            itemjson = json.loads('{"type": "Container","items": []}')
            
            questionjson = json.loads('{"type": "TextBlock", "wrap": "true"}')
            questionjson['text'] = item.question
            itemjson['items'].append(questionjson)
            
            responsejson = {}
            
            if item.itemType() == "choice":
                responsejson['type'] = "Input.ChoiceSet"
                if item.parameters['multiSelection'] == True:
                    responsejson['isMultiSelect'] = "true"
                if item.parameters['compact'] == False:
                    responsejson['style'] = "expanded"
                responsejson['choices'] = []
                
                for choice in item.choices:
                    choicejson = {}
                    choicejson['title'] = choice.title
                    choicejson['value'] = choice.value
                    responsejson['choices'].append(choicejson)
                
            else:
                responsejson['type'] = "Input.Text"
            
            responsejson['id'] = item.inputId
            if item.parameters['default'] == item.parameters['default']:
                responsejson['value'] = item.parameters['default']
            if item.parameters['placeholder'] == item.parameters['placeholder']:
                responsejson['placeholder'] = item.parameters['placeholder']
            
            itemjson['items'].append(responsejson)
            innerjson['body'].append(itemjson)
        
        outerjson["payload"] = innerjson
        
        return outerjson

class Item:
    """
    A pair of question and input
    """
    def __init__(self, qType, question, 
                 inputId, multiSelection = False, compact = False, 
                 default = None, placeholder = None):
        self.qType = qType.lower()
        self.question = question
        self.inputId = inputId
        self.parameters = {
            "multiSelection": multiSelection,
            "compact": compact,
            "default": default,
            "placeholder": placeholder
        }
        self.choices = []
        
    def itemType(self):
        return self.qType
        
    def addChoice(self, choice):
        if self.qType == "choice":
            self.choices.append(choice)

class Choice:
    def __init__(self, title, value):
        self.title = title
        self.value = value
