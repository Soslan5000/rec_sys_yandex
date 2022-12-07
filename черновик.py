d = {'b': 9, 'a': 3, 'c': 7, 'd':1, 'e':12}
sorted_tuple = sorted(d.items(), key=lambda x: x[1])
sorted_tuple.reverse()
sorted_tuple = dict(sorted_tuple)
# [('a', 3), ('c', 7), ('b', 9)]
# преобразовываем обратно в словарь
print(sorted_tuple)