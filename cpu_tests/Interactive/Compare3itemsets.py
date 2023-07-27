import time

'''
Apriori.py Implementation 
'''


def create_Combinations(iterable, combination_size):
    group = tuple(iterable)
    # first you create a tuple of the original input which you can refer later with
    # the corresponding indices
    tuple_size = len(group)
    # get the length of the tuple

    if combination_size > tuple_size:
        return
    # if the length of the desired combination is higher than the length of the tuple
    # it is not possible to create combination so return without doing something

    indexes = list(range(combination_size))
    # create the first list of indices in normal order ( indices = [0,1,2,3,...,combination_size])
    # up to the desired range combination_size

    yield tuple(group[i] for i in indexes)
    # return the first permutation which is a tuple of the input with the original
    # indices up to combination_size tuple(tuple[0], tuple[1],....,tuple[r])
    while True:
        for i in reversed(list(range(combination_size))):
            # i will go from combination_size-1, combination_size-2, combination_size-3, ....,0
            if indexes[i] != i + tuple_size - combination_size:
                # if condition is true except for the case
                # that at the position i in the tuple the last possible
                # character appears then it is equal and proceed with the character
                # before which means that this character is replaced by the next
                # possible one
                break
        else:
            # when the for loop completely finished then all possible character
            # combinations are processed and the function ends
            return
        indexes[i] += 1
        # as written proceed with the next character which means the
        # index at i is increased
        for j in list(range(i + 1, combination_size)):
            indexes[j] = indexes[j - 1] + 1
            # all the following indexes are increased as
            # well since we only want to at following
            # characters and not at previous one or the
            # same which is index at indexes[i]
        yield tuple(group[i] for i in indexes)
        # return the new tuple


# function processes the transaction data from the csv file and returns a Transactions list
def load_transactions(path_to_data, order):
    Transactions = []

    with open(path_to_data, 'r') as fid:

        for lines in fid:
            str_line = list(lines.strip().split(', '))
            # print(str_line)
            while ("" in str_line):
                str_line.remove("")
            str_line.sort(key=lambda x: order.index(x))
            Transactions.append(str_line)

    return Transactions

# function processes all the item from the transactions and return unique items as a list

def load_orders():
    Transactions = []
    with open(path_to_data) as fid:
        for lines in fid:
            str_line = list(lines.strip().split(', '))
            # print(str_line)
            Transactions.append(str_line)
    # list(filter(None,[list(filter(None,l)) for l in Transactions]))
    order = []
    for j in Transactions:
        for i in j:
            order.append(i)
    order = list(set(order))
    order.sort()
    while ("" in order):
        order.remove("")
    return order

# helper function get_frequent() to keep track of the frequency of the item set
# function will receive C of the corresponding iteration , Transaction to check the frequency, min support and discarded to avoid counting
# itemset that conatins subset that were previosuly discarded
# function returns frequent item sets, support and the new discarded item sets that will be used in the new iteration

def get_frequent(itemsets, Transactions, min_support, prev_discarded):
    # initialize frequent item set list
    L = []
    # initalize support count list that will give list of support count
    supp_count = []
    # itemset that will be discarded in current transcation will be stored in new_discarded
    new_discarded = []
    # num_trans will be used to calculate the frequency
    num_trans = len(Transactions)
    # k will keep length of previously dicarded sets of itemsets
    k = len(prev_discarded.keys())

    # go over itemsets , to check if the itemsets contain any subsets tha was previously discarded and than calculate the frequency
    for s in range(len(itemsets)):
        # flag variable to check for the subsets that were previosuly discarded
        discarded_before = False

        # if the size of previously discarded items > 0 that means we have items discarded in previous iteration
        # than check if the previously discarded itemsets are subsets of the. current itemsets
        if k > 0:
            for it in prev_discarded[k]:
                if set(it).issubset(set(itemsets[s])):
                    discarded_before = True
                    break
        # if the itemsets does not contain any previously discarded subset, than count using helper function count_occurences that will
        # take itemset and the transcations and returns the count
        if not discarded_before:
            count = count_occurrences(itemsets[s], Transactions)
            # check if the no of occurences/ total transcations > threshold to check if it is frequent and than append it to L and the support count
            if count / num_trans >= min_support:
                L.append(itemsets[s])
                supp_count.append(count)
            # if it does not pass the threshold save it in the new discarded itemsets
            else:
                new_discarded.append(itemsets[s])
    return L, supp_count, new_discarded

