from pyspark import SparkContext
import math
#get userid as key, value is (movie_id and rating)
#inpute movie and rating as inpute_movielist={'movie1':2.1,'movie2':3.5}
inpute_movielist={}
movielist = []
movielist2=[('1',1),('2',2),('3',3),
           ('4',4),('5',5),('6',1),('7',2),('8',3),
           ('9', 4), ('10', 5), ('11', 1), ('12', 2), ('13', 3),
           ('14', 4), ('15', 5)]
def extract_rating(record):
  try:
    user_id, movie_id, rating, timestamp = record.split(",")
    rating = float(rating)
    return (user_id,(movie_id, rating))
  except:
    return ()
def count_average_rating(record):
    user,movieidlists=record
    count=0
    ratingsum=0.0
    movelist_of_user=''
    for movieidlist in movieidlists:
        movieid,rating=movieidlist
        ratingsum=ratingsum+rating
        count=count+1
        ratingstr=str(rating)
        movelist_of_user=movelist_of_user+'|'+movieid+'|'+ratingstr
    averagerating=ratingsum/count
    averageratingstr=str(averagerating)
    values=averageratingstr+movelist_of_user
    return (user,values)

def movie_name_to_id(record):
    temp=record.strip().split(",")
    movieid=temp[0]
    if len(temp)>=3:
        movie_name=temp[1]
        if len(temp)>3:
            for i in range(2, len(temp) - 1):
                movie_name = movie_name + "," +temp[i]
    jud=0
    for ele in inpute_movielist:
        if ele==movie_name:
            value=inpute_movielist[ele]
            jud=1
    if jud==1:
        return[(movieid,value)]
    else:
        return []

def cereate_sim_matrix(record):
    user,value=record
    values=value.split("|")
    average=values[0];
    length=(len(values)-1)/2
    other_movielist=[]
    choose_movielist=[]
    pass_record_jud=True
    for i in range(int(length)):
        elei_isnot_in_movielist=True
        for ele in movielist:
            if ele[0]==values[2*i+1]:
                choose_movielist.append(2*i+1)
                pass_record_jud=False
                elei_isnot_in_movielist=False

        if elei_isnot_in_movielist:
            other_movielist.append(2 * i + 1)
    if pass_record_jud:
        return []
    else:
        resultset=[]
        for i in other_movielist:
            print(values[i])
            record_result = []
            for ele in movielist:
                jud=False
                for j in choose_movielist:
                    if ele[0]==values[j]:
                        a = float(values[i + 1]) - float(average)
                        b = float(values[j + 1]) - float(average)
                        jud = True
                if jud:
                    record_result.append((a,b))
                else:
                    record_result.append(None)
            resultset.append((values[i],record_result))

        return resultset

def put_value_of_key_together(a,b):
    return a+b
def sim_matrixreduce_creat(recordT):
    key,values=recordT
    length = len(movielist)
    coloums_number=len(values)/length
    toplist = [0.0 for i in range(length)]
    botleftlist = [0.0 for i in range(length)]
    botrightlist = [0.0 for i in range(length)]
    similrety = [0.0 for i in range(length)]

    for i in range(int(coloums_number)):
        for j in range(length):
            if values[length*i+j]!=None:
                toplist[j] = toplist[j] + values[length*i+j][0] * values[length*i+j][1]
                botleftlist[j] = botleftlist[j] + values[length*i+j][0] ** 2
                botrightlist[j] = botrightlist[j] + values[length*i+j][1] ** 2
    for i in range(length):
        temp=math.sqrt(botleftlist[i])*math.sqrt(botrightlist[i])
        if temp!=0:
            similrety[i]=toplist[i]/(temp)
    return key,similrety

def rating_predict(record):
    key,value=record
    length=len(movielist)
    a= int(length*2/3)
    dicforsort={}
    for i in range(length):
        dicforsort[value[i]]=i
    top_list=sorted(dicforsort,reverse=True)[:a]
    ratpredittop=0
    ratpreditbot=0
    for i in top_list:
        ratpredittop=ratpredittop+i*float(movielist[dicforsort[i]][1])
        ratpreditbot=ratpreditbot+abs(i)
    if    ratpreditbot!=0:
        return ratpredittop/ratpreditbot, key
    else:
        return 0,key
def add_new_key(record):
    return 1,record
def cut_result(record):
    key,value=record
    return [(value[2*i + 1], value[2*i]) for i in range(50) ]

def id_to_name(record):
    temp = record.strip().split(",")
    movieid = temp[0]
    if len(temp) >= 3:
        movie_name = temp[1]
        if len(temp) > 3:
            for i in range(2, len(temp) - 1):
                movie_name = movie_name + "," + temp[i]
    return movieid,movie_name

def creat_recom(line):
    key,value=line
    rating,values=value
    if len(str(rating))!=0:
        return [(rating,(values))]

def cut_result2(record):
    key,value=record
    return [(key,velueele) for velueele in value ]
def put_value_of_key_together2(a,b):
    return a+b
def getdic(record):
    temp = record.strip().split(",")
    rating = temp[-1]
    if len(temp) >= 2:
        movie_name = temp[0]
        if len(temp) > 2:
            for i in range(1, len(temp) - 1):
                movie_name = movie_name + "," + temp[i]
    return (movie_name,rating)


if __name__ == "__main__":
  sc = SparkContext(appName="Average Rating per Genre")
  ratings = sc.textFile("/share/movie/small/ratings.csv")
  movie_data = sc.textFile("/share/movie/small/movies.csv")
  rating_movie_dic=sc.textFile("/user/wtan4210/movie_rating.txt")

  #make a dictionary caled inpute_movielist it index is moviename and value is movie id
  rating_movie_dic_result=rating_movie_dic.map(getdic).collect()
  for elee in rating_movie_dic_result:
      moviename,rating=elee
      inpute_movielist[moviename]=rating


  user_ratings = ratings.map(extract_rating).groupByKey(1)
  user_ratings.saveAsTextFile("assignment/userrating")
  userlingmatrix=user_ratings.map(count_average_rating)
  userlingmatrix.saveAsTextFile("assignment/userrating")

  movie_name_to_id_result=movie_data.flatMap(movie_name_to_id)
  movie_name_to_id_result.saveAsTextFile("assignment/movieid")
  movie_name_to_id_result_new=movie_name_to_id_result.collect()
  for ele in movie_name_to_id_result_new:
      movielist.append(ele)
  sim_matrix_temp=userlingmatrix.flatMap(cereate_sim_matrix).reduceByKey(put_value_of_key_together)
  sim_matrix_temp.saveAsTextFile("assignment/movieid2")
  sim_matrix=sim_matrix_temp.map(sim_matrixreduce_creat)
  sim_matrix.saveAsTextFile("assignment/movieid3")
  ratingpredice=sim_matrix.map(rating_predict).sortByKey(ascending=False)
  recommendation_temp=ratingpredice.map(add_new_key)
  recommendation_temp2=recommendation_temp.reduceByKey(put_value_of_key_together)
  recommendation_temp3=recommendation_temp2.flatMap(cut_result)
  movie_id_to_name=movie_data.map(id_to_name)
  recommendation_result_temp=recommendation_temp3.leftOuterJoin(movie_id_to_name).flatMap(creat_recom).groupByKey(1)
  recommendation_result_temp2=recommendation_result_temp.flatMap(cut_result2)
  recommendation_result = recommendation_result_temp2.sortByKey(ascending=False)
  recommendation_result.saveAsTextFile("assignment/sim")






