
from yawrap import NavedYawrap, EmbedCss
from collections import namedtuple

Deploy = namedtuple("Deploy", "as_internal_content, as_local_link, as_web_url")
RS = namedtuple("RS", "css, js")
Info = namedtuple("Info", "code, note")


class ResourceInfoPage(NavedYawrap):
    resources = [
        EmbedCss("""
        body { padding: 12px; font-family: Arial, Helvetica, sans-serif; }
        table, th, td { border: 1px solid #b0baba; border-collapse: collapse; }
        tr, td { padding: 10px 8px; }
        ul { margin: 2px; padding: 2px 2px 2px 14px; }
        th { padding: 16px 8px; }
        .header { padding: 15px; font-weight: bold; }
        .code { padding: 4px; font-family: "Lucida Console", Monaco, monospace; font-size: 85%; color: #060; }""")
    ]


def build_the_table(doc, header, data):
    with doc.tag("table"):

        for elem_idx, type_name in enumerate(RS._fields):
            with doc.tag("tr"):
                with doc.tag("td", klass="header", colspan=4):
                    doc.text(type_name)

            with doc.tag("tr"):
                with doc.tag("th"):
                    doc.text('Source')
                for column in header:
                    with doc.tag("th"):
                        doc.text(column[elem_idx])

            for row in data:
                with doc.tag("tr"):
                    with doc.tag("td"):
                        doc.text(str(row["source"]))
                    for column in row["deploy"]:
                        code = column[elem_idx]
                        with doc.tag("td"):
                            if code is not None:
                                with doc.tag("ul"):
                                    for code_line in code.code:
                                        with doc.tag("li", klass="code"):
                                            doc.text(code_line)
                                with doc.tag("div"):
                                    doc.text(code.note)
                            else:
                                doc.text("Not applicable")


HEADER = Deploy(
    as_internal_content=RS(
        css="Embed / Insert style sheet into html page.",
        js="Embed / Insert java script into html page."
    ),
    as_local_link=RS(
        css="Reference style sheet file as local resource",
        js="Reference java script file as local resource"
    ),
    as_web_url=RS(
        css="Reference style sheet file by it's url",
        js="Reference java script file by it's url"
    ),
)

GUIDE = [
    {
        "source": "from string",
        "deploy": Deploy(
            as_internal_content=RS(
                css=Info(["EmbedCss(the_style_as_string)"], ""),
                js=Info(["EmbedJs(the_script_as_string)"], "")
            ),
            as_local_link=RS(
                css=Info([
                    "LinkCss(the_style_as_string, file_name = 'file_name.css')",
                ], "Providing the file name is required."),
                js=Info([
                    "LinkJs(the_script_as_string, file_name='file_name.js')",
                    "LinkJs(the_script_as_string, file_name='file_name.js', placement=yawrap.BODY_BEGIN)",
                    "LinkJs(the_script_as_string, file_name='file_name.js', placement=yawrap.BODY_END)",
                ], "Providing the file name is required. By default the link will appear in head. "
                    "You can select different placement if needed.")
            ),
            as_web_url=RS(
                css=None,
                js=None
            )
        )
    },
    {
        "source": "from local file",
        "deploy": Deploy(
            as_internal_content=RS(
                css=Info(["EmbedCss.from_file('/path/to/the_source.css')"], "The file must exist"),
                js=Info([
                    "EmbedJs.from_file('/path/to/the_source.js')",
                    "EmbedJs.from_file('/path/to/the_source.js', placement=yawrap.BODY_END)"],
                    "The source file must exist. You can change placement (HEAD is default)"),
            ),
            as_local_link=RS(
                css=Info([
                    "LinkCss.from_file('/path/to/the_source.css')",
                    "LinkCss.from_file('/path/to/the_source.css', file_name='different_name.css')",
                ], "By default - target file name is same as the source's name. Name can be changed."),
                js=Info([
                    "LinkJs.from_file('/path/to/the_source.js')",
                    "LinkJs.from_file('/path/to/the_source.js', file_name='different_name.js')",
                    "LinkJs.from_file('/path/to/the_source.js', file_name='different_name.js', placement=yawrap.BODY_BEGIN)",
                    "LinkJs.from_file('/path/to/the_source.js', file_name='different_name.js', placement=yawrap.BODY_END)",
                ], "The source file must exist. You can change the name or the link placement (HEAD is default)")
            ),
            as_web_url=RS(
                css=None,
                js=None
            )
        )
    },
    {
        "source": "from the web",
        "deploy": Deploy(
            as_internal_content=RS(
                css=Info(["EmbedCss.from_url('https://url.to/the.style.css')"], ""),
                js=Info(["EmbedJs.from_url('https://url.to/the.script.js')"], "")
            ),
            as_local_link=RS(
                css=Info([
                    "LinkCss.from_url('https://url.to/the.style.css')",
                    "LinkCss.from_url('https://url.to/the.style.css', file_name='different_name.css')",
                ], ""),
                js=Info([
                    "LinkJs.from_url('https://url.to/the.script.js')",
                    "LinkJs.from_url('https://url.to/the.script.js', file_name='different_name.css.js')",
                    "LinkJs.from_url('https://url.to/the.script.js', file_name='different_name.css.js', placement=yawrap.BODY_END)",
                ], "")
            ),
            as_web_url=RS(
                css=Info(["ExternalCss('https://url.to/the.style.css')"], ""),
                js=Info(["ExternalJs('https://url.to/the.script.js')"], "")
            )
        )
    },
]


def test_that():
    from exampling_tools import get_output_file_path  # need it to make this docs building
    doc = ResourceInfoPage(get_output_file_path("test_usage_02.html"))

    build_the_table(doc, HEADER, GUIDE)

    doc.render()
