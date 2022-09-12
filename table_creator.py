import pandas
def tables_to_exc(list,name='table'):
    map(list,list)
    dict = {f'{p}': [list[p]] for p in range(0, len(list))}
    print(dict)
    table = pandas.DataFrame.from_dict(data=dict, orient='columns')
    table.to_excel(f'{name}' + '.xlsx')