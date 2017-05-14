some_list = [('elephant', 461), ('', 283), ('b', 81), ('african', 69), ('asian', 67), ('animal', 64), ('c', 50), ('retrieved', 49), ('p', 45), ('trunk', 39), ('male', 39), ('specie', 38), ('may', 37), ('group', 36), ('one', 36), ('j', 35), ('family', 34), ('population', 33), ('africa', 32), ('female', 30), ('tusk', 30), ('sukumar', 30), ('pmid', 30), ('elephas', 29), ('year', 28), ('forest', 27), ('ivory', 27), ('shoshani', 26), ('ear', 26), ('r', 24), ('around', 24), ('known', 24), ('bull', 23), ('calf', 23), ('time', 23),]
print(len(some_list))
print()
# http://stackoverflow.com/a/4119142/4062341
lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]

l = lol(some_list,len(some_list)%8 )
for k in range(0, 8):
    # Create new threads
    print(l[k])
