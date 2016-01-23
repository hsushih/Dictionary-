import csv
import string

movieInfo={}
def create_actors_DB(actor_file):
    '''Create a dictionary keyed on actors from a text file'''
    f = open(actor_file)
    global movieInfo
    for line in f:
        line = line.rstrip().lstrip()
        actorAndMovies = line.split(',')
        actor = actorAndMovies[0]
        movies = [x.lstrip().rstrip() for x in actorAndMovies[1:]]
        movieInfo[actor] = set(movies)
    f.close()
    return movieInfo

scores_dict={}
def create_ratings_DB(ratings_file):
    '''make a dictionary from the rotten tomatoes csv file'''
    global scores_dict
    with open(ratings_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            scores_dict[row[0]] = [row[1], row[2]]
    return scores_dict


def insert_actor_info(actor,movies,movie_Db):
    ''' updating movies by sorting actors'''
    actor=stringToTitleCase(actor)
    if actor in movie_Db:
        actor = actor.rstrip().lstrip()
        movie_Db[actor].add(movies)
    else:
        movie_update = {}
        movie_update[actor]=movies
        movie_Db.update(movie_update)
    return movie_Db
        

def insert_rating(movie, ratings, ratings_Db):
    ''' updating ratings for new and existing movies'''
    if movie in ratings_Db:
        movie_rating_update = {}
        movie_rating_update[movie] = ratings
        ratings_Db.update(movie_rating_update)  
    else:
        ratings_Db[movie] = ratings
    return ratings_Db    
        
def delete_movie(movie, movie_Db, ratings_Db):
    ''' delete all information from the database that corresponds to this movie'''
    for item in movie_Db.itervalues():
        try:
            item.discard(movie)
        except ValueError:
            pass
    if movie in ratings_Db:
        del ratings_Db[movie]
    else:
        print ' no such movies'
        print ' the movies we have are'
    return(movie_Db, ratings_Db)
    

def select_where_actor_is(actorName,movie_Db):
    ''' given an actor, return the list of all movies'''
    actorName = stringToTitleCase(actorName)
    if actorName in movie_Db:
        return movie_Db[actorName]
    else:
        print ' no such an actor'
        return list()

def select_where_movie_is(movieName, movie_Db):
    ''' given a movie, return the list of all actors'''
    getMovie = list()
    movieName=stringToTitleCase(movieName)
    for actor, movies in movie_Db.iteritems():
        if movieName in movies:
            getMovie.append(actor)
    if len(getMovie) ==0:
        print 'no actors found'    
    return getMovie

def select_where_rating_is(targeted_rating,comparison,is_critic,ratings_Db):
    ''' returns a list of movies that satisfy an inequality or equality'''
    movie_list=list()
    if comparison =='>' and is_critic ==True:
        for movie,value in ratings_Db.iteritems():
            if int(value[0]) > targeted_rating:
                movie_list.append(movie)
                
    elif comparison =='<' and is_critic ==True:
        for movie,value in ratings_Db.iteritems():
            if int(value[0]) < targeted_rating:
                movie_list.append(movie)
                
    elif comparison =='=' and is_critic ==True:
        for movie,value in ratings_Db.iteritems():
            if int(value[0]) == targeted_rating:
                movie_list.append(movie)
    elif comparison =='>' and is_critic ==False:
        for movie,value in ratings_Db.iteritems():
            if int(value[1]) > targeted_rating:
                movie_list.append(movie)
                
    elif comparison =='<' and is_critic ==False:
        for movie,value in ratings_Db.iteritems():
            if int(value[1]) < targeted_rating:
                movie_list.append(movie)
                
    elif comparison =='=' and is_critic ==False:
        for movie,value in ratings_Db.iteritems():
            if int(value[1]) == targeted_rating:
                movie_list.append(movie)
    else:
        print ' there is no such rating'
    return movie_list
    
              

def get_co_actors(actorName, moviedb):
    ''' given an actor return a list of actors whom he/she has worked with'''
    actorName=stringToTitleCase(actorName)
    getActor=list()
    if actorName in moviedb:
        movie_list_given_actor=moviedb[actorName]
        for actors in moviedb:
            if len((moviedb[actors]).intersection(movie_list_given_actor))>=1:
                getActor.append(actors)
        getActor.remove(actorName)     
    if actorName not in moviedb:
        print 'no actors found'
    return getActor


def get_common_movie(actor1,actor2,moviedb):
    '''return the movies where both actors were cast'''
    common_movies=list()
    actor1=stringToTitleCase(actor1)
    actor2=stringToTitleCase(actor2)
    if actor1 in moviedb and actor2 in moviedb :
        movie_actor1=moviedb[actor1]
        movie_actor2=moviedb[actor2]
        if len((movie_actor1).intersection(movie_actor2))==0:
            print ' no common movies found'
        else:
            common_movies=(movie_actor1).intersection(movie_actor2)
    else:
        print ' no such actors in the movie database'
    return common_movies
      
                   
def critics_darling(movie_Db, ratings_Db):
    ''' finding the actor whose movies have the highest average rotten tomatoes rating, as per the critics'''
    criticValueList=list()
    movieMaximum=list()
    actors_in_highest_rates_movie=list()
    for item,value in ratings_Db.iteritems():
        criticValueList.append(int(value[0]))
        maxValue=max(criticValueList)
    for movie,score in ratings_Db.iteritems():
        if int(score[0]) == maxValue:
            movieMaximum.append(movie)       
    for actor,movie in movie_Db.iteritems():
        if (movie).intersection(movieMaximum):
            actors_in_highest_rates_movie.append(actor)
    return actors_in_highest_rates_movie

def audience_darling(movie_Db, ratings_Db):
    ''' finding the actor whose movies have the highest average rotten tomatoes rating, as per the audience'''
    criticValueList=list()
    movieMaximum=list()
    actors_in_highest_rates_movie=list()
    for item,value in ratings_Db.iteritems():
        criticValueList.append(int(value[1]))
        maxValue=max(criticValueList)
    for movie,score in ratings_Db.iteritems():
        if int(score[1]) == maxValue:
            movieMaximum.append(movie)
    for actor,movie in movie_Db.iteritems():
        if (movie).intersection(movieMaximum):
            actors_in_highest_rates_movie.append(actor)
    return actors_in_highest_rates_movie

def good_movies(ratings_Db):
    ''' returns the set of movies that both critics and the audience have rated above 85'''
    good_movie=select_where_rating_is(85,'>',True,ratings_Db)
    return set(good_movie)
        
        

def get_common_actors(movie1,movie2,movies_Db):
    ''' given a pair of movies, return a list of actors that acted in both'''
    commonActor=list()
    movie1=stringToTitleCase(movie1)
    movie2=stringToTitleCase(movie2)
    for actor,movie in movies_Db.iteritems():
        if movie1 in movie and movie2 in movie:
            commonActor.append(actor)
    return commonActor   
            

        
def stringToTitleCase(input_string):
    ''' given a random name retruns a uppercase and lowercase name'''
    if type(input_string) == str:
        return " ".join([word.capitalize() for word in input_string.split() if word != 'and'])
    elif type(input_string) == list:
        return (",".join(stringToTitleCase(word) for word in input_string)).split(',')        



def ask_user_to_select():
    '''ask user to select from the following options'''
    print ''' welcome to Stanley Movie World!!!!!! please select an option from the drop-down menu'''
    print ''' (1) list all movies acted by a given actor'''
    print ''' (2) all cast in a given movie'''
    print ''' (3) coActors'''
    print ''' (4) common movies performed by two actors'''
    print ''' (5) actors in the highest rated movies by critics'''
    print ''' (6) actors in the highest rated movies by audience'''
    print ''' (7) great movies who have got over 85 in critics and audience ratings'''
    print ''' (8) actors who acted in two movies'''
    print ''' (9) want to what good movies and bad moives - select this option'''
    print ''' (10) exit the program '''
    option=raw_input('select one option')
    return option

def want_to_know_movie_by_actor():
    ''' ask user to enter an actor to get a list of movies acted by that actor'''
    actor=raw_input('enter an actor to see what movies he/she has acted')
    print select_where_actor_is(actor,create_actors_DB('movies.txt'))
    
def want_to_know_actors_by_movies():
    ''' ask user to enter a name of movie to find a list of actors who performed in that movie'''
    movie=raw_input('please enter the movie you know to see a list of actors who played in that movie')
    print select_where_movie_is(movie,create_actors_DB('movies.txt'))

def want_to_know_coActors():
    ''' ask users for a name of an actor'''
    actor=raw_input('please enter an actor to see who he/she has worked with')
    print get_co_actors(actor,create_actors_DB('movies.txt'))
    
def want_to_know_commonMovie():
    ''' ask users two actors to find out the common movies'''
    actor1=raw_input('enter the first actor')
    actor2=raw_input('enter the second actor')
    print get_common_movie(actor1,actor2,create_actors_DB('movies.txt'))

def want_to_know_actors_in_the_highest_ratings_movie_from_critics():
    ''' find out a list of actors from movies that have the highest ratings from critics'''
    print critics_darling(create_actors_DB('movies.txt'),create_ratings_DB('moviescores.csv'))

def want_to_know_actors_in_the_highest_ratings_movie_from_audience():
    ''' find out a list of actors from movies that have the highest ratings from audience'''
    print audience_darling(create_actors_DB('movies.txt'),create_ratings_DB('moviescores.csv'))
    
def want_to_know_good_movies():
    ''' find out movies who got 85 from critics and auidence'''
    print good_movies(create_ratings_DB('moviescores.csv'))

def want_to_know_a_random_rating():
    ''' find out the good movies and bad movies by ratings from critcis and audience'''
    targeted_rating=input('enter a rating you want to enter')
    comparsion=raw_input(' please enter >,+,< for finding out the movies')
    critic=input('enter True or False')
    print select_where_rating_is(targeted_rating,comparsion,critic,create_ratings_DB('moviescores.csv'))
    
                     
                         
def want_to_know_actors_in_two_movies():
    ''' find out the actors in two movies'''
    movie1=raw_input('enter the first movie')
    movie2=raw_input('enter the second movie')
    print get_common_actors(movie1,movie2,create_actors_DB('movies.txt'))



def main():
    choice=0
    while choice==0:
        option=ask_user_to_select()
        if option =='1':
            print "\n" * 1
            want_to_know_movie_by_actor()
        elif option =='2':
            print "\n" * 1
            want_to_know_actors_by_movies()
        elif option =='3':
            print "\n" * 1
            want_to_know_coActors()
        elif option =='4':
            print "\n" * 1
            want_to_know_commonMovie()
        elif option =='5':
            print "\n" * 1
            want_to_know_actors_in_the_highest_ratings_movie_from_critics()
        elif option =='6':
            print "\n" * 1
            want_to_know_actors_in_the_highest_ratings_movie_from_audience()
        elif option =='7':
            print "\n" * 1
            want_to_know_good_movies()
        elif option =='8':
            print "\n" * 1
            want_to_know_actors_in_two_movies()
        elif option == '9':
            print "\n" * 1
            want_to_know_a_random_rating()
        elif option =='10':
            print ' thank you for using Stanley Movie World! Enjoy the rest of your day!!!'
            choice=1
        else:
            print ' please enter an option from the menu'
            
        print "\n" * 3    
            
            
            
if __name__ == "__main__":
    main()
            
            
            
