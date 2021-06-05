from nltk.corpus import wordnet

############################### SYNONYMS FINDER FUNCTION ##############################################
def synonym(word,count):
	synonyms = []
	for syn in wordnet.synsets(word):
	    for lemma in syn.lemmas():
		synonyms.append(lemma.name())
	if len(synonyms)<int(count):
		for time in range(int(count)-len(synonyms)):
			synonyms.append(word);
		return synonyms
	else:
		return synonyms[:int(count)]


poutsa = synonym('dick', 20);
#print(poutsa)

def synonymSentences(fullString, count):
	eachWord = fullString.split()
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
	final = final.join(sentences)# make it string 
	return final

def allPossibleCombinations(fullString, synonymsAmount): 
	eachWord = fullString.split()
	synonymsPerWord = []
	allSentences = []
	sentence =  eachWord
	poutsaFINAL = []
	final = ""
	temp = []
	for wordsInSentence in range(len(eachWord)):
		synonymsPerWord.append(synonym(eachWord[wordsInSentence],synonymsAmount))
	'''print(len(synonymsPerWord))
	print(len(synonymsPerWord[0]))
	for item in range(len(synonymsPerWord)):
		print(str(item) +" : " +" ".join(synonymsPerWord[item]))'''
	totalNumberOfSentences = 0;
	for positionInSentence in reversed(range(len(eachWord))):
		#print(sentence[positionInSentence])
		#changing only the sentencePositionInSentence 
		#print("POSITION : " + str(positionInSentence))
		for counter in range(synonymsAmount):
			#sentence[:] =""
			#print("SENTENCE   " + " ".join(sentence));
			allSentences.append(sentence)
			print("TOTAL NUMBER OF SENTENCES: " +str(totalNumberOfSentences) + " POSITION : " +  str(positionInSentence))
			totalNumberOfSentences = totalNumberOfSentences +1
			temp = synonymsPerWord[positionInSentence][counter]

			#print("COUNTER : "+str(counter))
			print("                  To Be Replaced "+allSentences[totalNumberOfSentences-1][positionInSentence])
			print("                  Replace with this: "+temp)
			allSentences[totalNumberOfSentences-1][positionInSentence] = temp
			print("                  CHECK IF REPLACED "+allSentences[totalNumberOfSentences-1][positionInSentence])

			
			#temp=temp+" ".join(allSentences[totalNumberOfSentences-1])
			
	#for item in temp:
	#	print(item)
	'''print(poutsaFINAL)
	poutsakiFINAL = []
	for number in range(totalNumberOfSentences):
		poutsakiFINAL.append([])
		poutsakiFINAL[number] = ""
		for word in range(len(poutsaFINAL)):
			if((synonymsAmount+1)%(word+1) ==0):
				poutsakiFINAL[number] = poutsakiFINAL[number] + poutsaFINAL[word]
	print(poutsakiFINAL)'''

#			print(allSentences[totalNumberOfSentences-1][positionInSentence] + "--------- at position Num:" +str(totalNumberOfSentences-1) + " pos:" + str(positionInSentence) );


	##print("ROWS: " +str(len(allSentences)))
	#print("COLUMNS: " +str(len(allSentences[0])))

	#print(allSentences)

#	for positionChanging in range(len(eachWord)):
#		sentence[positionChanging] = ""
#		for counter in range(count):
#			sentences.append("")
#			for wordCounter in range(len(eachWord)):		
#				sentence[positionChanging] = synonymsPerWord[wordCounter][counter]
#				sentences[counter] = sentences[counter] + sentence[positionChanging]
#			sentence[positionChanging] = ""
#
	
#print(sentences)

			#sentences.append(sentence)
			#sentence = ""


	
	
#poutsa = synonymSentences('Another dick in the wall',10);
#print(poutsa)
############################### OPEN FILES - PRINT WORDS ##############################################


poutsa = allPossibleCombinations('Another dick in the wall',3);
