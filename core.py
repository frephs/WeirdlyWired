import requests
from bs4 import BeautifulSoup, builder
from datetime import date

def getUrl(word):
    "Returns that is to be scraped"
    return "https://sapere.virgilio.it/parole/sinonimi-e-contrari/"+word.strip()

def getSomeSynonymsOf(word, level, synonym):
    "Scrapes synonyms or contraries of a given word"
    found = []
    word = word.capitalize()
    # Let's get scraping
    r = requests.get(getUrl(word))
    content = r.content
    soup = BeautifulSoup(content, 'html.parser')
    box = soup.findAll('div', attrs = {'class':'sct-descr'})
    try:
        if synonym:
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
    "Checks if (word, level, reps) is already present in the set of words"
    found = False
    for w in words:
        #print("Checking: "+ w[0].capitalize() + word[0].capitalize() )
        if w[0].capitalize() == word[0].capitalize() :
            found = True
            w[2] += 1
    return found

def _getWords(words, word, level, maxRecursion, synonym):
    """ 
        Recursively looks for more words 
        (synonms if synonym==true otherwise contraries ), 
        Stops when the maxRecursion is reached.
    """
    if not alreadyPresent(words, [word, level, 1]):
        words.append([word.capitalize(), level, 1])        
    if level < maxRecursion:
        syns = getSomeSynonymsOf(word, level+1, synonym)
        for s in syns:
            if not alreadyPresent(words, s):
                if not synonym:
                    synonym = True
                _getWords(words, s[0], level+1, maxRecursion, synonym) 
    return words

def getWords(words, word, level, maxRecursion, synonym):
    "Get synonyms or contraries sorts them and returns them"
    words = _getWords(words, word, level, maxRecursion, synonym)
    sorter = lambda x: (x[1], -x[2])
    res = sorted(words, key=sorter)
    return res;

def intersect(words_a, words_list):
    """
    Intersects a set of words with a list of others sets, 
    if a word is present in all the sets, its added
    """
    intersection = []
    for a in words_a:
        for words_b in words_list:
            found = alreadyPresent(words_b, a);
            if not found:
                break; # I HATE PYTHON SO MUCH
        if found:
            intersection.append(a[0].capitalize())
    return intersection

def findIntersection(str, precision, maxRecursion):
    """
        Given a list of words separated by commas finds a list of synonyms recursively
        Intersects the sets and continues until the minimum number of words (precision) is met
        or maxRecursion is reached
    """
    words = str.split(", "); n_words = len(words);
    words_list = []; intersection = [];
    for w in words:
        words_list.append([[w, 0, 1]]);
    iterations = 1
    while ((not intersection) or ( len(intersection) < precision)) and (iterations<=maxRecursion):
        for i in range(0, n_words):
            for w in words_list[i]:
                words_list[i] = _getWords(words_list[i], w[0], w[1]+1, iterations, True)
        a = words_list[0]
        b = [words_list[i] for i in range(0,n_words) if i] # all sets of words except the first one
        intersection = intersect(a,b)
        iterations+=1
    return intersection

def main():
    print(findIntersection("Metro, quadro", 5, 6))

if __name__ == "__main__":
    main()
