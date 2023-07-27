import time

'''
Apriori  
'''

def create_Combinations(iterable, combination_size):
    group = tuple(iterable)
    tuple_size = len(group)


    if combination_size > tuple_size:
        return

    indexes = list(range(combination_size))

    yield tuple(group[i] for i in indexes)
    while True:
        for i in reversed(list(range(combination_size))):
            if indexes[i] != i + tuple_size - combination_size:

                break
        else:

            return
        indexes[i] += 1
        for j in list(range(i + 1, combination_size)):
            indexes[j] = indexes[j - 1] + 1
        yield tuple(group[i] for i in indexes)


def load_transactions(path_to_data, order):
    Transactions = []

    with open(path_to_data, 'r') as fid:

        for lines in fid:
            str_line = list(lines.strip().split(', '))
            while ("" in str_line):
                str_line.remove("")
            str_line.sort(key=lambda x: order.index(x))
            Transactions.append(str_line)

    return Transactions


def load_orders():
    Transactions = []
    with open(path_to_data) as fid:
        for lines in fid:
            str_line = list(lines.strip().split(', '))
            Transactions.append(str_line)
    order = []
    for j in Transactions:
        for i in j:
            order.append(i)
    order = list(set(order))
    order.sort()
    while ("" in order):
        order.remove("")
    return order


def get_frequent(itemsets, Transactions, min_support, prev_discarded):
    L = []
    supp_count = []
    new_discarded = []
    num_trans = len(Transactions)
    k = len(prev_discarded.keys())

    for s in range(len(itemsets)):
        discarded_before = False

        if k > 0:
            for it in prev_discarded[k]:
                if set(it).issubset(set(itemsets[s])):
                    discarded_before = True
                    break

        if not discarded_before:
            count = count_occurrences(itemsets[s], Transactions)
            if count / num_trans >= min_support:
                L.append(itemsets[s])
                supp_count.append(count)
            else:
                new_discarded.append(itemsets[s])
    return L, supp_count, new_discarded


def count_occurrences(itemset, Transactions):
    count = 0
    for i in range(len(Transactions)):
        if set(itemset).issubset(set(Transactions[i])):
            count += 1
    return count


def print_table(T, supp_count):
    print("Itemset | Frequency")
    for k in range(len(T)):
        print("{}:  {}".format(T[k], supp_count[k]))

    print('\n')


def join_two_itemsets(it1, it2, order):
    it1.sort(key=lambda x: order.index(x))
    it2.sort(key=lambda x: order.index(x))

    for i in range(len(it1) - 1):
        if it1[i] != it2[i]:
            return []

    if order.index(it1[-1]) < order.index(it2[-1]):
        return it1 + [it2[-1]]

    return []


def join_set_itemsets(set_of_its, order):
    C = []
    for i in range(len(set_of_its)):
        for j in range(i + 1, len(set_of_its)):
            it_out = join_two_itemsets(set_of_its[i], set_of_its[j], order)
            if len(it_out) > 0:
                C.append(it_out)
    return C


def from_iterable(iterables):
    for it in iterables:
        for element in it:
            yield element


def powerset(s):
    return list(from_iterable(create_Combinations(s, r) for r in range(1, len(s) + 1)))


def print_rules(X, X_S, S, conf, supp, lift, num_trans):
    print('{0:<25} -> {1:^9} | Support:{2:^5} | Confidence:{3:>2} | Lift:{4:>2}'.format(' , '.join(list(S)), ' , '.join(
        list(X_S)) , str(round(supp / num_trans, 2) * 100) + '%', str(round(conf,1) * 100) + '%',round(lift,2)))


check_Support = False
while not check_Support:
    try:
        support_value = float(input('What min support would you like? {Note:- Required % Value > 0 and <= 100} --->'))
        if support_value > 0 and support_value <= 100:
          check_Support = True
        else:
            print('Invalid value!')
    except ValueError:
        print ('Invalid value!')

check_Conf = False
while not check_Conf:
    try:
        conf_value = float(input('What min confidence would you like? {Note:- Required % Value > 0 and <= 100} --->'))
        if conf_value > 0 and conf_value <= 100:
          check_Conf = True
        else:
            print('Invalid value!')
    except ValueError:
        print ('Invalid value!')


print("Select the dataset:")
print("1 wmdb1")
print("2 wmdb2")
print("3 wmdb3")
print("4 wmdb4")
print("5 wmdb5")
print("6 wmdb6")

