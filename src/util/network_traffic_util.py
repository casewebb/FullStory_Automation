import json
from typing import List

from seleniumwire import webdriver
from seleniumwire.request import Request


def get_all_fs_bundle_requests(driver: webdriver):
    return list(filter(lambda request: request.path == '/rec/bundle', driver.requests))


def is_product_added_evnt_present(requests: List[Request], fruit):
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


def is_user_going_to_market_evnt_present(requests: List[Request]):
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


def is_sequential_bundles(requests: List[Request]):
    seq = 1
    for request in requests:
        req_seq = request.params['Seq']
        if str(seq) != req_seq:
            return False
        if seq > 1:
            param_prev_bundle_time = request.params['PrevBundleTime']
            previous_bundle_response_bundle_time = json.loads(requests[requests.index(request) - 1].response.body)[
                'BundleTime']
            if param_prev_bundle_time != str(previous_bundle_response_bundle_time):
                return False
        seq += 1
    return True
