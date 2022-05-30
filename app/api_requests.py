import json
import threading

import requests


class ThreadWithReturnValue(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
        self._target = target
        self._args = args
        self._kwargs = kwargs

    def run(self):
        try:
            if self._target:
                self._return = self._target(*self._args, **self._kwargs)
        finally:
            del self._target, self._args, self._kwargs

    def join(self, timeout=None):
        threading.Thread.join(self, timeout)

        return self._return


def get_name():
    try:
        response = requests.get("http://random-data-api.com/api/name/random_name")
        if response:
            try:
                full_name = json.loads(response.text)
                first_name = full_name["first_name"]
                last_name = full_name["last_name"]
                return first_name, last_name
            except Exception:
                return "Without name", "Without surname"
    except requests.exceptions.RequestException:
        return "Without name", "Without surname"


def get_address():
    try:
        address = requests.get("https://random-data-api.com/api/address/random_address")
        if address:
            return address.json()
    except requests.exceptions.RequestException:
        return "No address"


def get_one_coffee():
    try:
        response = requests.get("https://random-data-api.com/api/coffee/random_coffee")
        if response:
            try:
                coffee_response = json.loads(response.text)
                coffee = dict()
                coffee["title"] = coffee_response["blend_name"]
                coffee["origin"] = coffee_response["origin"]
                coffee["notes"] = coffee_response["notes"].split(",")
                coffee["intensifier"] = coffee_response["intensifier"]
                return coffee
            except:
                return None

    except requests.exceptions.RequestException:
        return None


def get_result_set(target, length: int):
    threads = []
    for _ in range(length):
        thread = ThreadWithReturnValue(target=target)
        thread.start()
        threads.append(thread)

    result_set = [thread.join() for thread in threads]

    return result_set
