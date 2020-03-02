import os
import sys
import pandas as pd
import math
import json

# Declare classes
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
            if not math.isnan(item.parameters['default']):
                responsejson['value'] = item.parameters['default']
            if not math.isnan(item.parameters['placeholder']):
                item.responsejson['placeholder'] = item.parameters['placeholder']
            
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


def main(argv):
    dirname = os.path.dirname(__file__)
    fp = os.path.join(dirname, "input.csv")
    title = sys.argv[1]
    description = sys.argv[2]

    questions = pd.read_csv(fp, encoding = "utf-8") # change to ANSI if necessary

    card = Card(title, description)

    for i in range(len(questions)):
        entry = questions.iloc[i]
        item = Item(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6])
        if item.itemType() == "choice":
            j = 7
            while entry[j] == entry[j]: # entry[j] is neither None nor NaN
                choice = Choice(entry[j], entry[j + 1])
                item.addChoice(choice)
                j += 2
        card.addItem(item)

    outer = card.generate()
    output = json.dumps(outer, ensure_ascii = False)
    
    with open("output.json", "w") as f:
        f.write(output)


if __name__ == "__main__":
    main(sys.argv[1:])


