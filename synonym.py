import math

##Part 1
def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)
    
    
def cosine_similarity(vec1, vec2):
    import math
    '''
    sim(vec1,vec2)=(a)/(y*z) 
    where a is the item of key M in vec1 * the
    item of key M in vec1 + the item of key N in vec2 * the item of key N in
    vec2 and so on. y is the square of the magnitude of the shorter vector
    while z is the square of the magnitude of longer vector.
    '''
    
    a,y,z=0,0,0
    
    #Finding which vector is smaller
    if len(vec1)<len(vec2):
        short=vec1
        long=vec2
    else:
        short=vec2
        long=vec1
    
    for word,count in short.items():
        if word in long:
            a+=count*long[word]
        y+=count*count
    
    for word,count in long.items():
        z+=count*count

    return a/math.sqrt(y*z)

def build_semantic_descriptors(sentences):
    d={}
    for sentence in sentences:
        checked=[]
        for word in sentence:
            #print (word)
            if word not in checked:
                if word not in d:
                    d[word]={}
                checked_within=[]
                for check in sentence:
                    #print (word,check)
                    if check not in checked_within:
                        if check != word:
                            if check not in d[word]:
                                d[word][check]=0
                            d[word][check]+=1
                            checked_within.append(check)
                
                checked.append(word)
    return d
    

    
#print(build_semantic_descriptors([['a', 'b', 'd'], ['d', 'a', 'a', 'a'], ['t', 'b']]))    
    
    
    

def build_semantic_descriptors_from_files(filenames):
    result = {}
    for index in range(len(filenames)):
        text = open(filenames[index], "r", encoding = "utf-8")
        text = text.read()
        text = text.lower()
        
        text = text.replace("\n", " ")
        text = text.replace(","," ")
        text = text.replace("("," ")
        text = text.replace(")"," ")
        text = text.replace("-"," ")
        text = text.replace("--"," ")     
        text = text.replace(':', " ")
        text = text.replace(';', " ")
        text = text.replace('"', " ")
        text = text.replace("]", " ")
        text = text.replace("'", " ")

        text = text.replace("? ",".")
        text = text.replace("! ",".")
        text = text.replace(". ",".")

     

        
        text = text.split(".")
        
        
        for i in range(len(text)):
            text[i] = text[i].strip().split()
        # print(text)
            
        dic = build_semantic_descriptors(text)
        # print(dic.keys())
        for key in dic:
            if key == '':
                del key
            elif key not in result:
                if '' == dic[key]:
                    continue
                result[key] = dic[key]
            elif key in result:
                for key_key in dic[key]:
                    if key_key not in result[key]:
                        result[key][key_key] = dic[key][key_key]
                    elif key_key in result[key]:
                        result[key][key_key] += dic[key][key_key]
                        
            
        
    return result


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    best_sim=0
    best_sim_value=0
    previous_best_sim = 0
    

    for i in range(len(choices)):
        #print (word)
        #print (word in semantic_descriptors)
        if word in semantic_descriptors and choices[i] in semantic_descriptors:
            similarity = similarity_fn(semantic_descriptors[word],semantic_descriptors[choices[i]])
            #print (choices[i])
            #print (choices[i])
            #print (similarity*1000,best_sim*1000)
            #print (similarity>best_sim)
            if similarity_fn == cosine_similarity:
                if similarity>best_sim_value: 
                    best_sim=i
                    best_sim_value=similarity
            if similarity_fn == sim_euc or similarity_fn == sim_euc_nor:
                if previous_best_sim == 0:
                    previous_best_sim = similarity
                    best_sim = i
                elif previous_best_sim < similarity:
                    
                    best_sim=i
                    best_sim_value=similarity
            # print (choices[i])
            # print (similarity)
            # print (" ")
        #Maybe not needed because even if it was a tie, it would be of greater index

    return best_sim


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    # print (" ")
    num_correct=0
    
    f=open(filename)
    s=f.read()
    
    s = s.strip()
    
    s=s.split("\n") #split file into questions
    total=len(s)#total is the number of questions
    
    for i in range (len(s)): #going through the questions
        s[i]=s[i].split(" ")
        # print (s)
        
        x = most_similar_word (s[i][0],s[i][2:],semantic_descriptors,similarity_fn)
        if s[i][2+x]==s[i][1]:
            num_correct += 1
    
    #print (total)
    return num_correct/total
    
import os

os.chdir("C:\Users\Owner\Desktop")

# a = {'love':{'a':4, 'b':1}, 'hate': {"a":4, "c":1}, 'people':{'b':1,'c':1}}
# # print(build_semantic_descriptors_from_files(["testing"]))    
# print(run_similarity_test('test5', a, cosine_similarity))
#     


    
# print(build_semantic_descriptors_from_files(["test1", "test2"]))    



# from timeit import default_timer as timer
# 
# start = timer()
# run_similarity_test("test_code", build_semantic_descriptors_from_files(["test1", "test2"]) , cosine_similarity)
# end = timer()
# print(end - start) 



a = build_semantic_descriptors_from_files(["test1", "test2"])
# print(a)
###
print(run_similarity_test("test_code", a , cosine_similarity))
print(run_similarity_test("test_code", a , sim_euc))
print(run_similarity_test("test_code", a , sim_euc_nor))


    
##Part 2
def sim_euc(vec1,vec2):
    import math
    result = 0
    for i in vec1.keys():
        difference = 0
        if i in vec2:
            difference = vec1[i] - vec2[i]
            result += difference**2
    return -math.sqrt(result)
    
def sim_euc_nor(vec1, vec2):
    import math
    result = 0    
    sparse_vec1 = []
    sparse_vec2 = []
    for i in vec1.keys():
        if i in vec2:
            sparse_vec1.append(int(vec1[i]))
            sparse_vec2.append(int(vec2[i]))
            
    vec1_len = 0
    vec2_len = 0
    
    for j in range(len(sparse_vec1)):
        vec1_len += sparse_vec1[j]**2
        vec2_len += sparse_vec2[j]**2
        
    vec1_len = math.sqrt(vec1_len)
    vec2_len = math.sqrt(vec2_len)
    
    for k in range(len(sparse_vec1)):
        sparse_vec1[k] = sparse_vec1[k] / vec1_len
        sparse_vec2[k] = sparse_vec2[k] / vec2_len
        
    result = 0
    for i in range(len(sparse_vec1)):
        difference = sparse_vec1[i] - sparse_vec2[i]
        result += difference**2
            
    return -math.sqrt(result)
        
print(sim_euc({'i':1, 'j':2, 'k':3}, {'i':4, 'j':5, 'k':6}))

from matplotlib.pyplot import *



if __name__ == '__main__':
    import os
    os.chdir("C:/ChomeBB/Work/U1/Programming/Project 3")
    e=build_semantic_descriptors_from_files(["t.txt"])
    #print (cosine_similarity(e["man"],e["liver"]))
    #print (e["liver"])