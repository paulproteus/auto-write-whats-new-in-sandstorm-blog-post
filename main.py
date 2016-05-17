#!/usr/bin/python

import datetime
CHANGELOG_PATH = '/home/paulproteus/projects/sandstorm/CHANGELOG.md'
SANDSTORM_WEBSITE_PATH = '/home/paulproteus/projects/sandstorm-website/'
import subprocess

def main(now=None):
    if now is None:
        now = datetime.datetime.utcnow()
    today_string = now.strftime("%Y-%m-%d")
    print 'Today is', today_string
    print 'Looking for sandstorm-website posts ending in -whats-new.md...'
    matches, _ = subprocess.Popen(["git", "ls-files", "--", "_posts/*-whats-new.md"], stdout=subprocess.PIPE, cwd=SANDSTORM_WEBSITE_PATH).communicate()
    filenames = matches.strip().split()
    print 'Checking if this month has such a blog post...'
    this_month_string = now.strftime("%Y-%m")
    this_month_posts = [filename for filename in filenames if this_month_string in filename]
    if any(this_month_posts):
        print 'Yes! I will exit. If you want to run this with a different target month, provide it as argv[1].'
        return
    
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
---''' % (now.strftime("%B")))
        fd.write('\n\n')  # end the Jekyll front matter
        fd.write('\n\n'.join(keep_these_sections))  # add the content
    print ''
    print 'OK! Wrote a blog post to', output_path
    print ''
    print 'Go edit it, and save and commit it.'

if __name__ == '__main__':
    main()

