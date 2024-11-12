# Markdown

**Markdown** is a lightweight markup language for creating formatted text using a plain-text editor. [John Gruber](https://en.wikipedia.org/wiki/John_Gruber) created Markdown in 2004 as an easy-to-read markup language. Markdown is widely used for blogging and instant messaging, and also used elsewhere in online forums, collaborative software, documentation pages, and readme files.

The initial description of Markdown contained ambiguities and raised unanswered questions, causing implementations to both intentionally and accidentally diverge from the original version. This was addressed in 2014 when long-standing Markdown contributors released [CommonMark](#Standardization), an unambiguous specification and test suite for Markdown.

## History

Markdown was inspired by pre-existing conventions for marking up plain text in email and usenet posts, such as the earlier markup languages [setext](https://en.wikipedia.org/wiki/Setext) (c. 1992), [Textile](https://en.wikipedia.org/wiki/Textile_(markup_language)) (c. 2002), and [reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText) (c. 2002).

In 2002 [Aaron Swartz](https://en.wikipedia.org/wiki/Aaron_Swartz) created [atx](https://en.wikipedia.org/wiki/Atx_(markup_language)) and referred to it as "the true structured text format". Gruber created the Markdown language in 2004 with Swartz as his "sounding board." The goal of language was to enable people "to write using an easy-to-read and easy-to-write plain text format, optionally convert it to structurally valid [XHTML](https://en.wikipedia.org/wiki/XHTML) (or [HTML](https://en.wikipedia.org/wiki/HTML))."

Its key design goal was *readability*, that the language be readable as-is, without looking like it has been marked up with tags or formatting instructions, unlike text formatted with 'heavier' markup languages, such as [Rich Text Format](https://en.wikipedia.org/wiki/Rich_Text_Format) (RTF), HTML, or even [wikitext](https://en.wikipedia.org/wiki/Wikitext) (each of which have obvious in-line tags and formatting instructions which can make the text more difficult for humans to read).

Gruber wrote a [Perl](https://en.wikipedia.org/wiki/Perl) script, `Markdown.pl`, which converts marked-up text input to valid, well-formed XHTML or HTML and replaces angle brackets (`<`, `>`) and ampersands (`&`) with their corresponding character entity references. 

## Rise and divergence

As Markdown's popularity grew rapidly, many Markdown implementations appeared, driven mostly by the need for additional features such as tables, footnotes, definition lists, and Markdown inside HTML blocks.

The behavior of some of these diverged from the reference implementation, as Markdown was only characterised by an informal specification and a Perl implementation for conversion to HTML.

At the same time, a number of ambiguities in the informal specification had attracted attention. These issues spurred the creation of tools such as Babelmark to compare the output of various implementations, and an effort by some developers of Markdown parsers for standardisation.

However, Gruber has argued that complete standardization would be a mistake: "Different sites (and people) have different needs. No one syntax would make all happy."

Gruber avoided using curly braces in Markdown to unofficially reserve them for implementation-specific extensions.

## Standardization

| Filename extensions | Internet media type       | Uniform Type Identifier (UTI) | Developed by    | Initial release | Latest release    | Type of format     | Extended to                      |
|---------------------|---------------------------|--------------------------------|------------------|------------------|-------------------|---------------------|------------------------------------|
| `.md`, `.markdown`  | `text/markdown`          | `net.daringfireball.markdown` | John Gruber      | March 9, 2004    | 1.0.1             | Open file format   | pandoc, MultiMarkdown, Markdown Extra, CommonMark, RMarkdown |

From 2012, a group of people, including [Jeff Atwood](https://en.wikipedia.org/wiki/Jeff_Atwood) and [John MacFarlane (philosopher)](https://en.wikipedia.org/wiki/John_MacFarlane_(philosopher)), launched what Atwood characterised as a standardisation effort.

In September 2014, Gruber objected to the usage of "Markdown" in the name of this effort and it was rebranded as CommonMark. CommonMark.org published several versions of a specification, reference implementation, test suite, and "plans to announce a finalized 1.0 spec and test suite in 2019."

No 1.0 spec has since been released as major issues still remain unsolved.

Nonetheless, the following websites and projects have adopted CommonMark: [Discourse](https://en.wikipedia.org/wiki/Discourse_(software)), [GitHub](https://en.wikipedia.org/wiki/GitHub), [GitLab](https://en.wikipedia.org/wiki/GitLab), [Reddit](https://en.wikipedia.org/wiki/Reddit), [Qt](https://en.wikipedia.org/wiki/Qt_(software)), [Stack Exchange](https://en.wikipedia.org/wiki/Stack_Exchange) (Stack Overflow), and [Swift](https://en.wikipedia.org/wiki/Swift_(programming_language)).

In March 2016, two relevant informational Internet RFCs were published:

- RFC [7763](https://datatracker.ietf.org/doc/html/rfc7763) introduced MIME type `text/markdown`.

- RFC [7764](https://datatracker.ietf.org/doc/html/rfc7764) discussed and registered the variants MultiMarkdown, GitHub Flavored Markdown (GFM), Pandoc, and Markdown Extra among others.

## Variants

Websites like [Bitbucket](https://en.wikipedia.org/wiki/Bitbucket), [Diaspora](https://en.wikipedia.org/wiki/Diaspora_(social_network)), [GitHub](https://en.wikipedia.org/wiki/GitHub), [OpenStreetMap](https://en.wikipedia.org/wiki/OpenStreetMap), [Reddit](https://en.wikipedia.org/wiki/Reddit), [SourceForge](https://en.wikipedia.org/wiki/SourceForge) and [Stack Exchange](https://en.wikipedia.org/wiki/Stack_Exchange) use variants of Markdown to make discussions between users easier.

Depending on implementation, basic inline [HTML tags](https://en.wikipedia.org/wiki/HTML_tag) may be supported. Italic text may be implemented by `_underscores_` or `*single-asterisks*`.

### GitHub Flavored Markdown

GitHub had been using its own variant of Markdown since as early as 2009, which added support for additional formatting such as tables and nesting block content inside list elements, as well as GitHub-specific features such as auto-linking references to commits, issues, usernames, etc.

In 2017, GitHub released a formal specification of its GitHub Flavored Markdown (GFM) that is based on CommonMark. It is a strict superset of CommonMark, following its specification exactly except for tables, strikethrough, autolinks and task lists, which GFM adds as extensions.

Accordingly, GitHub also changed the parser used on their sites, which required that some documents be changed. For instance, GFM now requires that the hash symbol that creates a heading be separated from the heading text by a space character.

### Markdown Extra

Markdown Extra is a lightweight markup language based on Markdown implemented in PHP (originally), Python and Ruby. It adds the following features that are not available with regular Markdown:

- Markdown markup inside HTML blocks

- Elements with id/class attribute

- "Fenced code blocks" that span multiple lines of code

- Tables

- Definition lists

- Footnotes

- Abbreviations

Markdown Extra is supported in some content management systems such as [Drupal](https://en.wikipedia.org/wiki/Drupal), [Grav (CMS)](https://en.wikipedia.org/wiki/Grav_(CMS)) and [TYPO3](https://en.wikipedia.org/wiki/TYPO3).

### LiaScript

LiaScript is a Markdown dialect that was designed to create interactive educational content. It is implemented in Elm and TypeScript and adds additional syntax elements to define features like:

- Animations

- Automatic speech output

- Mathematical formulas (using KaTeX)

- ASCII art diagrams

- Various types of quizzes and surveys

- JavaScript is natively supported and can be attached to various elements, this way code fragments can be made executable and editable.

## Examples

| Text using Markdown syntax                                   | Corresponding HTML produced by a Markdown processor                                          | Text viewed in a browser                                    |
|--------------------------------------------------------------|-----------------------------------------------------------------------------------------------|-------------------------------------------------------------|
| Heading                                                      | `<h1>Heading</h1>`                                                                          | <div style="font-size: 1.8em;">Heading</div>               |
| Sub-heading                                                  | `<h2>Sub-heading</h2>`                                                                      | <div style="font-size: 1.5em;">Sub-heading</div>            |
| Bullet lists nested within numbered list:                   | `<ol><li>fruits <ul><li>apple</li><li>banana</li></ul></li><li>vegetables <ul><li>carrot</li><li>broccoli</li></ul></li></ol>` | Bullet lists nested within numbered list:                   |

## Implementations

Implementations of Markdown are available for over a dozen programming languages; in addition, many applications, platforms and frameworks support Markdown. For example, Markdown plugins exist for every major blogging platform.

While Markdown is a minimal markup language and is read and edited with a normal text editor, there are specially designed editors that preview the files with styles, which are available for all major platforms. Many general-purpose text and code editors have syntax highlighting plugins for Markdown built into them or available as optional download. Editors may feature a side-by-side preview window or render the code directly in a WYSIWYG fashion.

Some apps, services, and editors support Markdown as an editing format, including:

- [Bugzilla](https://en.wikipedia.org/wiki/Bugzilla) uses a customized version of Markdown.

- [ChatGPT](https://en.wikipedia.org/wiki/ChatGPT): Output from the LLM formatted in Markdown will be rendered in LaTeX and HTML by the ChatGPT client, and the model is encouraged to use Markdown to format its output. Markdown provided by the user will not be formatted by the client, but will still be passed to the model unaltered.

- [Discord](https://en.wikipedia.org/wiki/Discord_(software)): chat messages.

- [Discourse](https://en.wikipedia.org/wiki/Discourse_(software)) uses the CommonMark flavor of Markdown in the forum post composer.

- [Doxygen](https://en.wikipedia.org/wiki/Doxygen): a source code documentation generator which supports Markdown with extra features.

- [GitHub](https://en.wikipedia.org/wiki/GitHub) Flavored Markdown (GFM) ignores underscores in words, and adds syntax highlighting, task lists, and tables.

- The [GNOME Evolution](https://en.wikipedia.org/wiki/GNOME_Evolution) email client supports composing messages in Markdown format.

- [Joplin](https://en.wikipedia.org/wiki/Joplin_(software)): a note-taking application that supports markdown formatting.

- [JotterPad](https://en.wikipedia.org/wiki/JotterPad): an online WYSIWYG editor that supports Markdown and Fountain.

- [Kanboard](https://en.wikipedia.org/wiki/Kanboard): uses the standard Markdown syntax as its only formatting syntax for task descriptions.

- [Microsoft Azure DevOps](https://en.wikipedia.org/wiki/Microsoft_Azure_DevOps)' wiki feature has its own implementation.

- [Microsoft Teams](https://en.wikipedia.org/wiki/Microsoft_Teams): chat messages.

- [Misskey](https://en.wikipedia.org/wiki/Misskey): ensures a custom text format misleadingly called "Misskey-Flavored Markdown (MFM)".

- The [Mozilla Thunderbird](https://en.wikipedia.org/wiki/Mozilla_Thunderbird) email client supports Markdown through the "Markdown here Revival" add-on.

- [Nextcloud](https://en.wikipedia.org/wiki/Nextcloud): the default app for taking notes on the Nextcloud platform supports formatting using Markdown.

- [Obsidian](https://en.wikipedia.org/wiki/Obsidian_(software)) is note-taking software based on Markdown files.

- [RMarkdown](https://en.wikipedia.org/wiki/RMarkdown).

- [RStudio](https://en.wikipedia.org/wiki/RStudio): an IDE for R. It provides a C++ wrapper function for a markdown variant called sundown.

- [Simplenote](https://en.wikipedia.org/wiki/Simplenote).

## See also

- [Comparison of document markup languages](https://en.wikipedia.org/wiki/Comparison_of_document_markup_languages)

- [Comparison of documentation generators](https://en.wikipedia.org/wiki/Comparison_of_documentation_generators)

- [Lightweight markup language](https://en.wikipedia.org/wiki/Lightweight_markup_language)

- [Wiki markup](https://en.wikipedia.org/wiki/Wiki_markup)

## Explanatory notes

*Technically HTML description lists*

## References

1. Gruber, John (8 January 2014). [The Markdown File Extension](https://daringfireball.net/linked/2014/01/08/markdown-extension). The Daring Fireball Company, LLC.

2. Leonard, Sean (March 2016). [The text/markdown Media Type](https://datatracker.ietf.org/doc/html/rfc7763). Request for Comments: 7763. Internet Engineering Task Force.

3. Swartz, Aaron (2004-03-19). [Markdown](http://www.aaronsw.com/weblog/001189). Aaron Swartz: The Weblog.

4. Gruber, John. [Markdown](https://daringfireball.net/projects/markdown/index.text). Daring Fireball.

5. Markdown 1.0.1 readme source code. [Daring Fireball – Markdown](https://daringfireball.net/projects/markdown/).

6. Markdown: License. Daring Fireball.

7. RFC 7764. [Guidance on Markdown: Design Philosophies, Stability Strategies, and Select Registrations](https://datatracker.ietf.org/doc/html/rfc7764). Internet Engineering Task Force.

