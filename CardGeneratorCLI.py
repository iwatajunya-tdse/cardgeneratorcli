import os
import sys
from CardElements import *

def main(argv):
    dirname = os.path.dirname(__file__)
    fp = os.path.join(dirname, "input.csv")
    title = sys.argv[1]
    description = sys.argv[2]
    if len(sys.argv) == 4:
        encoding = sys.argv[3]
    else:
        encoding = "utf-8"

    questions = pd.read_csv(fp, encoding = encoding)

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
    if len(sys.argv) == 3 or len(sys.argv) == 4:
        main(sys.argv[1:])
    else:
        print("Card Generator\nUsage: python CardGeneratorCLI.py [title] [description] [encoding (optional)]")

