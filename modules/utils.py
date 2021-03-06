
"""
Provides essential utilites for the rest of TorBot app
"""
from queue import Queue
from threading import Thread
from requests.exceptions import HTTPError
import requests


# ALGORITHM UTILITY FUNCTIONS

def process_data(data_queue, process, args=tuple()):
    """
    Processes tasks using by grabbing threads from queue

    Args:
       data_queue (queue.Queue): contains tasks in FIFO data structure
       data_processor (function): function to be executed on task and args
       data_args (tuple): contains arguments for tasks
    Returns:
        None
    """
    while True:
        data = data_queue.get()
        if args:
            process(data, args)
        else:
            process(data)
        data_queue.task_done()


def multi_thread(data, data_function, args=tuple()):
    """
    Start threads with function to process data and arguments then process the data
    in FIFO order.

    Args:
        data (list): lists of values that you'd like to operate on
        data_function (function): function that you would like to use for processsing
        args (tuple): arguments for function
    Returns:
        None
    """
    data_queue = Queue(len(data)*2)
    for _ in data:
        if args:
            if isinstance(args, tuple):
                thd = Thread(target=process_data, args=(data_queue, data_function, args))
                thd.daemon = True
                thd.start()
            else:
                raise Exception('Arguments must be in the form of a tuple.')
        else:
            thd = Thread(target=process_data, args=(data_queue, data_function))
            thd.daemon = True
            thd.start()

    for data_obj in data:
        data_queue.put(data_obj)

    data_queue.join()

# Networking functions

def get_url_status(url, headers=False):
    """
    Uses GET request to check if website exists

    *NOTE: May look into changing this to HEAD requests to improve perf

    Args:
        url (str): url to be tested

    Return:
        something? (int/Response object): return value of the connection
        object's GET request if successful & zero upon failure
    """
    try:
        if headers:
            resp = requests.get(url, headers=headers)
        else:
            resp = requests.get(url)
        resp.raise_for_status()
        return resp
    except (ConnectionError, HTTPError):
        return 0
