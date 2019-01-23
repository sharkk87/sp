s = 'Плиточный клей (кнауф knauf knuf) (5 10 20 25) кг'
s = ' '.join(s.split()).lower()
s = s.split(' ')

result = []
list_index = 0
check_bracket = False
for i in s:
    if i.startswith('('):
        check_bracket = True
        # print(list_index, i, check_bracket)
        result.append([])

    elif i.endswith(')'):
        # print(list_index, i, check_bracket)
        check_bracket = False

    if check_bracket and i.startswith('('):
        # print(list_index, i, check_bracket)
        result[list_index].append(i[1:])

    elif check_bracket:
        # print(list_index, i, check_bracket)
        result[list_index].append(i)

    elif i.endswith(')'):
        # print(list_index, i, check_bracket)
        result[list_index].append(i[:-1])

        list_index += 1

    else:
        # print(list_index, i, check_bracket)
        result.append(i)

        list_index += 1

print(result)
