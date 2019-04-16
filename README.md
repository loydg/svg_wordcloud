# gh_pages
A single line was added to generate_from_text()
{% highlight python %}
self.to_svg()
{% endhighlight %}
{% highlight python %}
    def generate_from_text(self, text):
        """Generate wordcloud from text.

        The input "text" is expected to be a natural text. If you pass a sorted
        list of words, words will appear in your output twice. To remove this
        duplication, set ``collocations=False``.

        Calls process_text and generate_from_frequencies.

        ..versionchanged:: 1.2.2
            Argument of generate_from_frequencies() is not return of
            process_text() any more.

        Returns
        -------
        self
        """
        words = self.process_text(text)
        self.generate_from_frequencies(words)
        self.to_svg()
        return self
{% endhighlight %}

An extra function to_svg() was added and placed before to_img()

{% highlight python %}
    def to_svg(self):
        
        for (word, count), font_size, position, orientation, color in self.layout_:
            x = position[0]
            y = position[1]
            
            font = ImageFont.truetype(self.font_path, font_size)
                    
            ascent, descent = font.getmetrics()
            
            """
            from stackoverflow - doesn't seem to be according to PIL docs (should return height, width) but doesn't work otherwise...
            https://stackoverflow.com/questions/43060479/how-to-get-the-font-pixel-height-using-pil-imagefont
            """
            (getsize_width, baseline), (offset_x, offset_y) = font.font.getsize(word)
            
            """
            svg transform string - empty if no rotation (text horizontal), otherwise contains rotate and translate numbers
            """
            svgTransform = ""    
            
            svgFill = ' fill="{}"'.format(color)    
               
            """
            this is all it takes to transform x,y to svg space 
            """
            if orientation is None:
                svgX = y - offset_x
                svgY = x + ascent - offset_y      
                
            else:
                svgX = y + ascent - offset_y
                svgY = x + offset_x
                svgTransform = ' transform="rotate(-90, {}, {}) translate({}, 0)"'.format(svgX, svgY, -getsize_width)

            """
            print SVG to standard output 
            """
            print ('<text x="{}" y="{}" font-size="{}"{}{}>{}</text>'.format(svgX, svgY, font_size, svgTransform, svgFill, word))
    
{% endhighlight %}

Download a_new_hope.txt, stormtrooper_mask.png, and a_new_hope.py
The python script is modified to download the ttf file from google's github storage.

{% highlight python %}
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

"""
Used while figuring out text placement - was useful to 
highlight words by whether or not they had letters with
ascenders, descenders, or not, etc. The classification is
rough-and-ready because, for example, depending on the
typeface, letters such as uppercase Q and Z may have 
descenders.
"""
def red_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    ascenders = set('bdfhijkltABCDEDFGHIJKLMNOPQRSTUVWXYZ') 
    no_descenders = set('bdfhikltABCDEDFGHIJKLMNOPRSTUVWXYZ')
    descenders = set('gjpqy')
    color = "#000000"
    if not bool(set(word) & no_descenders):
        color = "#cc0000"        
    return color

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)


# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

# read the mask image taken from
# http://www.stencilry.org/stencils/movies/star%20wars/storm-trooper.gif
mask = np.array(Image.open(path.join(d, "stormtrooper_mask.png")))

# movie script of "a new hope"
# http://www.imsdb.com/scripts/Star-Wars-A-New-Hope.html
# May the lawyers deem this fair use.
text = open(path.join(d, 'a_new_hope.txt')).read()

# pre-processing the text a little bit
text = text.replace("HAN", "Han")
text = text.replace("LUKE'S", "Luke")

# adding movie script specific stopwords
stopwords = set(STOPWORDS)
stopwords.add("int")
stopwords.add("ext")

# dictionary of typefaces to play around with
theFonts = {
        'Roboto':['https://github.com/google/fonts/blob/master/apache/roboto/Roboto-Regular.ttf','https://fonts.googleapis.com/css?family=Roboto', '\'Roboto\''],
        
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

#        '':['', '', ''],
           }

Typeface = 'Roboto'
github_font_URL = theFonts[Typeface][0] + '?raw=true'
google_font_URL = theFonts[Typeface][1]
google_font_family = theFonts[Typeface][2]

fontFILE = NamedTemporaryFile(delete=False, suffix='.ttf')
response = urllib.request.urlopen(github_font_URL)
fontFILE.write(response.read())
fontFILE.close()

#should match dimensions of mask
Height = 1028
Width = 1190
Background_Color = 'white'

# Could also set the background this way
# but the entire browser page will be colored.
# Using a colored rect shows the size of your
# svg element - which is useful for some purposes
#svg { background-color: YOUR_COLOR_HERE; }

print ("""<svg width="{0}" height="{1}" xmlns="http://www.w3.org/2000/svg">
    <defs><style type="text/css">
    @import url("{2}");
    text {\{font-family: {3};
    font-variant-ligatures:none\}}
    </style></defs>""".format(Width, Height, google_font_URL, google_font_family))

# SVG background rectangle
print ("<rect width=\"100%\" height=\"100%\" fill=\"{}\"/>".format(Background_Color))

wc = WordCloud(max_words=1000, mask=mask, stopwords=stopwords, margin=10, font_path=fontFILE.name, color_func=red_color_func, background_color = Background_Color, random_state=1).generate(text)

print ('</svg>')

plt.title("Custom colors")
plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3),
           interpolation="bilinear")
wc.to_file("a_new_hope.png")
plt.axis("off")
plt.show()
{% endhighlight %}
