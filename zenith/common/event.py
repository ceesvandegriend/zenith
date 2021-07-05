"""
events and listeners
"""

__listeners = dict()


def listeners(listener: str) -> list:
    '''
    Lists all the listeners or an empty list if there are none.

    :param listener: name of the listener
    :return: a list or an empty list
    '''
    if listener in __listeners:
        return __listeners[listener]
    return []


def append_listener(listener: str, function: object) -> None:
    '''
    Register a listener funtion.

    :param listener: name of the listener
    :param function: function to be called
    '''
    if not listener in __listeners:
        __listeners[listener] = []

    __listeners[listener].append(function)


def clear_listeners() -> None:
    '''
    Clears all the listeners.
    '''
    __listeners.clear()


def fire_listeners(listener: str, event) -> None:
    '''
    Fires all the listener functions.

    :param listener: name of the listener
    :param event: data fot the function
    '''
    for function in listeners(listener):
        function(event)
