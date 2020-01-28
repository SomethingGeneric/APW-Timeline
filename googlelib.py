import requests as req
from bs4 import BeautifulSoup as soup
import webbrowser as wbrs
import sys
from time import sleep
from random import randint


class gsearch:
    def __init__(self):
        self.base = "https://www.google.com/search?q="
        # &start=10
        # increment by 10

    def raw_result(self, query):
        # Get raw HTML
        r = req.get(self.base + query.replace(" ", "%20"))
        return r.text

    def extract_local(self, query, text):
        if sys.platform == "win32":
            raw = soup(text, "lxml")
        else:
            raw = soup(text, "html.parser")
        linktags = raw.findAll("a", href=True)

        goodlinks = []

        # Iterate thru all a tags
        for link in linktags:
            # Grab the URL from the tag
            linkurl = link['href']
            # If there's a http or https, keep going (b/c if true then links to page outside of google)
            if "http" in linkurl or "https" in linkurl:
                # ignore any google services link
                if "google" not in linkurl and "youtube" not in linkurl and "gstatic" not in linkurl and query not in linkurl:
                    # Yet another attempt at removing links w/ query in domain
                    if linkurl.find(query) == -1:
                        # Remove Google URL garbage from string
                        linkurl = linkurl.replace(
                            "/url?q=", "").replace("/search?ie=UTF-8&q=related:", "")
                        # Remove more Google garbage from string
                        list = linkurl.split("&")
                        niceurl = str(list[0])
                        # No duplicates in my linkurl
                        if niceurl not in goodlinks:
                            # Add final nice url to list
                            goodlinks.append(niceurl)
        return goodlinks

    def get_links(self, query):

        print("Searching for " + query)

        # Empty list to fill with goodlinks things
        goodlinks = []

        # Start w/ first 10 items, b/c 10 per search page
        page = 19

        while page != 20:
            # Grab raw HTML, start BS4
            # Different parser arg for Windows
            # fUcK

            r = req.get(self.base + query + "&page=" + str(page))
            for boi in self.extract_local(query, r.text):
                goodlinks.append(boi)

            #print("Page value: " + str(page)+"\r", end="")
            print()
            # Boop to next page
            page += 1
           # dly = randint(60, 90)
            #print("Sleeping for " + str(dly))
            #for s in range(dly):
            #    sleep(1)
            print()
        # Return list of pretty URLS
        return goodlinks


"""if __name__ == "__main__":
    g = gsearch()
    bois = g.get_links(input("Search: "))
    for link in bois:
        print(link)
        print()
    print(str(bois))
    print("END")
    """
