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

# dictionary of typefaces to play around with
theFonts = {
        'Roboto':['https://github.com/google/fonts/blob/master/apache/roboto/Roboto-Regular.ttf','https://fonts.googleapis.com/css?family=Roboto', '\'Roboto\''],
    
        'Roboto Slab':['https://github.com/googlefonts/robotoslab/blob/master/fonts/static/RobotoSlab-Regular.ttf','https://fonts.googleapis.com/css?family=Roboto+Slab', '\'Roboto Slab\', serif'],
     
        'Roboto Slab Bold':['https://github.com/googlefonts/robotoslab/blob/master/fonts/static/RobotoSlab-Bold.ttf','https://fonts.googleapis.com/css?family=Roboto+Slab:700', '\'Roboto Slab\', serif'],
        
        'Press Start 2p':['https://github.com/google/fonts/blob/master/ofl/pressstart2p/PressStart2P-Regular.ttf', 'https://fonts.googleapis.com/css?family=Press+Start+2P', '\'Press Start 2p\', cursive'],
           
        'Pacifico':['https://github.com/google/fonts/blob/master/ofl/pacifico/Pacifico-Regular.ttf', 'https://fonts.googleapis.com/css?family=Pacifico', '\'Pacifico\', cursive'],
            
        'Oswald':['https://github.com/google/fonts/blob/master/ofl/oswald/static/Oswald-Medium.ttf', 'https://fonts.googleapis.com/css?family=Oswald:500', '\'Oswald\', sans-serif'],
            
        'Black Ops One':['https://github.com/google/fonts/blob/master/ofl/blackopsone/BlackOpsOne-Regular.ttf', 'https://fonts.googleapis.com/css?family=Black+Ops+One', '\'Black Ops One\', cursive'],
            
        'Dokdo':['https://github.com/google/fonts/blob/master/ofl/dokdo/Dokdo-Regular.ttf', 'https://fonts.googleapis.com/css?family=Dokdo', '\'Dokdo\', cursive'],
            
        'Special Elite':['https://github.com/google/fonts/blob/master/apache/specialelite/SpecialElite-Regular.ttf', 'https://fonts.googleapis.com/css?family=Special+Elite', '\'Special Elite\', cursive'],
            
        'Iceland':['https://github.com/google/fonts/blob/master/ofl/iceland/Iceland-Regular.ttf', 'https://fonts.googleapis.com/css?family=Iceland', '\'Iceland\', cursive'],
           
        'Libre Barcode 39 Text':['https://github.com/google/fonts/blob/master/ofl/librebarcode39text/LibreBarcode39Text-Regular.ttf', 'https://fonts.googleapis.com/css?family=Libre+Barcode+39+Text', '\'Libre Barcode 39 Text\', cursive'],
    
        'Zilla Slab Highlight':['https://github.com/google/fonts/blob/master/ofl/zillaslabhighlight/ZillaSlabHighlight-Regular.ttf', 'https://fonts.googleapis.com/css?family=Zilla+Slab+Highlight', '\'Zilla Slab Highlight\', cursive'],
    
        'Zilla Slab Highlight Bold':['https://github.com/google/fonts/blob/master/ofl/zillaslabhighlight/ZillaSlabHighlight-Bold.ttf', 'https://fonts.googleapis.com/css?family=Zilla+Slab+Highlight:700', '\'Zilla Slab Highlight\', cursive'],
    
        'ZCOOL KuaiLe':['https://github.com/google/fonts/blob/master/ofl/zcoolkuaile/ZCOOLKuaiLe-Regular.ttf', 'https://fonts.googleapis.com/css?family=ZCOOL+KuaiLe', '\'ZCOOL KuaiLe\', cursive'],
    
        'Fredericka the Great':['https://github.com/google/fonts/blob/master/ofl/frederickathegreat/FrederickatheGreat-Regular.ttf', 'https://fonts.googleapis.com/css?family=Fredericka+the+Great', '\'Fredericka the Great\', cursive'],
    
        'Geo':['https://github.com/google/fonts/blob/master/ofl/geo/Geo-Regular.ttf', 'https://fonts.googleapis.com/css?family=Geo', '\'Geo\', sans-serif'],
    
        'Stalemate':['https://github.com/google/fonts/blob/master/ofl/stalemate/Stalemate-Regular.ttf', 'https://fonts.googleapis.com/css?family=Stalemate', '\'Stalemate\', cursive'],
    
        'Amita':['https://github.com/google/fonts/blob/master/ofl/amita/Amita-Regular.ttf', 'https://fonts.googleapis.com/css?family=Amita', '\'Amita\', cursive'],
    
        'Delius Unicase':['https://github.com/google/fonts/blob/master/ofl/deliusunicase/DeliusUnicase-Regular.ttf', 'https://fonts.googleapis.com/css?family=Delius+Unicase', '\'Delius Unicase\', cursive'],
    
        'Amatic SC':['https://github.com/google/fonts/blob/master/ofl/amaticsc/AmaticSC-Regular.ttf', 'https://fonts.googleapis.com/css?family=Amatic+SC', '\'Amatic SC\', cursive'],
    
        'Amatic SC Bold':['https://github.com/google/fonts/blob/master/ofl/amaticsc/AmaticSC-Bold.ttf', 'https://fonts.googleapis.com/css?family=Amatic+SC:700', '\'Amatic SC\', cursive'],
    
        'Raleway Dots':['https://github.com/google/fonts/blob/master/ofl/ralewaydots/RalewayDots-Regular.ttf', 'https://fonts.googleapis.com/css?family=Raleway+Dots', '\'Raleway Dots\', cursive'],
    
        'Lusitana':['https://github.com/google/fonts/blob/master/ofl/lusitana/Lusitana-Regular.ttf', 'https://fonts.googleapis.com/css?family=Lusitana', '\'Lusitana\', serif'],
    
        'Anton':['https://github.com/google/fonts/blob/master/ofl/anton/Anton-Regular.ttf', 'https://fonts.googleapis.com/css?family=Anton', '\'Anton\', sans-serif'],
    
        'Audiowide':['https://github.com/google/fonts/blob/master/ofl/audiowide/Audiowide-Regular.ttf', 'https://fonts.googleapis.com/css?family=Audiowide', '\'Audiowide\', cursive'],
    
        'Stalinist One':['https://github.com/google/fonts/blob/master/ofl/stalinistone/StalinistOne-Regular.ttf', 'https://fonts.googleapis.com/css?family=Stalinist+One', '\'Stalinist One\', cursive'],
            
        'Mountains of Christmas':['https://github.com/google/fonts/blob/master/apache/mountainsofchristmas/MountainsofChristmas-Bold.ttf', 'https://fonts.googleapis.com/css?family=Mountains+of+Christmas:700', '\'Mountains of Christmas\', cursive;font-weight:bold'],

        'Permanent Marker':['https://github.com/google/fonts/blob/master/apache/permanentmarker/PermanentMarker-Regular.ttf', 'https://fonts.googleapis.com/css?family=Permanent+Marker', '\'Permanent Marker\', cursive'],
    
        'Syncopate Bold':['https://github.com/google/fonts/blob/master/apache/syncopate/Syncopate-Bold.ttf', 'https://fonts.googleapis.com/css?family=Syncopate:700', '\'Syncopate\', sans-serif;font-weight:bold'],

        'Crushed':['https://github.com/google/fonts/blob/master/apache/crushed/Crushed-Regular.ttf', 'https://fonts.googleapis.com/css?family=Crushed', '\'Crushed\', cursive'],

        'WeePeople':['https://github.com/propublica/weepeople/blob/master/weepeople.ttf', 'You will have to figure out what goes here by refering to the demo at propublica/weepeople on github ', '\'WeePeople\''],
#        '':['', '', ''],
           }
