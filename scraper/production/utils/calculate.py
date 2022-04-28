ETHER_VALUE = 10 ** 18


def cal_ether(wei):
    return wei / ETHER_VALUE


def cal_gas(tx):
    if (tx['inout'] == 1) | (tx['type'] == 'i'):
        return 0
    else:
        return tx['gasUsed'] * tx['gasPrice']


def cal_balance(balance, item):
    gas = cal_gas(item)
    delta = item['inout'] * item['value'] if item['status'] == 1 else 0
    return balance + delta - gas


def combine_normal_internal(txlist, txlistinternal):
    new_list = []
    i, j, balance = 0, 0, 0
    while i < len(txlist) & j < len(txlistinternal):
        if txlist[i]['timeStamp'] <= txlistinternal[j]['timeStamp']:
            new_list.append(txlist[i])
            new_list[-1]['balance'] = cal_balance(balance, txlist[i])
            i += 1
        else:
            new_list.append((txlistinternal[j]))
            new_list[-1]['balance'] = cal_balance(balance, txlistinternal[j])
            j += 1
        balance = new_list[-1]['balance']
    while i < len(txlist):
        new_list.append(txlist[i])
        new_list[-1]['balance'] = cal_balance(balance, txlist[i])
        balance = new_list[-1]['balance']
        i += 1
    while j < len(txlistinternal):
        new_list.append((txlistinternal[j]))
        new_list[-1]['balance'] = cal_balance(balance, txlistinternal[j])
        balance = new_list[-1]['balance']
        j += 1
    return new_list


def in_or_out(address, to_address):
    if (to_address == "") | (address.lower() == to_address.lower()):
        return 1
    else:
        return -1


def refine_tx(item, address, type_):
    return {
        'timeStamp': int(item['timeStamp']),
        'value': cal_ether(int(item['value'])),
        'from': item['from'],
        'to': item['to'],
        'inout': in_or_out(address, item['to']),
        'type': 'n' if type_ == 'txlist' else 'i',
        'gasUsed': int(item['gasUsed']),
        'gasPrice': None if type_ == 'txlistinternal' else cal_ether(int(item['gasPrice'])),
        'status': 0 if int(item['isError']) == 1 else 1
    }
