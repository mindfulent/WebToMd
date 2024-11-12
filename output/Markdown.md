# Markdown

**Markdown**[^9] is a [lightweight markup language](https://en.wikipedia.org/wiki/Lightweight_markup_language) for creating [formatted text](https://en.wikipedia.org/wiki/Formatted_text) using a [plain-text editor](https://en.wikipedia.org/wiki/Text_editor). [John Gruber](https://en.wikipedia.org/wiki/John_Gruber) created Markdown in 2004 as an easy-to-read [markup language](https://en.wikipedia.org/wiki/Markup_language)[^9]. Markdown is widely used for [blogging](https://en.wikipedia.org/wiki/Blog) and [instant messaging](https://en.wikipedia.org/wiki/Instant_messaging), and also used elsewhere in [online forums](https://en.wikipedia.org/wiki/Online_forums), [collaborative software](https://en.wikipedia.org/wiki/Collaborative_software), [documentation](https://en.wikipedia.org/wiki/Documentation) pages, and [readme files](https://en.wikipedia.org/wiki/README).

The initial description of Markdown[^10] contained ambiguities and raised unanswered questions, causing implementations to both intentionally and accidentally diverge from the original version. This was addressed in 2014 when long-standing Markdown contributors released [CommonMark](#Standardization), an unambiguous specification and test suite for Markdown[^11].

## History

Markdown was inspired by pre-existing [conventions](https://en.wikipedia.org/wiki/Convention_(norm)) for marking up [plain text](https://en.wikipedia.org/wiki/Plain_text) in [email](https://en.wikipedia.org/wiki/Email) and [usenet](https://en.wikipedia.org/wiki/Usenet) posts,[^12] such as the earlier markup languages [setext](https://en.wikipedia.org/wiki/Setext) (c. 1992), [Textile](https://en.wikipedia.org/wiki/Textile_(markup_language)) (c. 2002), and [reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText) (c. 2002)[^9].

In 2002, [Aaron Swartz](https://en.wikipedia.org/wiki/Aaron_Swartz) created [atx](https://en.wikipedia.org/wiki/Atx_(markup_language)) and referred to it as "the true structured text format." Gruber created the Markdown language in 2004 with Swartz as his "sounding board."[^13] The goal of language was to enable people "to write using an easy-to-read and easy-to-write plain text format, optionally convert it to structurally valid [XHTML](https://en.wikipedia.org/wiki/XHTML) (or [HTML](https://en.wikipedia.org/wiki/HTML))."[^5]

Its key design goal was *readability*, that the language be readable as-is, without looking like it has been marked up with tags or formatting instructions,[^9] unlike text formatted with 'heavier' [markup languages](https://en.wikipedia.org/wiki/Markup_language), such as [Rich Text Format](https://en.wikipedia.org/wiki/Rich_Text_Format) (RTF), HTML, or even [wikitext](https://en.wikipedia.org/wiki/Wikitext) (each of which have obvious in-line tags and formatting instructions which can make the text more difficult for humans to read).

Gruber wrote a [Perl](https://en.wikipedia.org/wiki/Perl) script, `Markdown.pl`, which converts marked-up text input to valid, [well-formed](https://en.wikipedia.org/wiki/XML#Well-formedness_and_error-handling) XHTML or HTML and replaces angle brackets (< and >) and [ampersands](https://en.wikipedia.org/wiki/Ampersand) (&) with their corresponding [character entity references](https://en.wikipedia.org/wiki/Character_entity_references). It can take the role of a standalone script, a plugin for [Blosxom](https://en.wikipedia.org/wiki/Blosxom) or a [Movable Type](https://en.wikipedia.org/wiki/Movable_Type), or of a text filter for [BBEdit](https://en.wikipedia.org/wiki/BBEdit).

## Rise and divergence

As Markdown's popularity grew rapidly, many Markdown [implementations](https://en.wikipedia.org/wiki/Implementation) appeared, driven mostly by the need for additional features such as [tables](https://en.wikipedia.org/wiki/Table_(information)), [footnotes](https://en.wikipedia.org/wiki/Note_(typography)), definition lists,[^16] and Markdown inside HTML blocks.

The behavior of some of these diverged from the reference implementation, as Markdown was only characterized by an informal [specification](https://en.wikipedia.org/wiki/Specification_(technical_standard))[^17] and a [Perl](https://en.wikipedia.org/wiki/Perl) implementation for conversion to HTML.

At the same time, a number of ambiguities in the informal specification had attracted attention.[^18] These issues spurred the creation of tools such as Babelmark[^19][^20] to compare the output of various implementations,[^21] and an effort by some developers of Markdown [parsers](https://en.wikipedia.org/wiki/Parsing) for standardization. However, Gruber has argued that complete standardization would be a mistake: "Different sites (and people) have different needs. No one syntax would make all happy."[^22]

Gruber avoided using curly braces in Markdown to unofficially reserve them for implementation-specific extensions.[^23]

## Standardization

| Filename extensions | Internet media type | Uniform Type Identifier (UTI)                                                                             | Developed by                     | Initial release | Latest release | Type of format   | Extended to             |
|---------------------|---------------------|-------------------------------------------------------------------------------------------------------------|-----------------------------------|------------------|----------------|-------------------|--------------------------|
| `.md`, `.markdown`  | `text/markdown`     | `net.daringfireball.markdown`                                                                                | [John Gruber](https://en.wikipedia.org/wiki/John_Gruber) | March 9, 2004   | 1.0.1, December 17, 2004 | [Open file format](https://en.wikipedia.org/wiki/Open_file_format) | [pandoc](https://en.wikipedia.org/wiki/Pandoc), [MultiMarkdown](https://en.wikipedia.org/wiki/MultiMarkdown), [Markdown Extra](https://en.wikipedia.org/wiki/Markdown_Extra), [CommonMark](#Standardization), [RMarkdown](https://en.wikipedia.org/wiki/RMarkdown) |

From 2012, a group of people, including [Jeff Atwood](https://en.wikipedia.org/wiki/Jeff_Atwood) and [John MacFarlane](https://en.wikipedia.org/wiki/John_MacFarlane_(philosopher)), launched what Atwood characterized as a standardization effort.[^11] 

A community website now aims to "document various tools and resources available to document authors and developers, as well as implementors of the various Markdown implementations."[^26]

In September 2014, Gruber objected to the usage of "Markdown" in the name of this effort and it was rebranded as CommonMark.[^12][^27][^28] CommonMark.org published several versions of a specification, reference implementation, test suite, and "[plans] to announce a finalized 1.0 spec and test suite in 2019."[59]

No 1.0 spec has since been released as major issues still remain unsolved.[^30]

Nonetheless, the following websites and projects have adopted CommonMark: [Discourse](https://en.wikipedia.org/wiki/Discourse_(software)), [GitHub](https://en.wikipedia.org/wiki/GitHub), [GitLab](https://en.wikipedia.org/wiki/GitLab), [Reddit](https://en.wikipedia.org/wiki/Reddit), [Qt](https://en.wikipedia.org/wiki/Qt_(software)), [Stack Exchange](https://en.wikipedia.org/wiki/Stack_Exchange) ([Stack Overflow](https://en.wikipedia.org/wiki/Stack_Overflow)), and [Swift](https://en.wikipedia.org/wiki/Swift_(programming_language)).

In March 2016, two relevant informational Internet [RFCs](https://en.wikipedia.org/wiki/Request_for_Comments) were published:

1. RFC [7763](https://datatracker.ietf.org/doc/html/rfc7763) introduced MIME type `text/markdown`.

2. RFC [7764](https://datatracker.ietf.org/doc/html/rfc7764) discussed and registered the variants [MultiMarkdown](https://en.wikipedia.org/wiki/MultiMarkdown), GitHub Flavored Markdown (GFM), [Pandoc](https://en.wikipedia.org/wiki/Pandoc), and Markdown Extra among others.[^31]

## Variants

Websites like [Bitbucket](https://en.wikipedia.org/wiki/Bitbucket), [Diaspora](https://en.wikipedia.org/wiki/Diaspora_(social_network)), [GitHub](https://en.wikipedia.org/wiki/GitHub)[^32][^31], [OpenStreetMap](https://en.wikipedia.org/wiki/OpenStreetMap), [Reddit](https://en.wikipedia.org/wiki/Reddit)[^32][^31], [SourceForge](https://en.wikipedia.org/wiki/SourceForge)[^33][^32], and [Stack Exchange](https://en.wikipedia.org/wiki/Stack_Exchange)[^34] use variants of Markdown to make discussions between users easier. 

Depending on implementation, basic inline [HTML tags](https://en.wikipedia.org/wiki/HTML_tag) may be supported.[^35] 

Italic text may be implemented by `_underscores_` or `*single-asterisks*`.[^36]

### GitHub Flavored Markdown

GitHub had been using its own variant of Markdown since as early as 2009,[^37] which added support for additional formatting such as tables and nesting [block content](https://en.wikipedia.org/wiki/HTML_element#Block_elements) inside list elements, as well as GitHub-specific features such as auto-linking references to commits, issues, usernames, etc.

In 2017, GitHub released a formal specification of its GitHub Flavored Markdown (GFM) that is based on CommonMark.[^32] It is a [strict superset](https://en.wikipedia.org/wiki/Superset) of CommonMark, following its specification exactly except for tables, [strikethrough](https://en.wikipedia.org/wiki/Strikethrough), [autolinks](https://en.wikipedia.org/wiki/Automatic_hyperlinking), and task lists, which GFM adds as extensions.[^38]

Accordingly, GitHub also changed the parser used on their sites, which required that some documents be changed. For instance, GFM now requires that the hash symbol that creates a heading be separated from the heading text by a space character.

### Markdown Extra

Markdown Extra is a [lightweight markup language](https://en.wikipedia.org/wiki/Lightweight_markup_language) based on Markdown implemented in [PHP](https://en.wikipedia.org/wiki/PHP) (originally), [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) and [Ruby](https://en.wikipedia.org/wiki/Ruby_(programming_language)).[^39] It adds the following features that are not available with regular Markdown:

- Markdown markup inside [HTML](https://en.wikipedia.org/wiki/HTML) blocks

- Elements with id/class attribute

- "Fenced code blocks" that span multiple lines of code

- Tables[^40]

- Definition lists

- Footnotes

- Abbreviations

Markdown Extra is supported in some [content management systems](https://en.wikipedia.org/wiki/Content_management_system) such as [Drupal](https://en.wikipedia.org/wiki/Drupal)[^41], [Grav](https://en.wikipedia.org/wiki/Grav_(CMS)), and [TYPO3](https://en.wikipedia.org/wiki/TYPO3).

### LiaScript

LiaScript[^43] is a Markdown dialect that was designed to create interactive educational content. It is implemented in [Elm](https://en.wikipedia.org/wiki/Elm_(programming_language)) and [TypeScript](https://en.wikipedia.org/wiki/TypeScript) and adds additional syntax elements to define features like:

- [Animations](https://en.wikipedia.org/wiki/Animation)

- Automatic [speech output](https://en.wikipedia.org/wiki/Speech_synthesis)

- [Mathematical formulas](https://en.wikipedia.org/wiki/Formula) (using [KaTeX](https://en.wikipedia.org/wiki/KaTeX))

- [ASCII art](https://en.wikipedia.org/wiki/ASCII_art) diagrams

- Various types of [quizzes](https://en.wikipedia.org/wiki/Quiz) and surveys

- [JavaScript](https://en.wikipedia.org/wiki/JavaScript) is natively supported and can be attached to various elements, this way code fragments can be made executable and editable

## Examples

| Text using Markdown syntax                                 | Corresponding HTML produced by a Markdown processor                          | Text viewed in a browser                                               |
|-----------------------------------------------------------|-------------------------------------------------------------------------------|----------------------------------------------------------------------|
| Heading                                                  | `<h1>Heading</h1>`                                                           | <h1>Heading</h1>                                                    |
| Sub-heading                                              | `<h2>Sub-heading</h2>`                                                       | <h2>Sub-heading</h2>                                               |
| Paragraphs are separated by a blank line.                | `<p>Paragraphs are separated by a blank line.</p>`                           | <p>Paragraphs are separated by a blank line.</p>                   |
| Two spaces at the end of a line produce a line break.    | `<p>Two spaces at the end of a line<br />produce a line break.</p>`          | <p>Two spaces at the end of a line<br />produce a line break.</p> |
| Text attributes _italic_, **bold**, `monospace`.         | `<p>Text attributes <em>italic</em>, <strong>bold</strong>, <code>monospace</code>.</p>` | Text attributes <i>italic</i>, <b>bold</b>, <code>monospace</code>. |
| Horizontal rule:                                         | `<hr />`                                                                      | <hr />                                                             |

## Implementations

Implementations of Markdown are available for over a dozen [programming languages](https://en.wikipedia.org/wiki/Programming_language); in addition, many [applications](https://en.wikipedia.org/wiki/Application_software), platforms and [frameworks](https://en.wikipedia.org/wiki/Software_framework) support Markdown.[^45] For example, Markdown [plugins](https://en.wikipedia.org/wiki/Plug-in_(computing)) exist for every major [blogging](https://en.wikipedia.org/wiki/Blog) platform.[^12]

While Markdown is a minimal markup language and is read and edited with a normal [text editor](https://en.wikipedia.org/wiki/Text_editor), there are specially designed editors that preview the files with styles, which are available for all major platforms. Many general-purpose text and [code editors](https://en.wikipedia.org/wiki/Source-code_editor) have [syntax highlighting](https://en.wikipedia.org/wiki/Syntax_highlighting) plugins for Markdown built into them or available as optional download. Editors may feature a side-by-side preview window or render the code directly in a [WYSIWYG](https://en.wikipedia.org/wiki/WYSIWYG) fashion.

Some apps, services, and editors support Markdown as an editing format, including:

- [Bugzilla](https://en.wikipedia.org/wiki/Bugzilla) uses a customized version of Markdown.[^46]

- [ChatGPT](https://en.wikipedia.org/wiki/ChatGPT): Output from the LLM formatted in Markdown will be rendered in LaTeX and HTML by the ChatGPT client, and the model is encouraged to use Markdown to format its output. Markdown provided by the user will not be formatted by the client, but will still be passed to the model unaltered.

- [Discord](https://en.wikipedia.org/wiki/Discord_(software)): chat messages[^47]

- [Discourse](https://en.wikipedia.org/wiki/Discourse_(software)) uses the CommonMark flavor of Markdown in the forum post composer.

- [Doxygen](https://en.wikipedia.org/wiki/Doxygen): a source code documentation generator which supports Markdown with extra features[^48]

- [GitHub](https://en.wikipedia.org/wiki/GitHub): GitHub Flavored Markdown (GFM) ignores underscores in words and adds [syntax highlighting](https://en.wikipedia.org/wiki/Syntax_highlighting), [task lists](https://en.wikipedia.org/wiki/Task_list), and tables[^49].

- The [GNOME Evolution](https://en.wikipedia.org/wiki/GNOME_Evolution) email client supports composing messages in Markdown format,[^50] with the ability to send and render emails in pure Markdown format (`Content-Type: text/markdown;`) or to convert Markdown to [plaintext](https://en.wikipedia.org/wiki/Plaintext) or [HTML email](https://en.wikipedia.org/wiki/HTML_email) when sending.

- [Joplin](https://en.wikipedia.org/wiki/Joplin_(software)): a note-taking application that supports markdown formatting[^51].

- [JotterPad](https://en.wikipedia.org/wiki/JotterPad): an online WYSIWYG editor that supports Markdown[^52].

- [Kanboard](https://en.wikipedia.org/wiki/Kanboard) uses the standard Markdown syntax as its only formatting syntax for task descriptions.[^53]

## See also

- [Comparison of document markup languages](https://en.wikipedia.org/wiki/Comparison_of_document_markup_languages)

- [Comparison of documentation generators](https://en.wikipedia.org/wiki/Comparison_of_documentation_generators)

- [Lightweight markup language](https://en.wikipedia.org/wiki/Lightweight_markup_language)

- [Wiki markup](https://en.wikipedia.org/wiki/Wiki_markup)

## Explanatory notes

[^9]: Markdown Syntax * - Daring Fireball  
[^10]: Daring Fireball: Introducing Markdown  
[^11]: The Future of Markdown - CodingHorror.com  
[^12]: Markdown: License - Daring Fireball  
[^13]: The markdown file extension  
[^16]: Technically HTML description lists  
[^17]: rv: 12642953  
[^18]: Markdown Syntax Documentation  
[^19]: Babelmark 2 - Compare markdown implementations  
[^20]: Babelmark 3 - Compare Markdown Implementations  
[^21]: 330707 - Mozilla  

## References

- Markup Languages Overview

## External links

- [Official website](https://daringfireball.net/projects/markdown/) for original John Gruber markup  

