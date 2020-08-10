import common.logging as log
import search
import queue
import pprint
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image




def getTop100Keywords(site, query, max):
    keywordDict = {}
    site = site.lower()
    count = 0
    q = queue.Queue(max + 1000)
    q.put(query)
    while not q.empty():
        if count == max:
            break
        else:
            count += 1

        keyword = q.get()
        
        relatedKeywords = []
        if site == 'naver': 
            relatedKeywords = search.searchRelatedKeywordNaver(keyword)
        elif site == 'daum':
            relatedKeywords = search.searchRelatedKeywordDaum(keyword)
        elif site ==  'google':
            relatedKeywords = search.searchRelatedKeywordGoogle(keyword)
        
        log.info(keyword + ': ' + ','.join(relatedKeywords))

        for relatedKeyword in relatedKeywords:
            if relatedKeyword == query:
                continue
            elif relatedKeyword in keywordDict.keys():
                keywordDict[relatedKeyword] += 1
            else :
                keywordDict[relatedKeyword] = 1
                q.put(relatedKeyword)

    return keywordDict

query = '냉동만두'
site = 'naver'
log.info('START: ' + query)
res = getTop100Keywords(site, query, 100)
log.info('FINISH')
pprint.pprint(res, depth=2)

alice_mask = np.array(Image.open("./alice_mask.png"))

wordcloud = WordCloud(
    width = 800,
    height = 800,
    font_path='./NanumGothic.ttf',
    background_color="white",
    #mask = alice_mask
)
wordcloud = wordcloud.generate_from_frequencies(res)
plt.figure(figsize=(10, 10))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()