# function to count occurences of each itemset
def count_occurrences(itemset, Transactions):
    count = 0
    # if the item is a subset of the transaction than increment the count
    for i in range(len(Transactions)):
        if set(itemset).issubset(set(Transactions[i])):
            count += 1
    return count


# function to print the table
def print_table(T, supp_count):
    print("Itemset | Frequency")
    for k in range(len(T)):
        print("{}:  {}".format(T[k], supp_count[k]))

    print('\n')

def join_three_itemsets(it1, it2, it3, order):
    # sort each itemsets according to position each item has in the order
    it1.sort(key=lambda x: order.index(x))
    it2.sort(key=lambda x: order.index(x))
    it3.sort(key=lambda x: order.index(x))

    # join critertia - check if they are joinable, means all the itemsets are in the sorted itemsets are the same except the last one, in the last one
    # which belongs to the second itemset must be greater than the last one in the first itemsets

    for i in range(len(it1) - 1):
        # if it is different return empty list
        if it1[i] != it2[i] != it3[i]:
            return []

    # checkign the last item in each of the itemsets and adding it
    if order.index(it1[-1]) < order.index(it2[-1]) < order.index(it3[-1]):
        return it1 + [it2[-1]] + [it3[-1]]

    # if above conditions does not satisy
    return []


def join_set_itemsets(set_of_its, order):
    # to return a list of candidates
    C = []
    # go over each itemsets and compare with all the ones that are after that specific itemsets so i + 1
    for i in range(len(set_of_its)):
        for j in range(i + 1, len(set_of_its)):
            # need join_three_itemsets that will join three itemsets that are in positon i and j
            it_out = join_three_itemsets(set_of_its[i], set_of_its[j], order)
            if len(it_out) > 0:
                C.append(it_out)
    return C


def from_iterable(iterables):
    for it in iterables:
        for element in it:
            yield element


def powerset(s):
    # create all combination from 1 to size of itemsets
    return list(from_iterable(create_Combinations(s, r) for r in range(1, len(s) + 1)))


# to print out the rules
def print_rules(X, X_S, S, conf, supp, lift, num_trans):
    print('{0:<25} -> {1:^9} | Support:{2:^5} | Confidence:{3:>2} | Lift:{4:>2}'.format(' , '.join(list(S)), ' , '.join(
        list(X_S)) , str(round(supp / num_trans, 2) * 100) + '%', str(round(conf,1) * 100) + '%',round(lift,2)))


check_Support = False
# checking whether user entered input in correct format for support value
while not check_Support:
    try:
        support_value = float(input('What min support would you like? {Note:- Required % Value > 0 and <= 100} --->'))
        if support_value > 0 and support_value <= 100:
          check_Support = True # we only get here if the previous line didn't throw an exception
        else:
            print('Invalid value!')
    except ValueError:
        print ('Invalid value!')

# checking whether user entered input in correct format for confidence value
check_Conf = False
while not check_Conf:
    try:
        conf_value = float(input('What min confidence would you like? {Note:- Required % Value > 0 and <= 100} --->'))
        if conf_value > 0 and conf_value <= 100:
          check_Conf = True # we only get here if the previous line didn't throw an exception
        else:
            print('Invalid value!')
    except ValueError:
        print ('Invalid value!')


# path_to_data = "db1.txt"
print("Select the dataset:")
print("1 wmdb1")
print("2 wmdb2")
print("3 wmdb3")
print("4 wmdb4")
print("5 wmdb5")

