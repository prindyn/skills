# Custom Fonts

Place `.ttf` or `.woff2` font files here and reference them from `assets/book.css`
using `@font-face` rules.

Example:

```css
@font-face {
  font-family: "MyFont";
  src: url("assets/fonts/MyFont-Regular.ttf") format("truetype");
  font-weight: normal;
  font-style: normal;
}
```

Then update `font-family` in `book.css` to use `"MyFont"`.

WeasyPrint resolves font paths relative to the CSS file or the base URL passed
to `HTML()`. pdfkit / wkhtmltopdf requires absolute paths in `@font-face` `src`.
