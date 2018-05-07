
from yawrap import Yawrap, ExternalJs, EmbedCss, EmbedJs, BODY_END


class MyPageTemplate(Yawrap):
    resources = [
        ExternalJs("https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"),
        EmbedCss("""
        body {
            padding: 12px;
            font-family: helvetica, sans-serif;
            font-size: 14px;
        }
        .box {
            display: inline-block;
            height: 80px;
            margin: 8px;
            padding: 8px;
            width: 80px;
        }
        """),
        EmbedJs("""
        $("button").click(function(){
            $("#red-box").fadeToggle();
            $("#green-box").fadeToggle("slow");
            $("#blue-box").fadeToggle(3000);
        });
        """, placement=BODY_END),
    ]

    def _create_box(self, name, color):
        style = "background-color:{};".format(color)
        with self.tag('div', id=name, klass="box", style=style):
            self.text(name)

    def fill_with_content(self):
        with self.tag("h2"):
            self.text("Demonstrate a simple JavaScript.")

        with self.tag('p'):
            self.text("fadeToggle() operating with different speed parameters.")

        with self.tag('button'):
            self.text("Click to fade in/out boxes")

        with self.tag("div"):
            self._create_box('red-box', "red")
            self._create_box('green-box', "#0f0")
            self._create_box('blue-box', "#0a1cf0")


def create_page(output_file_path):
    doc = MyPageTemplate(output_file_path, "Name of the page")
    doc.fill_with_content()
    doc.render()

# that's it

# end section A


from yawrap import LinkCss, LinkJs


class MyPage(MyPageTemplate):
    resources = [
        ExternalJs("https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"),
        LinkCss("""\
        body {
            padding: 12px;
            font-family: helvetica, sans-serif;
            font-size: 14px;
        }
        .box {
            display: inline-block;
            height: 80px;
            margin: 8px;
            padding: 8px;
            width: 80px;
        }""", file_name="common_linked.css"),
        LinkJs("""\
        $("button").click(function(){
            $("#red-box").fadeToggle();
            $("#green-box").fadeToggle("slow");
            $("#blue-box").fadeToggle(3000);
        });
        """, placement=BODY_END, file_name="common_linked.js"),
    ]

    # uses methods inherited from MyPageTemplate defined above


def create_page_with_linked_resources(output_file_path):
    doc = MyPage(output_file_path)
    doc.fill_with_content()
    doc.render()


# end section B

from exampling_tools import get_output_file_path


def test_that():
    output_file_path = get_output_file_path("test_usage_01.html")
    create_page(output_file_path)

    with open(output_file_path, "rt") as f:
        assert f.read() == """\
<!doctype html><html lang='en-US'>
  <head>
    <meta charset='UTF-8' />
    <title>Name of the page</title>
    <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js'></script>
    <style>

        body {
            padding: 12px;
            font-family: helvetica, sans-serif;
            font-size: 14px;
        }
        .box {
            display: inline-block;
            height: 80px;
            margin: 8px;
            padding: 8px;
            width: 80px;
        }
        
    </style>
  </head>
  <body>
    <h2>Demonstrate a simple JavaScript.</h2>
    <p>fadeToggle() operating with different speed parameters.</p>
    <button>Click to fade in/out boxes</button>
    <div>
      <div class='box' id='red-box' style='background-color:red;'>red-box</div>
      <div class='box' id='green-box' style='background-color:#0f0;'>green-box</div>
      <div class='box' id='blue-box' style='background-color:#0a1cf0;'>blue-box</div>
    </div>
    <script type='text/javascript'>

        $("button").click(function(){
            $("#red-box").fadeToggle();
            $("#green-box").fadeToggle("slow");
            $("#blue-box").fadeToggle(3000);
        });
        
    </script>
  </body>
</html>"""


def test_linked_resources():
    output_file_path = get_output_file_path("test_usage_01_linked.html")
    create_page_with_linked_resources(output_file_path)