path_to_data = ""
check_data = False
# checking whether user entered input in correct format for database int value
while not check_data:
    try:
        database = int(input("Enter any integer from 1 to 5:- "))
        if database > 0 and database <6:
          check_data = True # we only get here if the previous line didn't throw an exception
        else:
            print('Invalid value!')
    except ValueError:
        print ('Invalid value!')

if database == 1:
    path_to_data = "../../../csv/database/wmdb1.txt"
elif database == 2:
    path_to_data = "../../../csv/database/wmdb2.txt"
elif database == 3:
    path_to_data = "../../../csv/database/wmdb3.txt"
elif database == 4:
    path_to_data = "../../../csv/database/wmdb4.txt"
elif database == 5:
    path_to_data = "../../../csv/database/wmdb5.txt"
else:
    print('Error')


min_support = support_value / 100
print(min_support)
order = load_orders()
order = sorted(order, key=lambda s: s.casefold())

Transactions = load_transactions(path_to_data, order)


print('\n Items \n')
num=1
for x in order:
    print(num,' '+str(x))
    num+=1

print('\nTransactions')
for x in Transactions:
    print(str(x))



min_conf = conf_value / 100
num_trans = len(Transactions)


# making a dictionary for the set of candidates and frequent item sets
C = {}
L = {}
itemset_size = 1
# start with an empty list since it will be updated by the value returned by function
Discarded = {itemset_size: []}
# doing iteration over the size of the item set starting with the size of 1 and putting all the candidates of size 1
C.update({itemset_size: [[f] for f in order]})


supp_count_L = {}
f, sup, new_discarded = get_frequent(C[itemset_size], Transactions, min_support, Discarded)


# update the variable with generated outputs , which will give real set of discarded item sets from the first iteration
Discarded.update({itemset_size: new_discarded})
L.update({itemset_size: f})
supp_count_L.update({itemset_size: sup})

# print('L1: \n')
# print_table(L[1], supp_count_L[1])

# Apriori.py general idea
# generate on each iteration the set of itemsets of size K C[k], to get the candidates, after that we generate frequent item set L[k]
# after that we count using the helper function, the algorithm stops when L[k] is empty and continues if it is > 1
# each iteration depends on the size of the item sets
# loop starts with size of 2 so k = itemset_size + 1
print('-----------------------------')
print('Starting Apriori.py Approach')
print('-----------------------------')
start_apriori = time.time()
k = itemset_size + 1
convergence = False
while not convergence:
    # generating the candidates for iteration K using helper function
    C.update({k: join_set_itemsets(L[k - 1], order)})
    # print('Table C{}: \n'.format(k))
    # counting occurrences of each itemsets and list of transaction looping over itemsets
    # print_table(C[k], [count_occurrences(it, Transactions) for it in C[k]])
    # generate L after C using helper function
    f, sup, new_discarded = get_frequent(C[k], Transactions, min_support, Discarded)
    # update L, Discarded , support
    Discarded.update({k: new_discarded})
    L.update({k: f})
    supp_count_L.update({k: sup})
    # check if L is empty
    if len(L[k]) == 0:
        convergence = True
    else:
        pass
        #print('Table L{}: \n'.format(k))
        #print_table(L[k], supp_count_L[k])
    k += 1

end_apriori = time.time()
# by the end of the above while loop  we will have all the candidates of each itemsets for each iteration


rule_counter = 0

# Generating the Association rules according to the combination and than calculating the confidence and support
# loop over item set of size 2
for i in range(1, len(L)):
    # loop over that itemset
    for j in range(len(L[i])):
        # powerset returns all the subsets that can be produced
        s = powerset(set(L[i][j]))
        # get rid of the last item which is a subset that contains all the items
        s.pop()
        # going over each element in the subset
        for z in s:
            # set S
            S = set(z)
            # set produced by  itemset
            X = set(L[i][j])
            # set of the difference
            X_S = set(X - S)
            # support for X
            sup_x = count_occurrences(X, Transactions)
            # support for X - S
            sup_x_s = count_occurrences(X_S, Transactions)
            # calculate confidence
            conf =  sup_x / count_occurrences(S, Transactions)
            # lift
            lift = conf / (sup_x_s / num_trans)
            if conf >= min_conf and sup_x >= min_support:
                rule_counter += 1

                # found an association
                #print_rules(X, X_S, S, conf, sup_x, lift, num_trans)

