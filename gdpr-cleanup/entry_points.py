def all_required_args_set(args, required, definitions) -> bool:
    """
    Check that all requried args are set, print details on any missing.
    """
    set = True

    for arg in required:
        if not getattr(args, arg, False):
            print(('%s (%s) required, missing.' % (definitions.get(arg), arg)))
            set = False

    return set

def run_from_cli(func, description, definitions, required) -> None:
    """
    Entry point via command line.
    """
    import argparse
    import os
    import pprint

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    if os.path.exists(os.path.join(BASE_DIR, 'settings.py')):
        import settings
    else:
        settings = {}

    parser = argparse.ArgumentParser(description=description)

    for argname, helptext in list(definitions.items()):
        parser.add_argument(
            '--%s' % argname, dest=argname, help=helptext,
            default=getattr(settings, argname, False)
        )

    args = parser.parse_args()

    if all_required_args_set(args, required, definitions):
        pprint.PrettyPrinter(indent=2).pprint(func(args))

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def json_serial(obj):
    """JSON serializer for objects not serializable by default JSON code."""
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type %s not serializable." % type(obj))

def run_from_lamba(func, description, definitions, required, event) -> str:
    """
    Entry point from Amazom Lambda.
    """
    import json
    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    if os.path.exists(os.path.join(BASE_DIR, 'settings.py')):
        import settings
    else:
        settings = {}

    kwargs = event.get('kwargs', False)
    if kwargs:
        for argname in kwargs:
            event[argname] = kwargs.get(argname)

    for argname, helptext in list(definitions.items()):
        if not event.get(argname, False):
            event[argname] = getattr(settings, argname, False)

    args = Struct(**event)

    return json.dumps(func(args), default=json_serial)
