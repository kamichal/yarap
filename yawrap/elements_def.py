from collections import namedtuple

H4 = 'html4'  # only in html4
H5 = 'html5'  # only in html5
HB = 'both'  # allowed in both
N = 'normal'  # has a closing tag
E = 'empty'  # doesn't have a closing tag

ES = namedtuple('ES', 'tag, standard, type_, info')
ER = namedtuple('ES', 'tag, info')

HTML_ELEMENTS = [
    ES("html", HB, N, "Defines an HTML document"),
    ES("head", HB, N, "Defines information about the document"),
    ES("title", HB, N, "Defines a title for the document"),
    ES("body", HB, N, "Defines the document's body"),
    ES("h1", HB, N, "Defines HTML heading, rank 1."),
    ES("h2", HB, N, "Defines HTML heading, rank 2."),
    ES("h3", HB, N, "Defines HTML heading, rank 3."),
    ES("h4", HB, N, "Defines HTML heading, rank 4."),
    ES("h5", HB, N, "Defines HTML heading, rank 5."),
    ES("h6", HB, N, "Defines HTML heading, rank 6."),
    ES("p", HB, N, "Defines a paragraph"),
    ES("br", HB, E, "Inserts a single line break"),
    ES("hr", HB, E, "Defines a thematic change in the content"),
    # Formatting
    ES("acronym", H4, N, "Not supported in HTML5. Use <abbr> instead. Defines an acronym."),
    ES("abbr", HB, N, "Defines an abbreviation or an acronym"),
    ES("address", HB, N, "Defines contact information for the author/owner of a document/article"),
    ES("b", HB, N, "Defines bold text"),
    ES("bdi", H5, N, "Isolates a part of text that might be formatted in a different direction from "
                     "other text outside it"),  # noqa: E501
    ES("bdo", HB, N, "Overrides the current text direction"),
    ES("big", H4, N, "Not supported in HTML5. Use CSS instead. Defines big text"),
    ES("blockquote", HB, N, "Defines a section that is quoted from another source"),
    ES("center", H4, N, "Not supported in HTML5. Use CSS instead. Defines centered text."),
    ES("cite", HB, N, "Defines the title of a work"),
    ES("code", HB, N, "Defines a piece of computer code"),
    ES("del", HB, N, "Defines text that has been deleted from a document"),
    ES("dfn", HB, N, "Represents the defining instance of a term"),
    ES("em", HB, N, "Defines emphasized text "),
    ES("font", H4, N, "Not supported in HTML5. Use CSS instead. Defines font, color, and size for text."),
    ES("i", HB, N, "Defines a part of text in an alternate voice or mood"),
    ES("ins", HB, N, "Defines a text that has been inserted into a document"),
    ES("kbd", HB, N, "Defines keyboard input"),
    ES("mark", H5, N, "Defines marked/highlighted text"),
    ES("meter", HB, N, "Defines a scalar measurement within a known range (a gauge)"),
    ES("pre", HB, N, "Defines preformatted text"),
    ES("progress", H5, N, "Represents the progress of a task"),
    ES("q", HB, N, "Defines a short quotation"),
    ES("rp", H5, N, "Defines what to show in browsers that do not support ruby annotations"),
    ES("rt", H5, N, "Defines an explanation/pronunciation of characters (for East Asian typography)"),
    ES("ruby", H5, N, "Defines a ruby annotation (for East Asian typography)"),
    ES("s", HB, N, "Defines text that is no longer correct"),
    ES("samp", HB, N, "Defines sample output from a computer program"),
    ES("small", HB, N, "Defines smaller text"),
    ES("strike", H4, N, "Not supported in HTML5. Use <del> or <s> instead. Defines strikethrough text"),
    ES("strong", HB, N, "Defines important text"),
    ES("sub", HB, N, "Defines subscripted text"),
    ES("sup", HB, N, "Defines superscripted text"),
    ES("time", H5, N, "Defines a date/time"),
    ES("tt", H4, N, "Not supported in HTML5. Use CSS instead. Defines teletype text."),
    ES("u", HB, N, "Defines text that should be stylistically different from normal text"),
    ES("var", HB, N, "Defines a variable"),
    ES("wbr", H5, E, "Defines a possible line-break"),
    # Forms and Input
    ES("form", HB, N, "Defines an HTML form for user input"),
    ES("input", HB, E, "Defines an input control"),
    ES("textarea", HB, N, "Defines a multiline input control (text area)"),
    ES("button", HB, N, "Defines a clickable button"),
    ES("select", HB, N, "Defines a drop-down list"),
    ES("optgroup", HB, N, "Defines a group of related options in a drop-down list"),
    ES("option", HB, N, "Defines an option in a drop-down list"),
    ES("label", HB, N, "Defines a label for an <input> element"),
    ES("fieldset", HB, N, "Groups related elements in a form"),
    ES("legend", HB, N, "Defines a caption for a <fieldset> element"),
    ES("datalist", H5, N, "Specifies a list of pre-defined options for input controls"),
    ES("keygen", H5, E, "Defines a key-pair generator field (for forms)"),
    ES("output", H5, N, "Defines the result of a calculation"),
    # Frames
    ES("frame", H4, N, "Not supported in HTML5. Defines a window (a frame) in a frameset"),
    ES("frameset", H4, N, "Not supported in HTML5. Defines a set of frames"),
    ES("noframes", H4, N, "Not supported in HTML5. Defines an alternate content for users "
                          "that do not support frames"),
    ES("iframe", HB, N, "Defines an inline frame"),
    # Images
    ES("img", HB, E, "Defines an image"),
    ES("map", HB, N, "Defines a client-side image-map"),
    ES("area", HB, E, "Defines an area inside an image-map"),
    ES("canvas", H5, N, "Used to draw graphics, on the fly, via scripting (usually JavaScript)"),
    ES("figcaption", H5, N, "Defines a caption for a <figure> element"),
    ES("figure", H5, N, "Specifies self-contained content"),
    ES("picture", H5, N, "Defines a container for multiple image resources"),
    # Audio / Video
    ES("audio", H5, N, "Defines sound content"),
    ES("source", H5, E, "Defines multiple media resources for media elements (<video>, <audio> and <picture>"),
    ES("track", H5, E, "Defines text tracks for media elements (<video> and <audio>"),
    ES("video", H5, N, "Defines a video or movie"),
    # Links
    ES("a", HB, N, "Defines a hyperlink"),
    ES("link", HB, E, "Defines the relationship between a document and an external resource "
                      "(most used to link to style sheets)"),
    ES("nav", H5, N, "Defines navigation links"),
    # Lists
    ES("ul", HB, N, "Defines an unordered list"),
    ES("ol", HB, N, "Defines an ordered list"),
    ES("li", HB, N, "Defines a list item"),
    ES("dir", H4, N, "Not supported in HTML5. Use <ul> instead. Defines a directory list"),
    ES("dl", HB, N, "Defines a description list"),
    ES("dt", HB, N, "Defines a term/name in a description list"),
    ES("dd", HB, N, "Defines a description of a term/name in a description list"),
    ES("menu", HB, N, "Defines a list/menu of commands"),
    ES("menuitem", H5, N, "Defines a command/menu item that the user can invoke from a popup menu"),
    # Tables
    ES("table", HB, N, "Defines a table"),
    ES("caption", HB, N, "Defines a table caption"),
    ES("th", HB, N, "Defines a header cell in a table"),
    ES("tr", HB, N, "Defines a row in a table"),
    ES("td", HB, N, "Defines a cell in a table"),
    ES("thead", HB, N, "Groups the header content in a table"),
    ES("tbody", HB, N, "Groups the body content in a table"),
    ES("tfoot", HB, N, "Groups the footer content in a table"),
    ES("col", HB, E, "Specifies column properties for each column within a <colgroup> element"),
    ES("colgroup", HB, N, "Specifies a group of one or more columns in a table for formatting"),
    # Styles and Semantics
    ES("style", HB, N, "Defines style information for a document"),
    ES("div", HB, N, "Defines a section in a document"),
    ES("span", HB, N, "Defines a section in a document"),
    ES("header", H5, N, "Defines a header for a document or section"),
    ES("footer", H5, N, "Defines a footer for a document or section"),
    ES("main", H5, N, "Specifies the main content of a document"),
    ES("section", H5, N, "Defines a section in a document"),
    ES("article", H5, N, "Defines an article"),
    ES("aside", H5, N, "Defines content aside from the page content"),
    ES("details", H5, N, "Defines additional details that the user can view or hide"),
    ES("dialog", H5, N, "Defines a dialog box or window"),
    ES("summary", H5, N, "Defines a visible heading for a <details> element"),
    ES("data", H5, N, "Links the given content with a machine-readable translation"),
    # Meta Info
    ES("head", HB, N, "Defines information about the document"),
    ES("meta", HB, E, "Defines metadata about an HTML document"),
    ES("base", HB, E, "Specifies the base URL/target for all relative URLs in a document"),
    ES("basefont", H4, N, "Not supported in HTML5. Use CSS instead. Specifies a default color, size, "
                          "and font for all text in a document"),
    # Programming
    ES("script", HB, N, "Defines a client-side script"),
    ES("noscript", HB, N, "Defines an alternate content for users that do not support client-side scripts"),
    ES("applet", H4, N, "Not supported in HTML5. Use <embed> or <object> instead. Defines an embedded applet"),
    ES("embed", H5, E, "Defines a container for an external (non-HTML) application"),
    ES("object", HB, N, "Defines an embedded object"),
    ES("param", HB, E, "Defines a parameter for an object")]

HTML4_ELEMENTS = [e for e in HTML_ELEMENTS if e.standard == H4 or e.standard == HB]
HTML5_ELEMENTS = [e for e in HTML_ELEMENTS if e.standard == H5 or e.standard == HB]

HTML_TAGS = {
    H4: [e.tag for e in HTML4_ELEMENTS],
    H5: [e.tag for e in HTML5_ELEMENTS],
}
CONTEXT_ELEMENTS = {
    H4: [ER(e.tag, e.info) for e in HTML4_ELEMENTS if e.type_ == N],
    H5: [ER(e.tag, e.info) for e in HTML5_ELEMENTS if e.type_ == N]
}

EMPTY_ELEMENTS = {
    H4: [ER(e.tag, e.info) for e in HTML4_ELEMENTS if e.type_ == E],
    H5: [ER(e.tag, e.info) for e in HTML5_ELEMENTS if e.type_ == E]
}
