#!/home/nicholasc/anaconda2/bin/python

import json
import sys
import collections

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--base_file', type=str)
parser.add_argument('--other_file', type=str)
args = parser.parse_args()

base_file = args.base_file
other_file = args.other_file

# base_file = '/home/nicholasc/projects/allensdk/dev.json'
# later_file = '/home/nicholasc/projects/allensdk/ABS-129.json'

base_report = json.load(open(base_file, 'r'))
other_report = json.load(open(other_file, 'r'))

summary_dict = {}
for key, val in other_report['report']['summary'].iteritems():
    summary_dict[key] = base_report['report']['summary'][key] - val

for key, val in summary_dict.iteritems():
    print '%s:' % key, val

difference_dict = collections.defaultdict(list)
for curr_base_test, curr_later_test in zip(base_report['report']['tests'],
                                           other_report['report']['tests']):
    base_outcome = curr_base_test['outcome']
    other_outcome = curr_later_test['outcome']

    if base_outcome != other_outcome:
        difference_dict[base_outcome, other_outcome].append(
                (curr_base_test, curr_later_test))

for key, val in difference_dict.iteritems():
    if len(val) > 0:
        print 'base:%s other:%s' % key

        for curr_difference_tuple in difference_dict[key]:
            assert (curr_difference_tuple[0]['name'] ==
                    curr_difference_tuple[1]['name'])
            print '    ', curr_difference_tuple[0]['name']
            for curr_difference in curr_difference_tuple:
                if curr_difference['outcome'] == 'failed':
                    print '<<<<<<<<<<'
                    print curr_difference['call']['longrepr']
                    print '>>>>>>>>>>'
        print
