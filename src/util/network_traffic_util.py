import json
import time
from typing import List

from seleniumwire import webdriver
from seleniumwire.request import Request

MAX_RETRY = 15


# Retrieve all FS network requests from the Chrome session
def get_all_fs_bundle_requests(driver: webdriver):
    c = len(list(filter(lambda request: request.path == '/rec/bundle', driver.requests)))

    poll_c = 1
    while poll_c < MAX_RETRY:
        print('Waiting for new bundle to be present. (', poll_c, '/', MAX_RETRY, ')')
        req = list(filter(lambda request: request.path == '/rec/bundle', driver.requests))
        if len(req) > c:
            print('Found new bundle.')
            return req
        poll_c += 1
        time.sleep(1)

    raise Exception('No new bundle appeared within ' + str(MAX_RETRY) + ' seconds.')


# Check whether there is an existing bundle containing an event
# showing that the user has added a specific fruit to their cart
def is_product_added_evnt_present(requests: List[Request], fruit):
    for request in requests:
        data = json.loads(request.body)
        for evt in data['Evts']:
            args = evt['Args']
            if len(args) > 0 and args[0] == 'Product Added':
                prod_add_data = json.loads(args[1])
                if prod_add_data['displayName_str'] == fruit:
                    print('Validated event ', evt, ' for addition of ', fruit)
                    return True
    return False


# Check whether there is an existing bundle containing an event
# showing that the user has navigated to a given route
def is_user_going_to_route_evnt_present(requests: List[Request], route):
    for request in requests:
        data = json.loads(request.body)
        for evt in data['Evts']:
            args = evt['Args']
            if len(args) > 0 and args[0] == 'https://fruitshoppe.firebaseapp.com/#/' + route:
                print('Validated event ', evt, ' for navigation to ', route)
                return True
    return False


# Validate the FS Order Completed event that should contain
# all carted fruits
def is_order_completed_evnt_present(requests: List[Request], fruits):
    for request in requests:
        data = json.loads(request.body)
        for evt in data['Evts']:
            args = evt['Args']
            if len(args) > 0 and args[0] == 'Order Completed':
                prod_add_data = json.loads(args[1])['products_objs']
                found = 0
                for fruit in prod_add_data:
                    if fruit['name_str'] in fruits:
                        found += 1
                if found == len(fruits):
                    print('Validated event ', evt, ' for order completion with fruits ', str(fruits))
                    return True
    return False


def is_sequential_bundles(requests: List[Request]):
    print('Validating all bundles sent sequentially with chained bundle times.')
    seq = 1
    for request in requests:
        req_seq = request.params['Seq']
        if str(seq) != req_seq:
            return False
        if seq == 1:
            param_prev_bundle_time = request.params['PrevBundleTime']
            print('Bundle Seq ', seq, ' - PreviousBundleTime Found in Request Param : ', param_prev_bundle_time,
                  ' - BundleTime From Previous Bundle Response : N/A')
        else:
            param_prev_bundle_time = request.params['PrevBundleTime']
            previous_bundle_response_bundle_time = json.loads(requests[requests.index(request) - 1].response.body)[
                'BundleTime']
            if param_prev_bundle_time != str(previous_bundle_response_bundle_time):
                return False
            print('Bundle Seq ', seq, ' - PreviousBundleTime Found in Request Param : ',
                  param_prev_bundle_time,
                  ' - BundleTime From Previous Bundle Response : ',
                  previous_bundle_response_bundle_time)
        seq += 1
    return True
