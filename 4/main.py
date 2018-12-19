#!/usr/bin/env pypy3

from kitchen_sink import *

import re
import datetime
import sys

r = re.compile(r'\[([0-9]+)-([0-9]+)-([0-9]+) ([0-9]+):([0-9]+)\] (.+)')

class Event:
    def __init__(self, year, month, day, hour, minute, description):
        self.when = datetime.datetime(int(year), int(month), int(day),
                                      int(hour), int(minute))
        self.guard = None
        if description.startswith('Guard'):
            assert(description.split()[2:] == ['begins', 'shift'])
            self.guard = int(description.split()[1][1:])
            self.what = 'begins-shift'
        elif description == 'falls asleep':
            self.what = 'falls-asleep'
        elif description == 'wakes up':
            self.what = 'wakes-up'
        else:
            raise Exception("Don't know what to do with %s" % description)
    def __repr__(self):
        return "<%s> %s %s" % (self.what, self.when, self.guard)

def parse_event(line):
    result = r.match(line.strip())
    return Event(*result.groups())

def total_sleep(lst):
    return sum(l[1] - l[0] for l in lst)

def process_intervals(lst):
    lst.sort()
    lst_2 = (list((v[0], 'start', v) for v in lst) +
             list((v[1], 'end', v) for v in lst[::-1]))
    lst_2.sort(key=lambda l: l[0])

    argmax_minute = None
    max_minute = -100
    current_count = 0
    current_minute = -1
    for event in lst_2:
        current_minute = event[0]
        if event[1] == 'start':
            current_count += 1
        elif event[1] == 'end':
            current_count -= 1
        if current_count > max_minute:
            argmax_minute = current_minute
            max_minute = current_count
    return argmax_minute, max_minute
    
if __name__ == '__main__':
    events = list(parse_event(l) for l in input_lines())
    events.sort(key=lambda l: l.when)
    current_guard = None
    current_state = None
    sleep_start = None
    d = {}
    for event in events:
        if event.what == 'begins-shift':
            current_guard = event.guard
        elif event.what == 'falls-asleep':
            current_state = 'asleep'
            sleep_start = event.when
        elif event.what == 'wakes-up':
            current_state = 'awake'
            guard = current_guard
            total = (event.when - sleep_start).total_seconds()

            d.setdefault(guard, []).append([sleep_start.minute, event.when.minute]) #
            sleep_start = None
    
    most_frequent_asleep_minute = dict((k, process_intervals(v)) for (k, v) in d.items())

    print(most_frequent_asleep_minute)
    the_guard = argmax(most_frequent_asleep_minute, by=lambda v: v[1])
    print(the_guard)
    print(the_guard[0] * the_guard[1][0])

    # print("Guard: %s" % the_guard)
    # argmax_minute = 
    # print(the_guard, argmax_minute, the_guard * argmax_minute)
    
    
