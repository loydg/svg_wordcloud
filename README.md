# gh_pages
A simple hack to Andreas Mueller's https://amueller.github.io/word_cloud that produces SVG output while making the bare minimum changes to the code.

Some examples to demonstrate that it really does work. The output is produced by a modified version of [a_new_hope.py](https://github.com/amueller/word_cloud/blob/master/examples/a_new_hope.py) that prints out SVG in addition to the PNG. These fonts are from https://fonts.google.com. 

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
* Create environment *wordcloud*
* Activate environment *wordcloud*
* Install *matplotlib* and *wordcloud* modules
* modify *your_directory/anaconda3/envs/wordcloud/lib/python3.7/site-packages/wordcloud/wordcloud.py* as described below

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

The examples at the top of the page were produced with this script [svg_a_new_hope_net.py](put link here)
