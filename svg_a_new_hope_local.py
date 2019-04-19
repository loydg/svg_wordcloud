#!/usr/bin/env python
"""
Using custom colors
===================

Using the recolor method and custom coloring functions.
"""

import numpy as np
from PIL import Image
from os import path
import matplotlib.pyplot as plt
import os
import random

from wordcloud import WordCloud, STOPWORDS

from tempfile import NamedTemporaryFile
import urllib

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

# Adobe Illustrator doesn't recognize hsl(), so...
def RGB_grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "rgb({0}, {0}, {0})".format(random.randint(128, 255))

# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

github_mask_URL = 'https://github.com/amueller/word_cloud/blob/master/examples/stormtrooper_mask.png' + '?raw=true'
github_text_URL = 'https://github.com/amueller/word_cloud/blob/master/examples/a_new_hope.txt' + '?raw=true'

maskFILE = NamedTemporaryFile(delete=False, suffix='.png')
response = urllib.request.urlopen(github_mask_URL)
maskFILE.write(response.read())
maskFILE.close()

textFILE = NamedTemporaryFile(delete=False, suffix='.txt')
response = urllib.request.urlopen(github_text_URL)
textFILE.write(response.read())
textFILE.close()

fontFILE = '/usr/share/fonts/truetype/roboto-slab/RobotoSlab-Bold.ttf'
fontFamily = 'Roboto Slab'
fontWeight = 'Bold'

Height = 1028
Width = 1190
Background_Color = 'black'

# read the mask image 
mask = np.array(Image.open(maskFILE.name))
# movie script of "a new hope"
# http://www.imsdb.com/scripts/Star-Wars-A-New-Hope.html
# May the lawyers deem this fair use.
text = open(textFILE.name).read()

# pre-processing the text a little bit
text = text.replace("HAN", "Han")
text = text.replace("LUKE'S", "Luke")

# adding movie script specific stopwords
stopwords = set(STOPWORDS)
stopwords.add("int")
stopwords.add("ext")

'''
The background color could be set in the svg style element.

svg { background-color: YOUR_COLOR_HERE; }

But the entire browser page will be colored.
Using a colored rect makes the result match the png produced
by a_new_hope.py

'''
# https://www.w3.org/TR/css-fonts-3/#font-kerning-prop
# https://www.w3.org/TR/css-fonts-3/#font-variant-ligatures-prop
print ("""<svg width="{0}" height="{1}" xmlns="http://www.w3.org/2000/svg">
    <defs><style type="text/css">
    text {{font-family: '{2}'; font-weight: {3};
    font-kerning:none;
    font-variant-ligatures:none}}
    </style></defs>""".format(Width, Height, fontFamily, fontWeight))

# SVG background rectangle - not necessary if background is white.
print ("<rect width=\"100%\" height=\"100%\" fill=\"{}\"/>".format(Background_Color))

wc = WordCloud(max_words=1000, mask=mask, stopwords=stopwords, margin=10, font_path=fontFILE, color_func=RGB_grey_color_func, background_color=Background_Color, random_state=1).generate(text)

print ('</svg>')

plt.title("Custom colors")
plt.imshow(wc, interpolation="bilinear")
wc.to_file('a_new_hope_' + fontFamily.lower().replace(" ", "_") + '.png')
plt.axis("off")
plt.show()