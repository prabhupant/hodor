import nltk

FLAG = 0 #for NNS checking if requests are of the format "after 3 hours open the door"

#function for POS tagging
def tagger(sentence):
	tokenized = nltk.word_tokenize(sentence)
	tagged = nltk.pos_tag(tokenized)
	return tagged

#function for chunking 	
def chunker(sentence):
	tagged = tagger(sentence)
	entities = nltk.chunk.ne_chunk(tagged)
	return entities
	
#function for checking if word is a time word
def time_word_check(word):
	time_list = ['mins', 'min', 'hours', 'hr', 'hrs', 'sec', 'secs', 'seconds', 'am', 'a.m.', 'a. m.', 'a.m', 'a. m', 'pm', 'p.m.', 'p. m.', 'p.m', 'p. m', 'AM', 'A.M.', 'A. M.', 'A.M', 'A. M', 'PM', 'P.M.', 'P. M.', 'P.M', 'P. M']
	if word in time_list:
		return True
	else:
		return False
	
	
#function to extract the target object
def extract_noun(sentence):
	tagged = tagger(sentence)
	
	noun = ''
	
	for word, pos in tagged:
		if pos == 'NN' or pos == 'NNS':
			if time_word_check(word) or FLAG == 1:
				continue
			else:
				noun = word
				break
			
	return noun
	
#function to extract the name of the target person
def extract_name(sentence):
	entities = chunker(sentence)
	named_entities = []
	counter = 0
	
	need_NNP = 0

	for t in entities.subtrees():
		if t.label() == 'PERSON':
			named_entities.append(t)
			counter = counter + 1	
	
	if not named_entities:
		for word, pos in tagger(sentence):
			if pos == 'NNP':
				name = word
				return name
	#converting named_entities to strings
	if counter == 0:
			ent = str(entities)
			ent = ent.replace('/', ' ').replace('\n', '')
			lst = ent.split(' ')
			ind = lst.index('NNP')-1
			name = lst[ind]
			return name
			
	new_named_entities = str(named_entities)
	new_named_entities = new_named_entities.split(',')
	name = new_named_entities[1]
	name = name.replace('[', '').replace('(','').replace(' ', '').replace("'", '')
	return name
	
#function to extract the action to be done
def extract_verb(sentence):
	tagged = tagger(sentence)
	
	verb = []

	for word, pos in tagged:
		if pos == 'VB' or pos =='VBD' or pos =='VBG' or pos =='VBN' or pos =='VBP' or pos =='VBZ' or pos == 'JJ' or pos == 'RB' or pos == 'RBR' or pos == 'RBS': 
			if time_word_check(word) == False:
				verb.append(word)

	return verb
	
def extract_time(sentence):
	tagged = tagger(sentence)
	
	time_number = ''
	
	for word, pos in tagged:
		if pos == 'CD':
			time_number = word
			break
	
	time_index = tagged.index((word,pos))
	indicator_time = tagged[time_index-1][0]
	
	if 'am' in word or 'a.m.' in word or 'a. m.' in word or 'a. m' in word or 'a.m' in word or 'AM' in word or 'A.M.' in word or 'A.M' in word:
		min_hr_sec = 'A.M.'
		time_of_action = indicator_time + ' ' + time_number + ' ' + min_hr_sec
		return time_of_action
	elif 'pm' in word or 'p.m.' in word or 'p. m.' in word or 'p. m' in word or 'p.m' in word or 'PM' in word or 'P.M.' in word or 'P.M' in word:
		min_hr_sec = 'P.M.'
		time_of_action = indicator_time + ' ' + time_number + ' ' + min_hr_sec
		return time_of_action
	
	
	
	min_hr_sec = tagged[time_index+1][0]
	if 'min' in min_hr_sec:
		min_hr_sec = 'minutes'
	elif 'hour' in min_hr_sec or 'hr' in min_hr_sec:
		min_hr_sec = 'hour'
	elif 'sec' in min_hr_sec:
		min_hr_sec = 'seconds'
	elif 'am' in min_hr_sec or 'a.m.' in min_hr_sec or 'a. m.' in min_hr_sec or 'a. m' in min_hr_sec or 'a.m' in min_hr_sec or 'AM' in min_hr_sec or 'A.M.' in min_hr_sec or 'A.M' in min_hr_sec:
		min_hr_sec = 'A.M.'
	elif 'pm' in min_hr_sec or 'p.m.' in min_hr_sec or 'p. m.' in min_hr_sec or 'p. m' in min_hr_sec or 'p.m' in min_hr_sec or 'PM' in min_hr_sec or 'P.M.' in min_hr_sec or 'P.M' in min_hr_sec:
		min_hr_sec = 'P.M.'	
	
	FLAG = 1		#increasing the value of flag
	
	time_of_action = indicator_time + ' ' + time_number + ' ' + min_hr_sec
	return time_of_action


#check if time is present in the query
def check_time_exist(sentence):
	entities = chunker(sentence)
	ent = str(entities)
	if 'CD' in ent:
		return True
	else:
		return False
		
#check if a person is present in the query
def check_person_exist(sentence):
	entities = chunker(sentence)
	ent = str(entities)
	if 'PERSON' in ent or 'NNP' in ent:
		return True
	
	else:
		return False


def main(lines):
	action = extract_verb(lines)
	object = extract_noun(lines)
	
	if check_person_exist(lines):
		person = extract_name(lines)
		
	if check_time_exist(lines):
		time = extract_time(lines)
		print("time - ", time)
		
	task = action[0]
	
	tasks = {
		'PERSON' : person,
		'TIME' : time,
		'ACTION' : task,
		'OBJECT' : object
	}
