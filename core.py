import requests
from bs4 import BeautifulSoup, builder
from datetime import date

def getUrl(word):
    return "https://sapere.virgilio.it/parole/sinonimi-e-contrari/"+word.strip()

def getSomeSynonymsOf(word, level, sinonimo):
    found = []
    word = word.capitalize()
    # Let's get scraping
    r = requests.get(getUrl(word))
    content = r.content
    soup = BeautifulSoup(content, 'html.parser')
    box = soup.findAll('div', attrs = {'class':'sct-descr'})
    try:
        if sinonimo:
            box = soup.findAll('p')[1]
            # print(box.text)
            sinonimi = box.find_all("a" )
            for sin in sinonimi:
                found.append([sin.text.capitalize(), level, 0])
        else:
            try:
                box = soup.findAll('p')[3]
                contrari = box.find_all("a" )
                for sin in contrari:
                    found.append([sin.text.capitalize(), level, 0])
            except:
                pass
    except:
        pass
    return found

def alreadyPresent(words, word):
    found = False
    for w in words:
        #print("Checking: "+ w[0].capitalize() + word[0].capitalize() )
        if w[0].capitalize() == word[0].capitalize() :
            found = True
            w[2] += 1
    return found

def _getWords(words, word, level, limit, sinonimo):
    words.append([word, level, 1])
    if level < limit:
        syns = getSomeSynonymsOf(word, level+1, sinonimo)
        for s in syns:
            if not alreadyPresent(words, s):
                if not sinonimo:
                    sinonimo = True
                _getWords(words, s[0], level+1, limit, sinonimo) 
    return words

def getWords(words, word, level, limit, sinonimo):
    words = _getWords(words, word, level, limit, sinonimo)
    sorter = lambda x: (x[1], -x[2])
    res = sorted(words, key=sorter)
    return res;

def intersect(words_a, words_list):
    intersection = []
    for a in words_a:
        found = True
        # print(words_list)
        for words_b in words_list:
            #print(words_b)
            found = alreadyPresent(words_b, a);
            if not found:
                #print("Did not find" + a[0]+ " in")
                # print(words_b)
                break;
        if found:
            intersection.append(a[0])
            # print(a[0])
    return intersection

def findIntersection(str, precision):
    words = str.split(", ");
    #print(words)
    n_words = len(words)
    words_list = []
    intersection = []
    for w in words:
        words_list.append([]);
    while (not intersection) and ( len(intersection) < precision) :
        for i in range(0, n_words):
            words_list[i] = getWords(words_list[i], words[i], 0, 1, True)
        a = words_list[0]
        b = [words_list[i] for i in range(0,n_words) if i]
        # print(words_list)
        #print("\n\n"); print(a)
        intersection = intersect(a,b)
    return intersection

def main():
    print(findIntersection("Pigro, fannullone, scansafatiche", 2))

if __name__ == "__main__":
    main()