path_to_data = ""
check_data = False
while not check_data:
    try:
        database = int(input("Enter any integer from 1 to 6:- "))
        if database > 0 and database <7:
          check_data = True
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
elif database == 6:
    path_to_data = "../../../csv/database/wmdb6.csv"
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


C = {}
L = {}
itemset_size = 1
Discarded = {itemset_size: []}
C.update({itemset_size: [[f] for f in order]})


supp_count_L = {}
f, sup, new_discarded = get_frequent(C[itemset_size], Transactions, min_support, Discarded)


Discarded.update({itemset_size: new_discarded})
L.update({itemset_size: f})
supp_count_L.update({itemset_size: sup})


print('-----------------------------')
print('William Duggan begins Apriori test')
print('-----------------------------')
start_apriori = time.time()
k = itemset_size + 1
convergence = False
while not convergence:
    C.update({k: join_set_itemsets(L[k - 1], order)})
    f, sup, new_discarded = get_frequent(C[k], Transactions, min_support, Discarded)
    Discarded.update({k: new_discarded})
    L.update({k: f})
    supp_count_L.update({k: sup})
    if len(L[k]) == 0:
        convergence = True
    else:
        pass
    k += 1

end_apriori = time.time()


rule_counter = 0

for i in range(1, len(L)):
    for j in range(len(L[i])):
        s = powerset(set(L[i][j]))
        s.pop()
        for z in s:
            S = set(z)
            X = set(L[i][j])
            X_S = set(X - S)
            sup_x = count_occurrences(X, Transactions)
            sup_x_s = count_occurrences(X_S, Transactions)
            conf =  sup_x / count_occurrences(S, Transactions)
            lift = conf / (sup_x_s / num_trans)
            if conf >= min_conf and sup_x >= min_support:
                rule_counter += 1


if rule_counter == 0:
    print('No Association rules found using Apriori')
else:
    print('Association rules generated with Apriori',rule_counter)

print('Time taken using Apriori',round(end_apriori - start_apriori,4))

'''
Brute Force  
'''

def get_C1(Transactions):
    C1 = []
    for itemsets in Transactions:
        for item in itemsets:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return C1

def check_SupportConditions(Transactions, freq_sets, min_support= min_support):
    freq_set = []
    no_Of_Items = float(len(Transactions))
    for group_Of_Set in freq_sets:
        for each_set in group_Of_Set:
            counter = 0
            for each_Transaction in Transactions:
                if [item for item in each_set if item in each_Transaction] == each_set:
                    counter = counter + 1
            if counter / no_Of_Items >= min_support:
                freq_set.append(each_set)

    return freq_set

def create_AllFrequent_Set(freq_sets, C1):
    for i in range(len(C1) - 1):
        freq_sets.append([])
        for curr_L in freq_sets[i]:
            for item in C1:
                if type(curr_L) is int:
                    current_List = list([curr_L])
                else:
                    current_List = curr_L.copy()
                if item[-1] > current_List[-1]:
                    current_List.append(item[-1])
                    freq_sets[i + 1].append(current_List)

                del current_List
    return freq_sets



print('-----------------------------')
print('William Duggan begins Brute Force test')
print('-----------------------------')

start_bf = time.time()
C1 = get_C1(Transactions)
freq_sets = []
freq_sets.append(C1)
freq_sets = create_AllFrequent_Set(freq_sets, C1)
freq_set = check_SupportConditions(Transactions, freq_sets)
end_bf = time.time()


length = []
for item in freq_set:
    length.append(len(item))
unique_length = set(length)

bf_L = {}
unique_length = list(unique_length)
for item in range(1, (len(unique_length) + 2)):
    index = item
    bf_L[index] = []

for item in unique_length:
    index = item
    for values in freq_set:
        if len(values) == item:
            bf_L[index].append(values)
        else:
            continue

rule_counter_bf = 0

for i in range(1, len(bf_L)):
    for j in range(len(bf_L[i])):
        s = powerset(set(bf_L[i][j]))
        s.pop()
        for z in s:
            S = set(z)
            X = set(bf_L[i][j])
            X_S = set(X - S)
            sup_x = count_occurrences(X, Transactions)
            sup_x_s = count_occurrences(X_S, Transactions)
            conf = sup_x / count_occurrences(S, Transactions)
            lift = conf / (sup_x_s / num_trans)
            if conf >= min_conf and sup_x >= min_support:
                rule_counter_bf += 1

if rule_counter_bf == 0:
    print('No Association rules found using Brute Force method')
else:
    print('Association rules generated with Brute Force',rule_counter_bf)

print('Time taken using Brute Force', round(end_bf - start_bf,4))