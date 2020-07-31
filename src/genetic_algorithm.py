import numpy 
import random
from client_moodle import get_errors,submit 

def crossover(arr1,arr2):
    #### one-point cross-over
    shape=(1,11)
    new=numpy.zeros(shape)

    #k=random.randrange(0,11,1)
    for i in range(0,11):

        prob2=random.random()
        if prob2<0.5:
            new[0][i]=arr2[i]
        else:
            new[0][i]=arr1[i]
        ### made 2 off-springs
        #if prob2<0.5:
         #   new[1][i]=arr1[i]
        #else:
           # new[1][i]=arr2[i]
    #print (new)
    return new

def mutate(arr):
    
    i=random.randrange(0,11,1)
    p = random.random()
    # print('prob of mutation:',p)
    if p < 0.3:
            #idx = random.randrange(5,11,1)
            # arr[i]=random.uniform(-10,10)
        # print('mutating weight:',i)
        arr[i]=arr[i]*(random.uniform(0.9,1.1))
        # print('Mutated to')
        # print(arr)
    # else:
        # print('no mutation since p > 0.3')

    if arr[i] >= 10:
        arr[i]=9.999
    if arr[i] <= -10:
        arr[i] = -9.999
                       
                     
    return arr

def create_error_for_manual_testing():
    x=random.randrange(0.999999999999999e+32,9.999999999999999e+34)
    y=random.randrange(0.999999999999999e+32,9.999999999999999e+34)
    return [x,y]

def create_new_pop(error_list,population,prob):
    #### sort the current pop according to their fitness value
    new_pop=numpy.zeros(pop_size)
    error_list=sorted(error_list,key = lambda x: x[1])
    #print(numpy.size(error_list))
        ### now select top 3 from error_list[2]i.e. chromosome into new_pop numpy array	
    var=28
# pos = ['0']*15 +['1']*14 + ['2'] *13 + ['3']*12 +['4']*11 + ['5'] *10 + ['6']*9 +['7']*8 + ['8'] *7 + ['9']*6 +['10']*5 + ['11'] *4+['12']*3+['13']*2+['14']*1
    pos = ['0']*7 +['1']*6 + ['2'] *5 + ['3']*4+['4']*3 +['5']*2 +['6']*1 
    # for i in range(0,7):
    #     idx=((error_list[i][0]))
        # print('vector-----')
        # print('index:',error_list[i][0],'\n',population[idx])
        # print('probability')
        # print((7-i)/var)
    
    for i in range(0,3):
        idx = error_list[i][0]
        new_pop[i]=numpy.copy(population[idx])

        ### use these 5 to create 20 chromosomes using  cross over and mutation 
    for i in range (0,4): ## one iteration creates 2 offspring
        
        ind1=int(random.choice(pos))
        ind2=int(random.choice(pos))
        while ind1==ind2:
            ind2 = random.randrange(0,3,1)

        # print('Crossover starting-----')
        # print('Vectors for cross over------')
        # print('probability of choosing these vectors----')
        # if ind1==0:
        #     print(0.25,ind2/var)
        # elif ind2==0:
        #     print(ind1/var,0.25)
        # else:
        #     print(ind1/var,ind2/var)
        # print('selecting indices for crossover:',ind1,ind2)
        # print(population[ind1],population[ind2])
        temp=crossover(population[ind1],population[ind2])
        new_pop[3+ i] = numpy.copy(temp[0])
        # print('crossover succesful,new vector is:')
        # print(temp[0])

        x=mutate(temp[0])
        new_pop[3+ i]=numpy.copy(x)

        # print('Crossover and mutation finsished-----')

    return new_pop


team_id='St0WqOenu3543rZHrK2slWsnWWaRxtPXMeXynMX7GJQK2ERUva'

num_weights = 11
num_solution = 7 #Defining the no of chromosomes.

pop_size = (num_solution,num_weights) #shape of population list

overfit=numpy.array([0.0, 0.1240317450077846, -6.211941063144333, 0.04933903144709126, 0.03810848157715883, 8.132366097133624e-05, -6.018769160916912e-05, -1.251585565299179e-07, 3.484096383229681e-08, 4.1614924993407104e-11, -6.732420176902565e-12] )
population=numpy.zeros(pop_size)
#population=numpy.array()


for i in range(pop_size[0]):
    population[i]=numpy.copy(overfit)
min_error=float('inf')
min_weights=[]
iteration=0
submittotal=0
min_itr=-1
#print(pop_size)
print(num_solution)
while(iteration <3):
    print(iteration,'////////////////////////////////////////////////////////////////////////')
    print('population',population)

    error_list=[]
    prob=numpy.zeros(num_solution)
        ### step1:: find the error for each chromosome
    for i in range(0,num_solution):
            #### change population[i] to a list of length 11 
        temp=numpy.copy(population[i])
        new_list=numpy.array(temp).tolist()

        error_val=get_errors(team_id,new_list) ###
        #error_val=create_error_for_manual_testing() 
        print("idx:",i,"\t","error_val:",error_val)

        ### now call 
        # total_error=error_val[0]+ error_val[1] +max(error_val[0],error_val[1])
        total_error=error_val[0] + error_val[1] 
        if total_error< min_error:
            min_error=total_error
            min_weights=numpy.copy(new_list)
            print('min_weights')
            print(numpy.array(temp).tolist())
            print(submit(team_id,numpy.array(new_list).tolist()))
            submittotal+=1
            
            min_itr=iteration
            ##submit(team_id,)
        error_list.append([i,total_error])
        prob[i]=total_error

    ### step2 :: select parent for cross-over and mutation 			
    ### select best 20-25% and use them to generate new pop
    new_pop=create_new_pop(error_list,population,prob)  ## sort chromosomes according to their fitness value

    print('----------------------------------------------')
    print('new population',new_pop)

    iteration+=1
    population=numpy.copy(new_pop)

print('min_error:',min_error)
print('min_weights:',numpy.array(new_list).tolist())
print('min_itr:',min_itr)
print(submittotal)
