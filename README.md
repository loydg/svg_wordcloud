# gh_pages
A simple hack to Andreas Mueller's https://amueller.github.io/word_cloud that produces SVG output while making the bare minimum changes to the code.

Some examples to demonstrate that it really does work. The output is produced by a modified version of [a_new_hope.py](https://github.com/amueller/word_cloud/blob/master/examples/a_new_hope.py) that prints out SVG in addition to the PNG. These fonts are from https://fonts.google.com. I've tested them in Firefox, Chrome, and Safari on OSX, iOS POP!os(a variant of Ubuntu) and Windows and they worked ok. You can click within the svg and search for words - even on an iPhone (search within a webpage is located under the sharing button).

[oswald.svg](https://loydg.github.io/gh_pages/examples/oswald.svg), 
[amatic_sc_bold.svg](https://loydg.github.io/gh_pages/examples/amatic_sc_bold.svg), 
[zcool_kuaile.svg](https://loydg.github.io/gh_pages/examples/zcool_kuaile.svg), 
[zilla_slab_highlight_bold.svg](https://loydg.github.io/gh_pages/examples/zilla_slab_highlight_bold.svg), 
[libre_barcode_39_text.svg](https://loydg.github.io/gh_pages/examples/libre_barcode_39_text.svg), 
[stalinist_one.svg](https://loydg.github.io/gh_pages/examples/stalinist_one.svg), 
[black_ops_one.svg](https://loydg.github.io/gh_pages/examples/black_ops_one.svg), 
[press_start_2p.svg](https://loydg.github.io/gh_pages/examples/press_start_2p.svg)

This example uses a font from Propublica. https://github.com/propublica/weepeople

[weepeople.svg](https://loydg.github.io/gh_pages/examples/weepeople.svg)

Some more examples. This time the PNG output is generated with red text and the SVG output is generated with blue text. In an HTML file, the results are then stacked and the *mix-blend-mode* set to *multiply*. The two circles show the individual text colors and the resulting color when they overlap.

[Amatic SC Bold](https://loydg.github.io/gh_pages/amatic_sc_bold_overlay.html), 
[Crushed](https://loydg.github.io/gh_pages/crushed_overlay.html), 
[Mountains of Christmas](https://loydg.github.io/gh_pages/mountains_of_christmas_overlay.html), 
[Permanent Marker](https://loydg.github.io/gh_pages/permanent_marker_overlay.html), 
[Roboto Slab Bold](https://loydg.github.io/gh_pages/roboto_slab_bold_overlay.html), 
[Stalinist One](https://loydg.github.io/gh_pages/stalinist_one_overlay.html), 
[Syncopate Bold](https://loydg.github.io/gh_pages/syncopate_bold_overlay.html),
[WeePeople](https://loydg.github.io/gh_pages/weepeople_overlay.html)

Requirements/Steps
* Install Anaconda with Python3 if you don't already have it
* Create environment *svgwordcloud*
* Activate environment *svgwordcloud*
* Install *matplotlib* and *wordcloud* modules
* modify *your_directory/anaconda3/envs/svgwordcloud/lib/python3.7/site-packages/wordcloud/wordcloud.py* as described below

Add a single line - `self.to_svg()` - to `generate_from_text()`.
Here is the complete code for `generate_from_text()`. The additional line is before the return call.

```python
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
```

Add this function - `to_svg()` - before `to_img()` (not that it has to be in that particular location - it's just where I placed it). 
`to_svg()` prints the words in the layout as SVG to standard output - just the words not the opening/closing `<svg><style></style>...</svg>` elements.

```python
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
            it was arrived at using the methods of computer graphics programmers
            https://twitter.com/erkaman2/status/1104105232034861056
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
    
```

The examples at the top of the page were produced with this script [svg_a_new_hope_net.py](https://github.com/loydg/gh_pages/blob/master/svg_a_new_hope_net.py). It requires an internet connection.

When run, it will output an SVG wordcloud using the Roboto typeface (after you close the image preview window). So I'd suggest running it as:

```python svg_a_new_hope_net.py >roboto.svg```

Several other typefaces can be chosen. With the exception of the WeePeople typeface, the resulting output can be viewed by any web browser that has access to the internet - all the font information is accessed from Google Fonts. To produce the output for the overlay examples, modify the script as follows - set the background color to white, set the SVG text to blue and the PNG text to red.

The Output can also be opened by Adobe Illustrator, Affinity Designer or Inkscape - **IF** you have the font installed on your machine. **BUT**...

Inkscape ignores the font-weight set in the SVG. You'd probably have to write a Python plugin to fix that. So if you're using Inkscape, only make wordclouds with normal weight fonts.

Adobe Illustrator and Affinity Designer both ignore the ligature and kernings settings. For both applications, you can box select all the text and set the kerning to 0; In Affinity Designer, you can turn off ligatures in the same panel that lets you zero out kerning. Adobe Illustrator allows you to turn off the ligatures for OpenType fonts but not TrueType fonts. So in Illustrator you have to do the clumsy work-around of box selecting the text, changing it to an OpenType font (Myriad Pro happens to be the first one that appears for me), turn off ligatures, then change the font back to the original TrueType font - Illustrator "remembers" the ligature settings. I don't know how Inkscape handles this - but I wouldn't expect much.

If you want to produce output from font files on your machine, you can use [svg_a_new_hope_local.py](https://github.com/loydg/gh_pages/blob/master/svg_a_new_hope_local.py). The machine(Ubuntu-ish) I tested it on had the following font file - /usr/share/fonts/truetype/roboto-slab/RobotoSlab-Bold.ttf.

So I would type ```python svg_a_new_hope_local.py>roboto_slab_bold.svg```

You will need to edit the font file location according to your machine. Also remember that if your intention is to open the output in something like Adobe Illustrator, you need to specify fonts that are in your system path or one of the other specific places that the application looks for font files, as opposed to some random folder where you may have squirreled away downloads.

In my case, I had the difficulties mentioned above when opening it in Inkscape, so I transfered it to my Mac and opened it in Affinity Designer. Here's a [screenshot](https://github.com/loydg/gh_pages/blob/master/affinity_designer_screenshot.png) (the red squiggels are spell-check warnings)




