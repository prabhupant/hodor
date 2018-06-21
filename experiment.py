import nltk

#add a request checker to see what type of request has been entered
#then direct it either to the brain to process the request, or to the sub-brain to add the new user to the database

query = input("enter the query")
lst = q.split(' ')

if lst[0] == 'add':
	#call function to add new user

elif lst[1] == 'check':
	#call function to check status

else:
	#call brain to do the rest work
