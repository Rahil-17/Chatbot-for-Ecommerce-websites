from nltk.stem import WordNetLemmatizer
#from autocorrect import spell
print("==========downloading nltk wordnet==============")
downloading nltk wordnet
print("================================================")
wordnet_lemmatizer = WordNetLemmatizer()

stopwords = [ "a", "about", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at",
              "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do",
              "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having",
              "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how",
              "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself",
              "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought",
              "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should",
              "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then",
              "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through",
              "to", "too", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what",
              "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's",
              "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves" ]
name_entity_map = {}
unigramDict = {}
synonyms_map = {}
path = "./train.txt"
path1 = "./vocab.txt"
path2 = "./synonyms.txt"

def training():
    file = open(path,'rt')

    for lines in file:
        name_entity_list = lines.split('\t')
        name_entity_list[1] = name_entity_list[1].strip('\n')
        name = name_entity_list[0].split(" ")

        for word in name:
            name_entity_map[word] = name_entity_list[1]

    file1 = open(path1, 'rt')

    for lines in file1:
        words = lines.split(" ")

        for word in words:
            word = word.lower()
            word = word.strip("\n")
            unigramDict[word]=1

    file2 = open(path2,'rt')

    for lines in file2:

    	synonyms = lines.split('\t')
    	synonyms[1] = synonyms[1].strip('\n')
    	name = synonyms[0].split(" ")

    	for word in name:
    		synonyms_map[word] = synonyms[1]
    	# print(synonyms)

    # print(len(synonyms_map))
    # for k,v in unigramDict.items():
    #     print(k,"--",v)

def preprocess_query(query):
    query = query.lower()
    query = query.split()

    processed_query = []
    for word in query:
        #word = spellCheck(word)
        processed_query.append(wordnet_lemmatizer.lemmatize(word))
        #processed_query.append(word)
    return processed_query


def spellCheck(word):
    word = word.lower()
    return (set(edit_distance(word)) & set(unigramDict.keys()))


def edit_distance(word):
    alphabet = set('abcdefghijklmnopqrstuvwxyz')

    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts = [a + c + b for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

#input => Camera of xiaomi redmi note 4s pro
#output => [['camera', 'attribute'], ['xiaomi', 'data'], ['redmi note 4 pro', 'model']]

def get_ner(query):
    temp = []
    result = []

    # training()
    query = preprocess_query(query)

    for word in query:
        tag = name_entity_map.get(word,"NA")
        temp.append([word,tag])

    composite_tag = temp[0][0]
    pre_tag = temp[0][1]

    for i in range(1,len(temp)):
        if temp[i][1] == pre_tag:
            composite_tag += " " + temp[i][0]
        else:
            result.append([composite_tag,pre_tag])
            composite_tag = temp[i][0]

        pre_tag = temp[i][1]

    if composite_tag!="":
        result.append([composite_tag,pre_tag])

    length = len(result)
    i=0
    while i < length:
        if result[i][0] in stopwords:
            del result[i]
        length = len(result)
        i+=1

    return result

def process_NL(q5):
	training()
	q5 = q5.split(" ")
	for n,words in enumerate(q5):

		if words not in stopwords:
			print(words.lower(),spellCheck(words.lower()))
			temp = spellCheck(words.lower())
			if len(temp) > 0 and words.lower() not in temp:
				q5[n] = list(temp)[0]
		else:
			q5[n] = ""
	# print("query : ", q5)
	s = ' '.join(q5)
	print("\n",s)
	result = get_ner(s)
	print("\n",result)
	print("\n")

	extra_info = []
	for r in result:
		if (r[1] == 'data' or r[1] == 'NA') and r[0] in synonyms_map.keys():
			t = []
			t.append(synonyms_map[r[0]])
			if synonyms_map[r[0]] == "mobile":
				t.append('table')
			else:
				t.append('attribute')
			extra_info.append(t)
	if len(extra_info) > 0 and extra_info not in result:
		result.extend(extra_info)
	print("Modified : ", result,"\n----------------\n")    
	return result

def main():
    # q1 = "Camera of xiaomi redmi note 4s pro snapdargon samsing"
    # q2 = "All phones of xiaomi"
    # q3 = "phones with snapdragon processor"
    # q4 = "compare iphone x and redmi 4 screen"
    # q5 = "which all phones have snapdragon"

	ques = ["Camera of xiaomi redmi note 4s pro snapdargon samsing","All phones of xiaomi","phones with snapdragon processor","compare iphone x and redmi 4 screen","which all phones have snapdragon","phones with 128gb space and snapdragon","android phones under 10000"]
    # print("\n")
    # result = get_ner(q1)
    # print(q1)
    # print(result)
    # print("\n")
    #
    # result = get_ner(q2)
    # print(q2)
    # print(result)
    # print("\n")
    #
    # result = get_ner(q3)
    # print(q3)
    # print(result)
    # print("\n")
    #
    # result = get_ner(q4)
    # print(q4)
    # print(result)
    # print("\n")
	

	for q5 in ques:
		print(q5)
		process_NL(q5)

		


if __name__ == "__main__":
    main()

