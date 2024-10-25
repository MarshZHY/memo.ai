fewshots= (open('quote.txt', 'r',encoding="UTF-8").readlines())
x = []
for _ in fewshots:
    if _ not in x:
        x.append(_)
    else:
        pass
print(len(x),len(fewshots))
open('quote.txt', 'w',encoding="UTF-8").write("".join(x))