# Markdown

> For the marketing term, see [Price markdown](https://en.wikipedia.org/wiki/Price_markdown).

**Markdown** is a [lightweight markup language](https://en.wikipedia.org/wiki/Lightweight_markup_language) for creating [formatted text](https://en.wikipedia.org/wiki/Formatted_text) using a [plain-text editor](https://en.wikipedia.org/wiki/Text_editor). [John Gruber](https://en.wikipedia.org/wiki/John_Gruber) created Markdown in 2004 as an easy-to-read [markup language](https://en.wikipedia.org/wiki/Markup_language). Markdown is widely used for [blogging](https://en.wikipedia.org/wiki/Blog) and [instant messaging](https://en.wikipedia.org/wiki/Instant_messaging), and also used elsewhere in [online forums](https://en.wikipedia.org/wiki/Online_forums), [collaborative software](https://en.wikipedia.org/wiki/Collaborative_software), [documentation](https://en.wikipedia.org/wiki/Documentation) pages, and [readme files](https://en.wikipedia.org/wiki/README).

The initial description of Markdown contained ambiguities and raised unanswered questions, causing implementations to both intentionally and accidentally diverge from the original version. This was addressed in 2014 when long-standing Markdown contributors released [CommonMark](https://en.wikipedia.org/wiki/CommonMark), an unambiguous specification and test suite for Markdown.

| **Filename extensions** | `.md`, `.markdown` |
| **Internet media type** | `text/markdown` |
| **Uniform Type Identifier (UTI)** | `net.daringfireball.markdown` |
| **Developed by** | [John Gruber](https://en.wikipedia.org/wiki/John_Gruber) |
| **Initial release** | March 9, 2004 |
| **Latest release** | 1.0.1, December 17, 2004 |
| **Type of format** | [Open file format](https://en.wikipedia.org/wiki/Open_file_format) |
| **Extended to** | [pandoc](https://en.wikipedia.org/wiki/Pandoc), [MultiMarkdown](https://en.wikipedia.org/wiki/MultiMarkdown), [Markdown Extra](https://en.wikipedia.org/wiki/Markdown_Extra), [CommonMark](https://en.wikipedia.org/wiki/CommonMark), [RMarkdown](https://en.wikipedia.org/wiki/RMarkdown) |
| **Website** | [daringfireball.net/projects/markdown](https://daringfireball.net/projects/markdown/) |

## History

Markdown was inspired by pre-existing [conventions](https://en.wikipedia.org/wiki/Convention_(norm)) for marking up [plain text](https://en.wikipedia.org/wiki/Plain_text) in [email](https://en.wikipedia.org/wiki/Email) and [usenet](https://en.wikipedia.org/wiki/Usenet) posts, such as the earlier markup languages [setext](https://en.wikipedia.org/wiki/Setext) (c. 1992), [Textile](https://en.wikipedia.org/wiki/Textile_(markup_language)) (c. 2002), and [reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText) (c. 2002).

In 2002, [Aaron Swartz](https://en.wikipedia.org/wiki/Aaron_Swartz) created [atx](https://en.wikipedia.org/wiki/Atx_(markup_language)) and referred to it as "the true structured text format". Gruber created the Markdown language in 2004 with Swartz as his "sounding board". The goal of language was to enable people "to write using an easy-to-read and easy-to-write plain text format, optionally convert it to structurally valid [XHTML](https://en.wikipedia.org/wiki/XHTML) (or [HTML](https://en.wikipedia.org/wiki/HTML))".

Its key design goal was *readability*, that the language be readable as-is, without looking like it has been marked up with tags or formatting instructions, unlike text formatted with 'heavier' markup languages, such as [Rich Text Format](https://en.wikipedia.org/wiki/Rich_Text_Format) (RTF), HTML, or even [wikitext](https://en.wikipedia.org/wiki/Wikitext) (each of which have obvious in-line tags and formatting instructions which can make the text more difficult for humans to read).

Gruber wrote a [Perl](https://en.wikipedia.org/wiki/Perl) script, `Markdown.pl`, which converts marked-up text input to valid, [well-formed](https://en.wikipedia.org/wiki/XML#Well-formedness_and_error-handling) XHTML or HTML and replaces angle brackets (`<`, `>`) and [ampersands](https://en.wikipedia.org/wiki/Ampersand) (`&`) with their corresponding [character entity references](https://en.wikipedia.org/wiki/Character_entity_reference). It can take the role of a standalone script, a plugin for [Blosxom](https://en.wikipedia.org/wiki/Blosxom) or a [Movable Type](https://en.wikipedia.org/wiki/Movable_Type), or of a text filter for [BBEdit](https://en.wikipedia.org/wiki/BBEdit).

## Rise and divergence

As Markdown's popularity grew rapidly, many Markdown [implementations](https://en.wikipedia.org/wiki/Implementation) appeared, driven mostly by the need for additional features such as [tables](https://en.wikipedia.org/wiki/Table_(information)), [footnotes](https://en.wikipedia.org/wiki/Note_(typography)), definition lists, and Markdown inside HTML blocks.

The behavior of some of these diverged from the reference implementation, as Markdown was only characterized by an informal [specification](https://en.wikipedia.org/wiki/Specification_(technical_standard)) and a [Perl](https://en.wikipedia.org/wiki/Perl) implementation for conversion to HTML. At the same time, a number of ambiguities in the informal specification had attracted attention. These issues spurred the creation of tools such as Babelmark to compare the output of various implementations, and an effort by some developers of Markdown [parsers](https://en.wikipedia.org/wiki/Parsing) for standardization. However, Gruber has argued that complete standardization would be a mistake: "Different sites (and people) have different needs. No one syntax would make all happy."

Gruber avoided using curly braces in Markdown to unofficially reserve them for implementation-specific extensions.

## Standardization

| CommonMark |
| **Filename extensions** | `.md`, `.markdown` |
| **Internet media type** | `text/markdown; variant=CommonMark` |
| **Uniform Type Identifier (UTI)** | uncertain |
| **Developed by** | [John MacFarlane](https://en.wikipedia.org/wiki/John_MacFarlane_(philosopher)), open source |
| **Initial release** | October 25, 2014 |
| **Latest release** | 0.30, June 19, 2021 |
| **Type of format** | [Open file format](https://en.wikipedia.org/wiki/Open_file_format) |
| **Extended from** | Markdown |
| **Extended to** | GitHub Flavored Markdown |

From 2012, a group of people, including [Jeff Atwood](https://en.wikipedia.org/wiki/Jeff_Atwood) and [John MacFarlane](https://en.wikipedia.org/wiki/John_MacFarlane_(philosopher)), launched what Atwood characterised as a standardization effort. A community website now aims to "document various tools and resources available to document authors and developers, as well as implementors of the various Markdown implementations".

In September 2014, Gruber objected to the usage of "Markdown" in the name of this effort and it was rebranded as CommonMark. CommonMark.org published several versions of a specification, reference implementation, test suite, and plans to announce a finalized 1.0 spec and test suite in 2019. No 1.0 spec has since been released as major issues still remain unsolved. Nonetheless, the following websites and projects have adopted CommonMark: [Discourse](https://en.wikipedia.org/wiki/Discourse_(software)), [GitHub](https://en.wikipedia.org/wiki/GitHub), [GitLab](https://en.wikipedia.org/wiki/GitLab), [Reddit](https://en.wikipedia.org/wiki/Reddit), [Qt](https://en.wikipedia.org/wiki/Qt_(software)), [Stack Exchange](https://en.wikipedia.org/wiki/Stack_Exchange) (Stack Overflow), and [Swift](https://en.wikipedia.org/wiki/Swift_(programming_language)).

In March 2016, two relevant informational Internet [RFCs](https://en.wikipedia.org/wiki/Request_for_Comments) were published:

- RFC [7763](https://datatracker.ietf.org/doc/html/rfc7763) introduced [MIME](https://en.wikipedia.org/wiki/MIME) type `text/markdown`.

- RFC [7764](https://datatracker.ietf.org/doc/html/rfc7764) discussed and registered the variants MultiMarkdown, GitHub Flavored Markdown (GFM), Pandoc, and Markdown Extra among others.

## Variants

Websites like [Bitbucket](https://en.wikipedia.org/wiki/Bitbucket), [Diaspora](https://en.wikipedia.org/wiki/Diaspora_(social_network)), [GitHub](https://en.wikipedia.org/wiki/GitHub), [OpenStreetMap](https://en.wikipedia.org/wiki/OpenStreetMap), [Reddit](https://en.wikipedia.org/wiki/Reddit), and [SourceForge](https://en.wikipedia.org/wiki/SourceForge) use variants of Markdown to make discussions between users easier.

Depending on implementation, basic inline [HTML tags](https://en.wikipedia.org/wiki/HTML_tag) may be supported. Italic text may be implemented by `_underscores_` or `*single-asterisks*`.

### GitHub Flavored Markdown

GitHub had been using its own variant of Markdown since as early as 2009, which added support for additional formatting such as tables and nesting [block content](https://en.wikipedia.org/wiki/HTML_element#Block_elements) inside list elements, as well as GitHub-specific features such as auto-linking references to commits, issues, usernames, etc.

In 2017, GitHub released a formal specification of its GitHub Flavored Markdown (GFM) that is based on CommonMark. It is a [strict superset](https://en.wikipedia.org/wiki/Superset) of CommonMark, following its specification exactly except for tables, [strikethrough](https://en.wikipedia.org/wiki/Strikethrough), [autolinks](https://en.wikipedia.org/wiki/Automatic_hyperlinking), and task lists, which GFM adds as extensions.

### Markdown Extra

Markdown Extra is a [lightweight markup language](https://en.wikipedia.org/wiki/Lightweight_markup_language) based on Markdown implemented in [PHP](https://en.wikipedia.org/wiki/PHP) (originally), [Python](https://en.wikipedia.org/wiki/Python_(programming_language)), and [Ruby](https://en.wikipedia.org/wiki/Ruby_(programming_language)). It adds the following features that are not available with regular Markdown:

- Markdown markup inside [HTML](https://en.wikipedia.org/wiki/HTML) blocks

- Elements with id/class attribute

- "Fenced code blocks" that span multiple lines of code

- Tables

- Definition lists

- Footnotes

- Abbreviations

Markdown Extra is supported in some [content management systems](https://en.wikipedia.org/wiki/Content_management_system) such as [Drupal](https://en.wikipedia.org/wiki/Drupal), [Grav](https://en.wikipedia.org/wiki/Grav_(CMS)), and [TYPO3](https://en.wikipedia.org/wiki/TYPO3).

### LiaScript

LiaScript is a Markdown dialect that was designed to create interactive educational content. It is implemented in [Elm](https://en.wikipedia.org/wiki/Elm_(programming_language)) and [TypeScript](https://en.wikipedia.org/wiki/TypeScript) and adds additional syntax elements to define features like:

- Animations

- Automatic speech output

- Mathematical formulas (using [KaTeX](https://en.wikipedia.org/wiki/KaTeX))

- ASCII art diagrams

- Various types of quizzes and surveys

- JavaScript is natively supported and can be attached to various elements, making code fragments executable and editable.

## Examples

| Text using Markdown syntax | Corresponding HTML produced by a Markdown processor | Text viewed in a browser |
| Heading | `<h1>Heading</h1>` | <h1>Heading</h1> |
| Sub-heading | `<h2>Sub-heading</h2>` | <h2>Sub-heading</h2> |
| Alternative heading | `<h1>Alternative heading</h1>` | <h1>Alternative heading</h1> |
| Alternative sub-heading | `<h2>Alternative sub-heading</h2>` | <h2>Alternative sub-heading</h2> |
| Paragraphs are separated by a blank line. | `<p>Paragraphs are separated by a blank line.</p>` | <p>Paragraphs are separated by a blank line.</p> |
| Two spaces at the end of a line produce a line break. | `<p>Two spaces at the end of a line<br />produce a line break.</p>` | <p>Two spaces at the end of a line<br />produce a line break.</p> |
| Bullet lists nested within numbered list: | `<ol><li>fruits<ul><li>apple</li><li>banana</li></ul></li><li>vegetables<ul><li>carrot</li><li>broccoli</li></ul></li></ol>` | <ol><li>fruits<ul><li>apple</li><li>banana</li></ul></li><li>vegetables<ul><li>carrot</li><li>broccoli</li></ul></li></ol> |
| A [link](http://example.com). | `<p>A <a href="http://example.com">link</a>.</p>` | <p>A <a rel="nofollow" class="external text" href="http://example.com/">link</a>.</p> |
| ![Image](Icon-pictures.png) | `<p><img alt="Image" src="Icon-pictures.png" /></p>` | <p><span class="mw-default-size" typeof="mw:File"><span title="image"><img alt="Image" src="//upload.wikimedia.org/wikipedia/commons/5/5c/Icon-pictures.png" decoding="async" width="65" height="59" class="mw-file-element" data-file-width="65" data-file-height="59" /></span></span></p> |

## Implementations

Implementations of Markdown are available for over a dozen [programming languages](https://en.wikipedia.org/wiki/Programming_language); in addition, many [applications](https://en.wikipedia.org/wiki/Application_software), platforms, and [frameworks](https://en.wikipedia.org/wiki/Software_framework) support Markdown.

### Some examples of applications supporting Markdown:

- [Bugzilla](https://en.wikipedia.org/wiki/Bugzilla): uses a customized version of Markdown.

- [ChatGPT](https://en.wikipedia.org/wiki/ChatGPT): Output from the LLM formatted in Markdown will be rendered in LaTeX and HTML by the ChatGPT client, and the model is encouraged to use Markdown to format its output.

- [Discord](https://en.wikipedia.org/wiki/Discord_(software)): chat messages.

- [Discourse](https://en.wikipedia.org/wiki/Discourse_(software)): uses the CommonMark flavor of Markdown in the forum post composer.

- [Doxygen](https://en.wikipedia.org/wiki/Doxygen): a source code documentation generator which supports Markdown with extra features.

- [GitHub](https://en.wikipedia.org/wiki/GitHub): Flavored Markdown (GFM) ignores underscores in words, and adds syntax highlighting, task lists.

## See also

- [Comparison of document markup languages](https://en.wikipedia.org/wiki/Comparison_of_document_markup_languages)

- [Comparison of documentation generators](https://en.wikipedia.org/wiki/Comparison_of_documentation_generators)

- [Lightweight markup language](https://en.wikipedia.org/wiki/Lightweight_markup_language)

- [Wiki markup](https://en.wikipedia.org/wiki/Wiki_markup)

## Explanatory notes

Technically HTML description lists.