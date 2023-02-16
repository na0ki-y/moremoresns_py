import MeCab
def wakatigai_return_meisi(text):
    mecabTagger = MeCab.Tagger()
    noun_count = {}
    node = mecabTagger.parseToNode(text)
    while node:
        word = node.surface
        hinshi = node.feature.split(",")[0]
        if word in noun_count.keys() and hinshi == "名詞":
            noun_freq = noun_count[word]
            noun_count[word] = noun_freq + 1
        elif hinshi == "名詞":
            noun_count[word] = 1
        else:
            pass
        node = node.next
        
    noun_count = sorted(noun_count.items(), key=lambda x:x[1], reverse=True)
    return noun_count

if __name__=="__main__":
    wakatigai("ご飯を食べたよ")