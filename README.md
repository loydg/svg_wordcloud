# SVG Word Cloud
A simple hack to Andreas Mueller's https://amueller.github.io/word_cloud that produces SVG output while making the bare minimum changes to the code.
## SVG Output Examples
Some examples to demonstrate that it really does work. The output is produced by a modified version of [a_new_hope.py](https://github.com/amueller/word_cloud/blob/master/examples/a_new_hope.py) that prints out SVG in addition to the PNG. Unless otherwise noted, the fonts are from https://fonts.google.com. I've tested the SVG files in Firefox, Chrome, and Safari on OSX, iOS POP!os(a variant of Ubuntu) and Windows and they worked ok. The comparison examples did not work in I.E. You can click within the svg and search for words - even on an iPhone (search within a webpage is located under the sharing button).

[oswald.svg](https://loydg.github.io/svg_wordcloud/examples/oswald.svg), 
[amatic_sc_bold.svg](https://loydg.github.io/svg_wordcloud/examples/amatic_sc_bold.svg), 
[zcool_kuaile.svg](https://loydg.github.io/svg_wordcloud/examples/zcool_kuaile.svg), 
[zilla_slab_highlight_bold.svg](https://loydg.github.io/svg_wordcloud/examples/zilla_slab_highlight_bold.svg), 
[libre_barcode_39_text.svg](https://loydg.github.io/svg_wordcloud/examples/libre_barcode_39_text.svg), 
[stalinist_one.svg](https://loydg.github.io/svg_wordcloud/examples/stalinist_one.svg), 
[black_ops_one.svg](https://loydg.github.io/svg_wordcloud/examples/black_ops_one.svg), 
[press_start_2p.svg](https://loydg.github.io/svg_wordcloud/examples/press_start_2p.svg)

stalinist_one.svg has an incorrect layout of words due to an error in the TTF font file in googles github repository that has been corrected in the version at https://fonts.google.com. I left it as is to show what can happen when there is a mismatch between the font file that generated the PNG and the font file that generates the SVG. It is corrected in the example below. Oddly, the Google github repository has two versions of Roboto Slab with slight differences in "g","k","K" and "R". Also, Black Ops One has a bug affecting "R" - it looks bad - but doesn't affect wordcloud layout.

This example uses a font from Propublica. https://github.com/propublica/weepeople

[weepeople.svg](https://loydg.github.io/svg_wordcloud/examples/weepeople.svg)

## Comparing SVG and PNG Output
Some more examples. This time the PNG output is generated with red text and the SVG output is generated with blue text. In an HTML file, the results are then stacked and the *mix-blend-mode* set to *multiply*. The two circles show the individual text colors and the resulting color when they overlap.

[Amatic SC Bold](https://loydg.github.io/svg_wordcloud/amatic_sc_bold_overlay.html), 
[Crushed](https://loydg.github.io/svg_wordcloud/crushed_overlay.html), 
[Mountains of Christmas](https://loydg.github.io/svg_wordcloud/mountains_of_christmas_overlay.html), 
[Permanent Marker](https://loydg.github.io/svg_wordcloud/permanent_marker_overlay.html), 
[Roboto Slab Bold](https://loydg.github.io/svg_wordcloud/roboto_slab_bold_overlay.html), 
[Stalinist One](https://loydg.github.io/svg_wordcloud/stalinist_one_overlay.html), 
[Syncopate Bold](https://loydg.github.io/svg_wordcloud/syncopate_bold_overlay.html),
[WeePeople](https://loydg.github.io/svg_wordcloud/weepeople_overlay.html)

In most cases the PNG and SVG match quite well. Generally, it seems that mismatches most commonly occur in the longer text strings, possibly because of accumulating error due to integer math. The WeePeople example has the most significant errors, but it is also a rather idiosyncratic typeface.

## How
When the code that generates the PNG writes a word to an image at (x,y) - (x,y) is the coordinate of the upper left bounding box of the rendered word. When SVG text is rendered to a screen at (x,y) - (x,y) is the coordinate of the start of the baseline of the rendered word. With some caveats, I wondered if that was the only significant difference between the two. So the first step was to transform (x,y) of the upper left bounding box of the text to (xSVG, ySVG) the coordinates of the text's baseline and see what it looked like. And the result was ok, but clearly not correct either.
And I thought that was possibly because the SVG rendered text in a more sophisticated manner. PNG code would write a word, "first" for example, as "f" glyph, "i" glyph, "r" glyph, "s" glyph, "t" glyph - and the SVG code would write a word to screen as "fi" ligature glyph, "r" glyph, "s" glyph, "t" glyph with kerning applied (and perhaps other transformations). And that's not easy to fix in the Python code. But it's trivial to fix in SVG in the style element - just turn it off to match what the PNG code does.

```html
text{
     font-kerning:none;
     font-variant-ligatures:none
    }
```

## Requirements/Steps
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

* Add this function - `to_svg()` - before `to_img()` (not that it has to be in that particular location - it's just where I placed it). 
* `to_svg()` prints the words in the layout as SVG to standard output - just the words not the opening/closing `<svg><style></style>...</svg>` elements.

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
## Script That Generated the Output Above
The examples at the top of the page were produced with this script - [svg_a_new_hope_net.py](https://github.com/loydg/svg_wordcloud/blob/master/svg_a_new_hope_net.py). 

It requires an internet connection. When run, it will download the required font, image mask, and text from github and output an SVG wordcloud using the Roboto typeface. So I'd suggest running it as:

```python svg_a_new_hope_net.py >roboto.svg```

The code contains a data structure containing data for several other typefaces. With the exception of the WeePeople typeface, the resulting output can be viewed by any web browser that has access to the internet - all the font information is accessed from Google Fonts. To produce the output for the overlay examples, modify the script as follows - set the background color to white, set the SVG text to blue and the PNG text to red. If the typeface the SVG uses is installed on your system, you will be able to open the SVG in Adobe Illustrator, Affinity Desiginer, or Inkscape.

## Generating the SVG with Fonts on Your Machine
If you want to produce output from font files on your machine, you can use [svg_a_new_hope_local.py](https://github.com/loydg/svg_wordcloud/blob/master/svg_a_new_hope_local.py). As is, it will produce an SVG wordcloud using bold weighted text from the Roboto Slab typeface, because the Ubuntu variant I tested it on happened to have the font file - /usr/share/fonts/truetype/roboto-slab/RobotoSlab-Bold.ttf. Just substitute appropriate values from your system for these lines:

```python
fontFILE = '/usr/share/fonts/truetype/roboto-slab/RobotoSlab-Bold.ttf'
fontFamily = 'Roboto Slab'
fontWeight = 'Bold'
```

And run the script similarly... ```python svg_a_new_hope_local.py>roboto_slab_bold.svg```

And remember that if your intention is to open the output in something like Adobe Illustrator, you must specify fonts that are in your system path or one of the other specific places that the application looks for font files, as opposed to some random folder where you may have squirreled away downloads.

## Opening the SVG in Vector Drawing Programs
The Output can be opened by Adobe Illustrator, Affinity Designer or Inkscape. There may be others but these are the ones that I am most familiar with. Inkscape is open source and free but is lacking in some of the text/character features you will need. Adobe Illustrator is expensive but works well with SVG in most cases. Affinity designer costs $50 - one time payment - no perpetual license fees and it actually works better with TrueType files than Adobe (so far, knock on wood). It has other oddities - sometimes SVG elements, for instance the background rectangles, are masked and you have to drag on a corner to unmask the element and make it visible. 

### BUT

Inkscape ignores the font-weight value set in the style element of the SVG. And you can't just box select all the text and change the font weight - you can't change one attribute of all the text elements. Instead it changes all the text to the same font size and weight. You could probably write a Python plugin to implement it. 

Adobe Illustrator and Affinity Designer both ignore the ligature and kerning settings. For both applications, you can box select all the text and set the kerning to 0. In Affinity Designer, you can turn off ligatures in the same panel that lets you zero out kerning. Adobe Illustrator allows you to turn off the ligatures for OpenType fonts but not TrueType fonts. So in Illustrator you have to do the clumsy work-around of box selecting the text, changing it to an OpenType font (Myriad Pro happens to be the first one that appears for me), turn off ligatures, then change the font back to the original TrueType font - Illustrator "remembers" the ligature settings. I didn't bother to investigate this in Inkscape - the font-weight issue was enough for me.

After opening ```roboto_slab_bold.svg``` in Inkscape and noting the font weight problem,  I transfered it to my Mac and opened it in Affinity Designer. Here's a [screenshot](https://github.com/loydg/svg_wordcloud/blob/master/affinity_designer_screenshot.png) (the red squiggles are spell-check warnings) Note the panel to the right with the various character/typeface settings.




