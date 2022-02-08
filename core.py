import requests
from bs4 import BeautifulSoup, builder
from datetime import date


def getUrl(word):
    return "https://sapere.virgilio.it/parole/sinonimi-e-contrari/"+word.strip()

def getSomeSynonymsOf(word, level, sinonimo):
    found = []
    # Let's get scraping
    r = requests.get(getUrl(word))
    content = r.content
    soup = BeautifulSoup(content, 'html.parser')
    box = soup.findAll('div', attrs = {'class':'sct-descr'})
    try:
        # TODO: divisione sinonimi e contrari dentro e fuori il "p"
        if sinonimo:
            box = soup.findAll('p')[1]
            # print(box.text)
            sinonimi = box.find_all("a" )
            for sin in sinonimi:
                found.append([sin.text, level, 0])
        else:
            try:
                if soup.findAll('p')[2].text == "Contrari":
                    print("Hey")
                    box = soup.findAll('p')[3]
                    contrari = box.find_all("a" )
                    for sin in contrari:
                        found.append([sin.text, level, 0])
            except:
                pass
    except:
        pass
    return found


def _getWords(words, word, level, limit, sinonimo):
    words.append([word, level, 1])
    if level < limit:
        syns = getSomeSynonymsOf(word, level+1, sinonimo)
        for s in syns:
            #print("Checking "+s[0])
            if not alreadyPresent(words, s):
                if not sinonimo:
                    sinonimo = True
                _getWords(words, s[0], level+1, limit, sinonimo)
    return words



def alreadyPresent(words, word):
    found = False
    for w in words:
        if w[0]==word[0]:
            found = True
            w[2] += 1
    return found

def getWords(words, word, level, limit, sinonimo):
    words = _getWords([], "ingegno", 0,3, True)
    sorter = lambda x: (x[1], -x[2])
    res = sorted(words, key=sorter)
    return res;

def main():
    words = getWords([], "ingegno", 0,3, True)
    for w in words:
        print(w)

if __name__ == "__main__":
    main()
