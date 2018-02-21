'''
las = linking and sourcing of external files
'''
from yawrap import Yawrap
from yawrap._sourcer import ExtenalJs, ExtenalCss, EmbedCss, LinkJs, BODY_BEGIN, BODY_END


def test_one():

    class MyClass(Yawrap):
        resources = [
            EmbedCss.from_str("body { color: #DAF; }", BODY_BEGIN),
            LinkJs.from_url("https://invalid.address.com/want/to/have/it/in/head.js"),
            LinkJs.from_url("https://invalid.address.com/want/to/have/it/at_body_beggining.js", BODY_BEGIN),
            LinkJs.from_url("https://invalid.address.com/want/to/have/it/at_body_end.js", BODY_END),
            ExtenalJs("https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"),
            ExtenalCss("https://www.w3schools.com/w3css/4/w3.css"),
        ]

    doc = MyClass("/tmp/that_file.html", "that title")

    with doc.tag("p"):
        doc.text("The body content")

    print(doc._render_page())
