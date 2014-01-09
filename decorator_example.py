#!/usr/bin/python

from functools import wraps


''' Simple Decorator Example '''


class Present(object):

    def __init__(self):
        self.wrapped = False
        self.damaged_by_ups = True
        self.repaired_by_recipient = None

    @property
    def pretty(self):
        return self.wrapped and (
            not self.damaged_by_ups or self.repaired_by_recipient)


def bow_and_ribbon(present_func):
    def wrapped_present():
        p = present_func()
        p.wrapped = True
        p.repaired_by_recipient = True
        return p
    return wrapped_present


def new_present():
    return Present()

ugly_box = new_present()
print ugly_box.pretty  # False

pretty_gift = bow_and_ribbon(new_present)()
print pretty_gift.pretty  # True


''' Using the Actual Decorator Syntax '''


@bow_and_ribbon
def new_present_2():
    return Present()

prewrapped_gift = new_present_2()

print prewrapped_gift.pretty  # True


''' Complex Decorator Example '''


def require_password(password):
    def _check_password(f):
        @wraps(f)
        def _wrapper(*args, **kwargs):
            p = kwargs.get('password')
            if password == p:
                return f(*args, **kwargs)
            raise Exception('Be doomed forever.')
        return _wrapper
    return _check_password


@require_password('open_sesame')
def open_secret_door(password=None):
    return 'eternal_riches'


try:
    open_secret_door('blubber fish')  # Failed attempt
except Exception as e:
    print e

assert(open_secret_door(password='open_sesame') == 'eternal_riches')  # True
print 'I am rich now!'
