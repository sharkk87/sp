import re


s = 'Плиточный клей (кнауф knauf knuf) (5 10 20 25) кг'

# result = re.findall(r"\([^)]+\)", s)
# print(s)
# print(result)
#
# s_or = []
# s_and = []
# check = False
# for i in s:
#     if i == '(':
#         check = True
#         continue
#     elif i == ')':
#         check = False
#         continue
#
#     if not check:
#         s_and.append(i)
#
#
# print(''.join(s_and).split())
# s_and = ''.join(s_and).split()
#
# s_and_2 = ''
# for i in s_and:
#     s_and_2 += i + ' AND '
#
# print(s_and_2)
#
# s_or = []
# for i in result:
#     a = str(i)
#     a = a.replace('(', '')
#     a = a.replace(')', '')
#     b = a.split()
#     s_or.append(b)
#
# print(s_or)

# s = ' '.join(s.split()).lower()
# print(s)
#
s = s.split()
print(s)
result = []
brasket = False
count = 0
for i in s:
    if not brasket:
        result.append(i)
        count += 1

    if i.startswith('('):
        result.append(i[1:])
        brasket = True
        continue

    if i.endswith(')'):
        brasket = False
        result.append(i[:-1])
        continue
    elif brasket:
        result.append(i)

print(result)

# Формирование запроса для SQLAlchemy
# s = [['плит', 'клей'], ['кнауф', 'knauf', 'knuf'], ['20', '25'], 'кг']
#
# for i in s:
#     if isinstance(i, list):
#         for j in i:
#             print(j)

# [print(j) for i in s if isinstance(i, list) for j in i]