if rule_counter == 0:
    print('No Association Rules found from apriori method')
else:
    print('Association rules generated with Apriori.py',rule_counter)

print('Time taken with Apriori.py Approach',round(end_apriori - start_apriori,4))

'''
Brute Force Implementation 
'''

# getting all the unique candidates from the transactions and returning it
def get_C1(Transactions):
    C1 = []
    for itemsets in Transactions:
        for item in itemsets:
            if not [item] in C1:
                C1.append([item])
    # sorting the candidates
    C1.sort()
    return C1

def check_SupportConditions(Transactions, freq_sets, min_support= min_support):
    freq_set = []
    no_Of_Items = float(len(Transactions))
    for group_Of_Set in freq_sets:
        for each_set in group_Of_Set:
            counter = 0
            for each_Transaction in Transactions:
                # checking for the items if it is in freq_sets and in each transaction
                if [item for item in each_set if item in each_Transaction] == each_set:
                    counter = counter + 1
            # checking for the threshold value given by user
            if counter / no_Of_Items >= min_support:
                freq_set.append(each_set)

    return freq_set

# generates all possible frequent item sets
def create_AllFrequent_Set(freq_sets, C1):
    for i in range(len(C1) - 1):
        freq_sets.append([])
        for curr_L in freq_sets[i]:
            for item in C1:
                # putting single element in to the list
                if type(curr_L) is int:
                    current_List = list([curr_L])
                else:
                    current_List = curr_L.copy()
                # checking the last item
                if item[-1] > current_List[-1]:
                    current_List.append(item[-1])
                    freq_sets[i + 1].append(current_List)

                del current_List
    return freq_sets



print('-----------------------------')
print('Starting Brute Force Approach')
print('-----------------------------')

start_bf = time.time()
C1 = get_C1(Transactions)
freq_sets = []
freq_sets.append(C1)
freq_sets = create_AllFrequent_Set(freq_sets, C1)
freq_set = check_SupportConditions(Transactions, freq_sets)
end_bf = time.time()


# getting the unique length of item set from frequent sets
length = []
for item in freq_set:
    length.append(len(item))
unique_length = set(length)

# creating frequent set dictionary to store values for different item set length
bf_L = {}
unique_length = list(unique_length)
for item in range(1, (len(unique_length) + 2)):
    index = item
    bf_L[index] = []

# appending all the values at specific index in the dictionary
for item in unique_length:
    index = item
    for values in freq_set:
        if len(values) == item:
            bf_L[index].append(values)
        else:
            continue

# variable to count no of rules generated
rule_counter_bf = 0

# Generating the Association rules for brute force approach
# loop over item set of size 2
for i in range(1, len(bf_L)):
    # loop over that item set
    for j in range(len(bf_L[i])):
        # power set returns all the subsets that can be produced
        s = powerset(set(bf_L[i][j]))
        # get rid of the last item which is a subset that contains all the items
        s.pop()
        # going over each element in the subset
        for z in s:
            # set S
            S = set(z)
            # set produced by  item set
            X = set(bf_L[i][j])
            # set of the difference
            X_S = set(X - S)
            # support for X
            sup_x = count_occurrences(X, Transactions)
            # support for X - S
            sup_x_s = count_occurrences(X_S, Transactions)
            # calculate confidence
            conf = sup_x / count_occurrences(S, Transactions)
            # lift
            lift = conf / (sup_x_s / num_trans)
            if conf >= min_conf and sup_x >= min_support:
                rule_counter_bf += 1
                # found an association
                #print_rules(X, X_S, S, conf, sup_x, lift, num_trans)

if rule_counter_bf == 0:
    print('No Association Rules found from Brute Force method')
else:
    print('Association rules generated with Brute Force',rule_counter_bf)

print('Time taken with Brute Force Approach', round(end_bf - start_bf,4))