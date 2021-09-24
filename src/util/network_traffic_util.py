import json


def get_all_fs_bundle_requests(driver):
    return list(filter(lambda request: request.path == '/rec/bundle', driver.requests))


def is_product_added_evnt_present(requests, fruit):
    found = False

    for request in requests:
        data = json.loads(request.body)
        for evt in data['Evts']:
            args = evt['Args']
            if len(args) > 0 and args[0] == 'Product Added':
                prod_add_data = json.loads(args[1])
                if prod_add_data['displayName_str'] == fruit:
                    found = True
                break
        else:
            continue
        break
    return found


def is_user_going_to_market_evnt_present(requests):
    found = False

    for request in requests:
        data = json.loads(request.body)
        for evt in data['Evts']:
            args = evt['Args']
            if len(args) > 0 and args[0] == 'https://fruitshoppe.firebaseapp.com/#/market':
                found = True
                break
        else:
            continue
        break
    return found


def is_sequential_bundles(requests):
    seq = 1
    for request in requests:
        req_seq = request.params['Seq']
        if str(seq) != req_seq:
            return False
        seq += 1
    return True
