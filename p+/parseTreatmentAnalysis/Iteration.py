""" A generic module to encapsulate iteration of a data set that also traps the StopIteration and
returns None instead."""


def iteration_generator(collection):
    """ Create a generator object to iterate over a collection.

    Args:
        collection:  Any collection object that can be iterated over.

    Returns:
        A generator object that can be used to control iteration of a series of objects in a collection.
    """
    for item in collection:
        yield item


def next_item(generator):
    """ Get the next item in a generator, while hiding the StopIteration Error and return None instead.

    Args:
        generator:  A generator object that will yield the objects of a collection.

    Returns:
        Successive items in the list of the collection. None if the collection has completed yielding items.
    """
    try:
        item = next(generator)
        return item
    except StopIteration as e:
        return None

