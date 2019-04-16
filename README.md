# gh_pages
Hello World!

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