'''
Stalinist One ttf file on github is not the same as the one
served by google fonts.
Black Ops One has a reported bug that affects uppercase "R"
https://github.com/google/fonts/issues/1131
'''
Typeface = 'Roboto'
github_font_URL = theFonts[Typeface][0] + '?raw=true'
google_font_URL = theFonts[Typeface][1]
google_font_family = theFonts[Typeface][2]

github_mask_URL = 'https://github.com/amueller/word_cloud/blob/master/examples/stormtrooper_mask.png' + '?raw=true'
github_text_URL = 'https://github.com/amueller/word_cloud/blob/master/examples/a_new_hope.txt' + '?raw=true'

fontFILE = NamedTemporaryFile(delete=False, suffix='.ttf')
response = urllib.request.urlopen(github_font_URL)
fontFILE.write(response.read())
fontFILE.close()

maskFILE = NamedTemporaryFile(delete=False, suffix='.png')
response = urllib.request.urlopen(github_mask_URL)
maskFILE.write(response.read())
maskFILE.close()

textFILE = NamedTemporaryFile(delete=False, suffix='.txt')
response = urllib.request.urlopen(github_text_URL)
textFILE.write(response.read())
textFILE.close()

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
    @import url("{2}");
    text {{font-family: {3};
    font-kerning:none;
    font-variant-ligatures:none}}
    </style></defs>""".format(Width, Height, google_font_URL, google_font_family))

# SVG background rectangle - not necessary if background is white.
print ("<rect width=\"100%\" height=\"100%\" fill=\"{}\"/>".format(Background_Color))

wc = WordCloud(max_words=1000, mask=mask, stopwords=stopwords, margin=10, font_path=fontFILE.name, color_func=grey_color_func, background_color=Background_Color, random_state=1).generate(text)

print ('</svg>')

plt.title("Custom colors")
plt.imshow(wc,interpolation="bilinear")
wc.to_file('a_new_hope_' + Typeface.lower().replace(" ", "_") + '.png')
plt.axis("off")
plt.show()