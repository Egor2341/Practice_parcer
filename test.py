# import re
# a = "dfadsfadfa<adfafdsaf/>adfadfas"
# pattern = re.compile('<.*?>')
# a = re.sub(pattern, ' ', a)
# print(a)

salary = {'from': 10000, 'to': 120000, 'currency': 'RUR', 'gross': False}
res = ''
if salary["from"]:
    res += f"от {salary['from']} "
if salary["to"]:
    res += f"до {salary['to']} "
res += salary["currency"]
res = res.capitalize()
print(res)