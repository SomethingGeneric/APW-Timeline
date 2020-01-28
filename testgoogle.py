from googlelib import gsearch
import requests
import re

regex = "\d{4}"

# match = re.findall(exp,string)

fn = input("Event list: ")
fo = input("Output file: ")

ostr = ""

with open(fn) as f:
    events = f.read().split('\n')

print("----------")
ymin = int(input("Min date guess: "))
ymax = int(input("Max date guess: "))
freq = int(input("Min occur. for result: "))
print("-----------")

for query in events:

    print("Event: " + query)
    ostr += "\n-----\n" + query + ": "

    r = requests.get("https://google.com/search?q=" + query.replace(" ", "%20"))

    matchs = re.findall(regex,r.text)
    if matchs is None or len(matchs) == 0:
        """
        g = gsearch()
        links = g.get_links(query)
        externals = []
        for link in links:
            if link[0] == "h":
                externals.append(link)
        for i in range(5):
            print(externals[i])
        """
        ostr += "No dates for this query"
        print("No dates")
            
    else:
        valid = []
        for match in matchs:
            t = int(match)
            if ymin <= t and t <= ymax:
                valid.append(match)
        if len(valid) > 0:
            counted = []
            for date in valid:
                if date not in counted:
                    occurs = valid.count(date)
                    if occurs >= freq:
                        print(date + " : " + str(occurs))
                        ostr += "\n" + date + " : " + str(occurs)
                        counted.append(date)
        else:
            ostr += "No dates in occur. threshold for this query"
            print("All dates are too infrequent")
    print("----------")
        
with open(fo,"w") as f:
    f.write(ostr)
