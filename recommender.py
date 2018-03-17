import numpy as np
import pandas as pd
from scrap_data import dataset

#print(dataset['user_1']['meme_3'])

def similarity_index(user1, user2) :
	

	#distance = euclidian_distance(user1, user2)
	#ans = 1/(1+np.sqrt(distance))
	ans = pearson_similarity(user1, user2)
	return ans

def euclidian_distance(user1, user2 ) :
	common_views = {} #to get a dict of memes seen by both the users
	for item in dataset[user1] :
		if item in dataset[user2]:
			common_views[item] = 1
	
	if len(common_views)==0 : # this means that both the users have 0 common rating elements
		return 0

	euclid_distance = 0
	for item in dataset[user1] :
		if item in dataset[user2] :
			temp = (dataset[user2][item]-dataset[user1][item])**2
			euclid_distance = euclid_distance+temp
	return euclid_distance

def pearson_similarity(user1, user2) :
	common_views = {}
	for item in dataset[user1] :
		if item in dataset[user2] and dataset[user1][item]!=0 and dataset[user2][item]!=0 : 
			common_views[item] = 1

	total_ratings = len(common_views)

	if total_ratings == 0 :
		return 0 

	user1_sum = 0
	user1_square = 0

	for item in common_views :
		user1_sum = user1_sum + dataset[user1][item]
		user1_square = user1_square + dataset[user1][item]**2

	user2_sum = 0
	user2_square = 0
	for item in common_views :
		user2_sum = user2_sum + dataset[user2][item]
		user2_square = user2_square + dataset[user2][item]**2

	Sxx = user1_square - (user1_sum**2/total_ratings)
	Syy = user2_square - (user2_sum**2/total_ratings)

	xy_sum = 0
	for item in common_views :
		xy_sum = xy_sum + dataset[user1][item]*dataset[user2][item]

	Sxy = xy_sum - (user1_sum*user2_sum/total_ratings)
	#print(Sxx)
	#print(Syy)
	#print(Sxy)
	#print(np.sqrt(Sxx*Syy))
	denom = np.sqrt(Sxx*Syy)
	if denom == 0 :
		return 0
	pearson_value = Sxy/denom
	return pearson_value




def other_users(user) :
	similarity_scores = {}
	for users in dataset :
		if users != user :
			temp_score = pearson_similarity(user, users)
			similarity_scores[users] = temp_score
	return similarity_scores


	# now that we have got similarity index between different users, we could directly review movies to our users that the most similiar user viewer viewed
	# and liked it.
	# But this is not a good way because it can give us users that haven't rated any of the movies that our user liked. Or it can recommend strange movies 
	# that 
	# out similiar user liked but all the users didn't liked it. Therefore even though we will decide mostly on views of most viewed user but we will also
	# take 
	# contributions for remaining users as well to ensure that any strange movie that our similiar user liked but all others disliked is not recommended.

	#We can do this by associating weights to all users with most similiar user getting higest weight
def recommend(user) :
	similarity_scores = other_users(user)
	unrated = []
	for element in dataset[user] :
		if dataset[user][element] == 0:
			unrated.append(element)

	
	recommendation_score = {}
	for element in unrated :
		total = 0
		sim_sum = 0
		for users in dataset :
			if users!= user and dataset[users][element]!=0 :

				sim = pearson_similarity(user, users)
				if sim<=0 :
					continue
				#print(users+" " + str(sim))
				sim_sum = sim_sum+sim
				total = total+ sim*dataset[users][element]
		#print(sim_sum)
		#print(total)
		if sim_sum == 0 :
			recommendation_score[element] = 0
			continue
		recommendation_score[element] = total/sim_sum
	return recommendation_score

d = recommend('Lisa Rose')
print(d)