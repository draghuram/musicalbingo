#!/usr/bin/env python

import sys

def genchits(titles, outf):
    import random
    num_chits = 48
    rows = 4
    cols = 3
    outf.write('<html><body>\n')
    for i in xrange(num_chits):
        entries = random.sample(titles, rows*cols)
        outf.write('<table cellpadding=5 border align=center valign=middle>')
        for j in range(rows):
            outf.write('<tr align=left>')
            for k in range(cols):
                outf.write('<td>[&nbsp;&nbsp]&nbsp;&nbsp;%s</td>' % entries.pop())
            outf.write('</tr>')
        outf.write('</table><br><br>')
    outf.write('</body><html>\n')

def genmlist(titles, outf):
    titles.sort()
    cols = 5
    outf.write('<html><body>\n')
    outf.write('<table border align=center>')
    while titles:
        outf.write('<tr align=left>')
        for k in range(cols):
            if titles:
                outf.write('<td>&nbsp;&nbsp;%s&nbsp;</td>' % titles.pop(0))
        outf.write('</tr>')
    outf.write('</table><br><br>')
    outf.write('</body><html>\n')

input_file = sys.argv[1]

with open("master_list.html", "wt") as master_f:
    genmlist(open(input_file).readlines(), master_f)

with open("chits.html", "wt") as chits_f:
    genchits(open(input_file).readlines(), chits_f)


