#Usage: python qGen.py <numberOfSynonymsPerWord> (<t>) (<d>) (<n>)
#Example for augmented titles only w/ 5 synonyms: python qGen.py 5 t
#Ex. for augmented titles and desc: python qGen.py 5 t d

import string
import sys
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize

indexPath = "/home/neo/Downloads/IR-2019-2020-Project-1/indices/example";
paths = ['topics.301-350.trec6', 'topics.351-400.trec7', 'topics.401-450.trec8'];

def synonym(word,count): #Returns <count> number of synonyms for the word(list of strings)
	synonyms = []
	for syn in wordnet.synsets(word):
	    for lemma in syn.lemmas():
		synonyms.append(lemma.name())
	if len(synonyms)<int(count): #if less synonyms than required fill with original word
		for i in range(0,(int(count)-len(synonyms))):
			synonyms.append(word)
		return synonyms
	else:
		return synonyms[:int(count)]

def synonymSentences(eachWord, count): # Returns sentences of different synonyms(as single string)
	synonymsPerWord = []
	sentences = []
	sentence = ""
	final = ""
	for wordsInSentence in range(len(eachWord)): 
		synonymsPerWord.append(synonym(eachWord[wordsInSentence],count))
	for counter in range(count): 
		for wordCounter in range(len(eachWord)):		
			sentence = sentence + " " + synonymsPerWord[wordCounter][counter]
		sentences.append(sentence)
		sentence = ""
	final = " ".join(sentences)
	final = " ".join(eachWord)+" "+final
	return final

def sentences(tokens,count): #Deprecated
	sents = [""] * int(count)
	for i in range(0,len(tokens)):
		for j in range(0,int(count)):
			tempw = synonym(tokens[i],count)[j]
			tempw = " ".join([sents[j],tempw])
			sents[j] = tempw
	return(" ".join(sents))
	

def multisyn(tokens, count): # Returns <count> number of synonyms of each word w/out aranging as sentence
	aug = []
	for word in tokens:
		synonyms = []
		for syn in wordnet.synsets(word):
	   		 for lemma in syn.lemmas():
				synonyms.append(lemma.name())
		aug.append("{"+" ".join(synonyms)+"}")
	return " ".join(aug)

aug_count = int(sys.argv[1])
print("Number of synonyms: "+str(aug_count))

titles = []
descs = []
narrs = []
for path in paths:
    print("Processing "+path+" ...");
    f = open(path,'r')
    contents = f.read()
    f.close()
    contents = contents.replace('-',' '); 
    contents = contents.replace('\n',' '); 
    contents = contents.replace("&"," and ")
    #contents = contents.replace("'s","")
    while True:
        title_pos = contents.find('<title>')
        if (title_pos == -1):
            break;
        desc_pos = contents.find('<desc>')
	temp = contents[title_pos+8:desc_pos]
	temp = temp.replace('/',' ')
	temp = temp.translate(None,string.punctuation)
	titles.append(temp)
        
        narr_pos = contents.find('<narr>');
	temp = contents[desc_pos+18:narr_pos];
	temp = temp.replace('/',' ')
        descs.append(temp.translate(None,string.punctuation));

        top_pos = contents.find('</top>');
	temp = contents[narr_pos+15:top_pos];
	temp = temp.replace('/',' ')
        narrs.append(temp.translate(None,string.punctuation));
        contents = contents[top_pos+6:];
    
#Augmented Titles
if len(sys.argv)>2:
	if sys.argv[2]=='t':
		aug_titles = []
		print("writing augmented title queries ...");
		f = open("title_aug^"+str(aug_count)+".queries", "w")
		f.write("<parameters>\n<index>"+indexPath+"</index>\n<rule>method:dirichlet,mu:1000</rule>\n<count>1000</count>\n<trecFormat>true</trecFormat>\n");
		f.close();

		f = open("title_aug^"+str(aug_count)+".queries", "a")
		i = 300;
		for title in titles:
			titleTokens = word_tokenize(title)
			#augmented_title = multisyn(titleTokens,aug_count)
			augmented_title = synonymSentences(titleTokens,aug_count)
			augmented_title = augmented_title.replace('_',' ')
			aug_titles.append(augmented_title)
			i = i + 1;
			f.write("<query> <type>indri</type> <number>"+str(i)+"</number> <text>");
			f.write(augmented_title);
			f.write("</text> </query>\n");
		f.write("</parameters>");
		f.close();

