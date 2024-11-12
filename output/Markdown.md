# Markdown

**Markdown**[^9] is a [lightweight markup language](https://en.wikipedia.org/wiki/Lightweight_markup_language) for creating [formatted text](https://en.wikipedia.org/wiki/Formatted_text) using a [plain-text editor](https://en.wikipedia.org/wiki/Text_editor). [John Gruber](https://en.wikipedia.org/wiki/John_Gruber) created Markdown in 2004 as an easy-to-read [markup language](https://en.wikipedia.org/wiki/Markup_language)[^9]. Markdown is widely used for [blogging](https://en.wikipedia.org/wiki/Blog) and [instant messaging](https://en.wikipedia.org/wiki/Instant_messaging), and also used elsewhere in [online forums](https://en.wikipedia.org/wiki/Online_forums), [collaborative software](https://en.wikipedia.org/wiki/Collaborative_software), [documentation](https://en.wikipedia.org/wiki/Documentation) pages, and [readme files](https://en.wikipedia.org/wiki/README).

The initial description of Markdown[^10] contained ambiguities and raised unanswered questions, causing implementations to both intentionally and accidentally diverge from the original version. This was addressed in 2014 when long-standing Markdown contributors released [CommonMark](https://en.wikipedia.org/wiki/CommonMark), an unambiguous specification and test suite for Markdown[^11].

## History

Markdown was inspired by pre-existing [conventions](https://en.wikipedia.org/wiki/Convention_(norm)) for marking up [plain text](https://en.wikipedia.org/wiki/Plain_text) in [email](https://en.wikipedia.org/wiki/Email) and [usenet](https://en.wikipedia.org/wiki/Usenet) posts,[^12] such as the earlier markup languages [setext](https://en.wikipedia.org/wiki/Setext) (c. 1992), [Textile](https://en.wikipedia.org/wiki/Textile_(markup_language)) (c. 2002), and [reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText) (c. 2002)[^9].

In 2002 [Aaron Swartz](https://en.wikipedia.org/wiki/Aaron_Swartz) created [atx](https://en.wikipedia.org/wiki/Atx_(markup_language)) and referred to it as "the true structured text format". Gruber created the Markdown language in 2004 with Swartz as his "sounding board"[^13]. The goal of language was to enable people "to write using an easy-to-read and easy-to-write plain text format, optionally convert it to structurally valid [XHTML](https://en.wikipedia.org/wiki/XHTML) (or [HTML](https://en.wikipedia.org/wiki/HTML))[^5].

Its key design goal was *readability*, that the language be readable as-is, without looking like it has been marked up with tags or formatting instructions,[^9] unlike text formatted with 'heavier' [markup languages](https://en.wikipedia.org/wiki/Markup_language), such as [Rich Text Format](https://en.wikipedia.org/wiki/Rich_Text_Format) (RTF), HTML, or even [wikitext](https://en.wikipedia.org/wiki/Wikitext) (each of which have obvious in-line tags and formatting instructions which can make the text more difficult for humans to read).

Gruber wrote a [Perl](https://en.wikipedia.org/wiki/Perl) script, `Markdown.pl`, which converts marked-up text input to valid, [well-formed](https://en.wikipedia.org/wiki/XML#Well-formedness_and_error-handling) XHTML or HTML and replaces angle brackets (`<`, `>`) and [ampersands](https://en.wikipedia.org/wiki/Ampersand) (`&`) with their corresponding [character entity references](https://en.wikipedia.org/wiki/Character_entity_references). It can take the role of a standalone script, a plugin for [Blosxom](https://en.wikipedia.org/wiki/Blosxom) or a [Movable Type](https://en.wikipedia.org/wiki/Movable_Type) blog, or of a text filter for [BBEdit](https://en.wikipedia.org/wiki/BBEdit)[^5].

## Rise and divergence

As Markdown's popularity grew rapidly, many Markdown [implementations](https://en.wikipedia.org/wiki/Implementation) appeared, driven mostly by the need for additional features such as [tables](https://en.wikipedia.org/wiki/Table_(information)), [footnotes](https://en.wikipedia.org/wiki/Note_(typography)), definition lists,[^16] and Markdown inside HTML blocks.

The behavior of some of these diverged from the reference implementation, as Markdown was only characterised by an informal [specification](https://en.wikipedia.org/wiki/Specification_(technical_standard))[^17] and a [Perl](https://en.wikipedia.org/wiki/Perl) implementation for conversion to HTML.

At the same time, a number of ambiguities in the informal specification had attracted attention.[^18] These issues spurred the creation of tools such as Babelmark[^19][^20] to compare the output of various implementations,[^21] and an effort by some developers of Markdown [parsers](https://en.wikipedia.org/wiki/Parsing) for standardisation. However, Gruber has argued that complete standardization would be a mistake: "Different sites (and people) have different needs. No one syntax would make all happy"[^22].

Gruber avoided using curly braces in Markdown to unofficially reserve them for implementation-specific extensions[^23].

## Standardization

| Filename extensions         | Internet media type                 | Uniform Type Identifier (UTI)                | Developed by                        | Initial release      | Latest release        | Type of format        | Extended to                                     |
|-----------------------------|-------------------------------------|------------------------------------------------|-------------------------------------|----------------------|----------------------|-----------------------|-------------------------------------------------|
| .md, .markdown[^1][^2]     | text/markdown[^2]                  | net.daringfireball.markdown                 | John Gruber                        | March 9, 2004       | 1.0.1 December 17, 2004 | Open file format[^6] | pandoc, MultiMarkdown, Markdown Extra, CommonMark,[^7] RMarkdown[^8] |

## Variants

Websites like [Bitbucket](https://bitbucket.org), [Diaspora](https://diaspora.social), [GitHub](https://github.com)[^32] use variants of Markdown to make discussions between users easier.

Depending on implementation, basic inline [HTML tags](https://en.wikipedia.org/wiki/HTML_tag) may be supported.[^35] 

## Examples

| Text using Markdown syntax | Corresponding HTML produced by a Markdown processor           | Text viewed in a browser |
|---------------------------|---------------------------------------------------------------|---------------------------|
| Heading                    | `<h1>Heading</h1>`                                          | <h1>Heading</h1>         |
| Sub-heading                | `<h2>Sub-heading</h2>`                                      | <h2>Sub-heading</h2>     |
| Alternative heading        | `<h1>Alternative heading</h1>`                              | <h1>Alternative heading</h1> |
| Alternative sub-heading    | `<h2>Alternative sub-heading</h2>`                          | <h2>Alternative sub-heading</h2> |
| Paragraphs are separated by a blank line. Two spaces at the end of a line produce a line break. | `<p>Paragraphs are separated by a blank line.<br />Two spaces at the end of a line produce a line break.</p>` | Paragraphs are separated by a blank line.<br />Two spaces at the end of a line produce a line break. |

---

For the **image**:

![Markdown](https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Markdown-mark.svg/175px-Markdown-mark.svg.png)

### References

[^9]: Markdown Syntax Documentation  
[^10]: Daring Fireball – Markdown – Syntax  
[^11]: CommonMark specification  
[^12]: ArsTechnica - Markdown throwdown: What happens when FOSS software gets corporate backing?  
[^13]: Markdown: License  
[^1]: RFC 7763  
[^2]: RFC 7764  
[^6]: Daring Fireball: Introducing Markdown  
[^7]: Future of Markdown  
[^8]: GitHub Flavored Markdown  
[^32]: GitHub Flavored Markdown Examples  
[^35]: Markdown Text 101 (Chat Formatting)  
