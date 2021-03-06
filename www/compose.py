#! /usr/bin/env python2

import sys
import datetime
import types
from collections import OrderedDict

tabs = OrderedDict([
    ("Overview", OrderedDict([
        ("index",""),
    ])),
    ("Documentation", OrderedDict([
        ("news", "News"),
        ("migration", "Migration"),
        ("tutorial", "Tutorial"),
        ("herbstluftwm", "herbstluftwm(1)"),
        ("herbstclient", "herbstclient(1)"),
    ])),
    ("FAQ", OrderedDict([
        ("faq", "FAQ"),
    ])),
    ("Download", OrderedDict([
        ("download", "Download"),
    ])),
    ("Wiki", "http://wiki.herbstluftwm.org"),
])

page2tab = {
    'imprint': "Imprint and Privacy Policy",
}

filename = sys.argv[1]
name = filename.replace('-content.html', '')
toc = filename.replace('-content.html', '-toc.html')

windowtitle = "herbstluftwm"
for title, subpages in tabs.iteritems():
    if not isinstance(subpages, basestring):
        for fn, subtitle in subpages.iteritems():
            page2tab[fn] = title
            if not ("" == subtitle) and (name == fn):
                windowtitle = subtitle + " - herbstluftwm"


curtab = page2tab[name]

#====~===~=========~==
# Header
#====~===~=========~==
print """\
<html>
 <head>
  <link rel="stylesheet" href="main.css" type="text/css" />
  <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=UTF-8" />
  <title>{title}</title>
 </head>
 <body>
  <div id="frame">
   <div id="header">
    <div id="logoname">
     <img id="icon" src="herbstluftwm.svg"/>
     <div id="squeezeheader">
       <h1>herbstluftwm</h1>
       <div id="subheader">
        a manual tiling window manager for X
       </div>
     </div>
    </div>
   </div>""".format(title=windowtitle)

#====~===~=========~==
# Navigation bar
#====~===~=========~==

print """\
    <ul id="navigationbar">"""

for title, subpages in tabs.iteritems():
    classstring = "notab"
    if title == curtab:
        classstring = "curtab"
    if isinstance(subpages, basestring):
        trg = subpages
    else:
        trg = subpages.keys()[0] + ".html"
    print '<li class="{cls}"><a href="{target}">{title}</a></li>'.format(
        cls = classstring,
        target = trg,
        title = title)


print """\
    </ul>\
    <div class="tabbarseparator"></div>
"""

subpages = tabs.get(page2tab[name], OrderedDict([]))

if len(subpages) > 1:
    print '<div class="subpagebar">'
    for basename, title in subpages.iteritems():
        if basename == name:
            cls = "subpagecur subpage"
        else:
            cls = "subpage"
        print '<span class="{cls}">'.format(cls = cls)
        print '<a href="{url}">{title}</a></span>'.format(
            url = basename + ".html",title = title)
    print "</div>"



print """\
    <div id="content">\
"""

# possibly table of contents:
try:
	print open(toc).read()
except IOError:
	# no toc file
	print "<!-- no toc file present -->"
print open(filename).read()


print """\
    <div class="footer">
      Generated on {date}
     - <a href=\"imprint.html\">Imprint and Privacy Policy</a>
    </div>
""".format(date=datetime.datetime.now().strftime('%Y-%m-%d at %H:%M:%S %Z'))

#====~===~=========~==
# Footer
#====~===~=========~==
print """\
   </div>
  </div>
 </body>
</html>
"""

# vim: noet
