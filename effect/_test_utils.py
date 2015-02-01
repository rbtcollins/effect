"""Another sad little utility module."""

import traceback

from characteristic import attributes

from testtools.matchers import Equals


@attributes(['expected_tb', 'got_tb'])
class ReraisedTracebackMismatch(object):
    def describe(self):
        return ("The reference traceback:\n"
                + ''.join(self.expected_tb)
                + "\nshould match the tail end of the received traceback:\n"
                + ''.join(self.got_tb)
                + "\nbut it doesn't.")


@attributes(['expected'], apply_with_init=False)
class MatchesReraisedExcInfo(object):

    def __init__(self, expected):
        self.expected = expected

    def match(self, actual):
        valcheck = Equals(self.expected[1]).match(actual[1])
        if valcheck is not None:
            print "val doesn't match", valcheck
            return valcheck
        typecheck = Equals(self.expected[0]).match(actual[0])
        if typecheck is not None:
            print "type doesn't match", typecheck
            return typecheck
        expected = traceback.format_exception(*self.expected)
        new = traceback.format_exception(*actual)
        tail_equals = lambda a, b: a == b[-len(a):]
        if not tail_equals(expected[1:], new[1:]):
            return ReraisedTracebackMismatch(expected_tb=expected,
                                             got_tb=new)