#Augmented Descriptions
if len(sys.argv)>3:
	if sys.argv[3]=='d':
		aug_descs = []
		print("writing augmented description queries ...");
		f = open("title+desc_aug^"+str(aug_count)+".queries", "w")
		f.write("<parameters>\n<index>"+indexPath+"</index>\n<rule>method:dirichlet,mu:1000</rule>\n<count>1000</count>\n<trecFormat>true</trecFormat>\n");
		f.close();

		f = open("title+desc_aug^"+str(aug_count)+".queries", "a")
		i = 300;
		for j in range(0,len(titles)):
			descTokens = word_tokenize(descs[j])
			augmented_desc = synonymSentences(descTokens,aug_count)
			augmented_desc = augmented_desc.replace('_',' ')
			aug_descs.append(augmented_desc)
			i = i + 1;
			f.write("<query> <type>indri</type> <number>"+str(i)+"</number> <text>");
			f.write(aug_titles[j]+" ");
			f.write(augmented_desc);
			f.write("</text> </query>\n");
		f.write("</parameters>");
		f.close();

#Augmented Narratives
if len(sys.argv)>4:
	if sys.argv[4]=='n':
		aug_narrs = []
		print("writing augmented narrative queries ...");
		f = open("title+desc+narr_aug^"+str(aug_count)+".queries", "w")
		f.write("<parameters>\n<index>"+indexPath+"</index>\n<rule>method:dirichlet,mu:1000</rule>\n<count>1000</count>\n<trecFormat>true</trecFormat>\n");
		f.close();

		f = open("title+desc+narr_aug^"+str(aug_count)+".queries", "a")
		i = 300;
		for j in range(0,len(titles)):
			narrTokens = word_tokenize(narrs[j])
			augmented_narr = synonymSentences(narrTokens,aug_count)
			augmented_narr = augmented_narr.replace('_',' ')
			aug_narrs.append(augmented_narr)
			i = i + 1;
			f.write("<query> <type>indri</type> <number>"+str(i)+"</number> <text>");
			f.write(aug_titles[j]+" ");
			f.write(aug_descs[j]);
			f.write(augmented_narr);
			f.write("</text> </query>\n");
		f.write("</parameters>");
		f.close();

#Titles
print("writing title queries ...");
f = open("title.queries", "w")
f.write("<parameters>\n<index>"+indexPath+"</index>\n<rule>method:dirichlet,mu:1000</rule>\n<count>1000</count>\n<trecFormat>true</trecFormat>\n");
f.close();

f = open("title.queries", "a")
i = 300;
for title in titles:
    i = i + 1;
    f.write("<query> <type>indri</type> <number>"+str(i)+"</number> <text>");
    f.write(title[:-2]);
    f.write("</text> </query>\n");
f.write("</parameters>");
f.close();

#Description
print("writing title+description queries ...");
f = open("title+desc.queries", "w")
f.write("<parameters>\n<index>"+indexPath+"</index>\n<rule>method:dirichlet,mu:1000</rule>\n<count>1000</count>\n<trecFormat>true</trecFormat>\n");
f.close();

f = open("title+desc.queries", "a")
i = 300;
for j in range(0,len(titles)):
    i = i + 1;
    f.write("<query> <type>indri</type> <number>"+str(i)+"</number> <text>");
    f.write(titles[j][:-2]);
    f.write(descs[j][:-2]);
    f.write("</text> </query>\n");
f.write("</parameters>");
f.close();

#Narrative
print("writing title+description+narrative queries ...");
f = open("title+desc+narr.queries", "w")
f.write("<parameters>\n<index>"+indexPath+"</index>\n<rule>method:dirichlet,mu:1000</rule>\n<count>1000</count>\n<trecFormat>true</trecFormat>\n");
f.close();

f = open("title+desc+narr.queries", "a")
i = 300;
for j in range(0,len(titles)):
    i = i + 1;
    f.write("<query> <type>indri</type> <number>"+str(i)+"</number> <text>");
    f.write(titles[j][:-2]);
    f.write(descs[j][:-2]);
    f.write(narrs[j][:-2]);
    f.write("</text> </query>\n");
f.write("</parameters>");
f.close();

print("Done");
