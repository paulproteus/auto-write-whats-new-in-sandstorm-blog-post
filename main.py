#!/usr/bin/python

import datetime
import sys
CHANGELOG_PATH = '/home/paulproteus/projects/sandstorm/CHANGELOG.md'
SANDSTORM_WEBSITE_PATH = '/home/paulproteus/projects/sandstorm-website/'
import subprocess

def main(now=None, search_now=None):
    if now is None:
        now = datetime.datetime.utcnow()
    if search_now is None:
        search_now = datetime.datetime.utcnow()
    today_string = now.strftime("%Y-%m-%d")
    search_now_string = search_now.strftime("%Y-%m-%d")
    print 'Today is', today_string
    print 'Searching for posts as if it were', search_now_string
    print 'Looking for sandstorm-website posts ending in -whats-new.md...'
    matches, _ = subprocess.Popen(["git", "ls-files", "--", "_posts/*-whats-new.md"], stdout=subprocess.PIPE, cwd=SANDSTORM_WEBSITE_PATH).communicate()
    filenames = matches.strip().split()
    print 'Checking if this month has such a blog post...'
    this_month_string = search_now.strftime("%Y-%m")
    this_month_posts = [filename for filename in filenames if this_month_string in filename]
    if any(this_month_posts):
        print 'Yes! Be careful!'
    
    print 'No! I will write one.'
    keep_these_sections = []
    
    for changelog_section in open(CHANGELOG_PATH).read().split('\n\n'):
        changelog_section = changelog_section.strip()
        if not (changelog_section.startswith('###')):
            print 'Got a weird changelog section, skipping it...', repr(changelog_section)
            continue
        if this_month_string in changelog_section:
            keep_these_sections.append(changelog_section)

    if not keep_these_sections:
        print 'Eek! No changelog sections found for this month. Bailing out now.'
        return

    print 'Found %d sections...' % (len(keep_these_sections),)
    
    output_path = SANDSTORM_WEBSITE_PATH + '_posts/' + today_string + '-whats-new.md'
    with open(output_path, 'w') as fd:
        fd.write('''---
layout: post
title: "%s changelog - what's new in Sandstorm"
author: Asheesh Laroia
authorUrl: https://github.com/paulproteus
---''' % (search_now.strftime("%B")))
        fd.write('\n\n')  # end the Jekyll front matter
        fd.write('\n\n'.join(keep_these_sections))  # add the content
    print ''
    print 'OK! Wrote a blog post to', output_path
    print ''
    print 'Go edit it, and save and commit it.'

if __name__ == '__main__':
    if len(sys.argv) >= 1:
        search_date = map(int, sys.argv[1].split('-'))
        search_now = datetime.date(search_date[0], search_date[1], search_date[2])
    else:
        search_now = None
    main(now=None, search_now=search_now)

