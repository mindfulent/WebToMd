Here's a comprehensive guide to creating properly formatted Markdown documents:

## Headings

Use hash symbols (#) to create headings. The number of hashes corresponds to the heading level:

```markdown
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6
```

Always include a space between the hash and the heading text. Leave blank lines before and after headings for better readability.

## Paragraphs and Line Breaks

Separate paragraphs with a blank line. For line breaks within a paragraph, end a line with two or more spaces before pressing return.

## Text Formatting

- **Bold**: Wrap text with double asterisks or underscores: `**bold text**` or `__bold text__`
- *Italic*: Use single asterisks or underscores: `*italic text*` or `_italic text_`
- ***Bold and Italic***: Combine both: `***bold and italic***` or `___bold and italic___`
- ~~Strikethrough~~: Use double tildes: `~~strikethrough text~~`

## Lists

### Unordered Lists

Use asterisks, plus signs, or hyphens:

```markdown
* Item 1
* Item 2
  * Subitem 2.1
  * Subitem 2.2
```

### Ordered Lists

Use numbers followed by periods:

```markdown
1. First item
2. Second item
   1. Subitem 2.1
   2. Subitem 2.2
```

## Links

Create links using square brackets for the link text and parentheses for the URL:

```markdown
[Visit OpenAI](https://www.openai.com)
```

For reference-style links:

```markdown
[OpenAI][1]

[1]: https://www.openai.com
```

## Images

Insert images similarly to links, but with an exclamation mark at the beginning:

```markdown
![Alt text](image-url.jpg "Optional title")
```

## Blockquotes

Use the greater-than symbol (>) for blockquotes:

```markdown
> This is a blockquote.
> It can span multiple lines.
```

## Code

For inline code, use backticks:

```markdown
Use the `print()` function in Python.
```

For code blocks, use triple backticks and specify the language for syntax highlighting:

```markdown
```python
def hello_world():
    print("Hello, World!")
```
```

## Horizontal Rules

Create horizontal rules with three or more hyphens, asterisks, or underscores:

```markdown
---
***
___
```

## Tables

Create tables using pipes and hyphens:

```markdown
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |
```

## Task Lists

Create task lists with square brackets:

```markdown
- [x] Completed task
- [ ] Uncompleted task
```

## Escaping Characters

Use a backslash ($$ to escape Markdown formatting characters:

```markdown
\*This text is not italic\*
```

## Footnotes

Add footnotes using square brackets with a caret:

```markdown
Here's a sentence with a footnote.[^1]

[^1]: This is the footnote.
```

## Conclusion

Remember to maintain consistent formatting throughout your document. Use blank lines to separate different elements for better readability. Always preview your Markdown to ensure it renders as intended[1][2][3][4].

Citations:
[1] https://www.markdownguide.org/getting-started/
[2] https://www.markdownguide.org/basic-syntax/
[3] https://www.writethedocs.org/guide/writing/markdown/
[4] https://docs.skillable.com/docs/creating-instructions-with-markdown-syntax
[5] https://www.markdownguide.org
[6] https://document360.com/blog/introductory-guide-to-markdown-for-documentation-writers/
[7] https://experienceleague.adobe.com/en/docs/contributor/contributor-guide/writing-essentials/markdown
[8] https://dev.to/soumikdhar/how-to-write-better-cleaner-markdown-the-definitive-guide-3fif