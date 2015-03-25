# templatemaker #

Given a list of text files in a similar format, templatemaker creates a template that can extract data from files in that same format.

The library is written in Python, but the underlying longest-common-substring algorithm is implemented in C for performance.

## How to download ##

Go to the ["Downloads" page](http://code.google.com/p/templatemaker/downloads/list) and download the latest version, **0.1.1**.

Newer (but not necessarily stable) code is available via Subversion on the ["Source" page](http://code.google.com/p/templatemaker/source).

## Example usage ##

Here's a sample Python interactive interpreter session:

```
# Import the Template class.
>>> from templatemaker import Template

# Create a Template instance.
>>> t = Template()

# Learn a Sample String.
>>> t.learn('<b>this and that</b>')

# Output the template so far, using the "!" character to mark holes.
# We've only learned a single string, so the template has no holes.
>>> t.as_text('!')
'<b>this and that</b>'

# Learn another string. The True return value means the template gained
# at least one hole.
>>> t.learn('<b>alex and sue</b>')
True

# Sure enough, the template now has some holes.
>>> t.as_text('!')
'<b>! and !</b>'

# Learn another string. This time, the return value is False, which means
# the template didn't gain any holes.
>>> t.learn('<b>fine and dandy</b>')
False

# The template is the same as before.
>>> t.as_text('!')
'<b>! and !</b>'

# Now that we have a template, let's extract some data.
>>> t.extract('<b>red and green</b>')
('red', 'green')
>>> t.extract('<b>django and stephane</b>')
('django', 'stephane')

# The extract() method is very literal. It doesn't magically trim
# whitespace, nor does it have any knowledge of markup languages such as
# HTML.
>>> t.extract('<b>  spacy  and <u>underlined</u></b>')
('  spacy ', '<u>underlined</u>')

# The extract() method will raise the NoMatch exception if the data
# doesn't match the template. In this example, the data doesn't have the
# leading and trailing "<b>" tags.
>>> t.extract('this and that')
Traceback (most recent call last):
...
NoMatch
```

## Documentation ##

See [README.TXT](http://templatemaker.googlecode.com/svn/trunk/README.TXT) in the distribution for full documentation.

## Stability ##

The library is functional, but this is my first time writing C code since college. As such, it may or may not have buffer-overflow issues. I'm hoping a C expert will step in and audit the code.

Do not use this in a production setting just yet.

## Mailing list ##

The [mailing list](http://groups.google.com/group/templatemaker) is hosted by Google Groups.

## Academic stuff ##

Thanks to some kind contributors, I've learned that this sort of technology goes by several names in the academic community:

  * Wrapper induction ("wrapper" is a formal term for "screen scraper"). Every paper I've found about wrapper induction takes a "supervised" approach -- that is, it requires human-labeled input. My goal with templatemaker is to be entirely unsupervised.
  * Wrapper generation. (This seems to be a synonym for "wrapper induction.")
  * Information extraction (IE).
  * Template detection.

See [these search results](http://www.google.com/search?hl=en&q=+site:citeseer.ist.psu.edu+%22wrapper+induction%22) for hours of reading material.

## Credits ##

This code was written by [Adrian Holovaty](http://www.holovaty.com/) and originally released July 5, 2007.