import os

from yawrap import Yawrap


def draw_sample_svg(painter_doc, points="50,150 50,200 200,200 200,100"):
    painter_doc.stag('rect', x="25", y="25", width="200", height="200", klass='the_rect')
    painter_doc.stag('circle', cx="125", cy="125", r="75", fill="orange")
    painter_doc.stag('polyline', points=points, stroke="red", fill="none", stroke_width=4)
    painter_doc.stag('line', x1="50", y1="50", x2="200", y2="200", stroke="blue", stroke_width="4")


def test_basic_svg(out_dir):
    target_file = os.path.join(out_dir, 'basic.html')
    jarap = Yawrap(target_file)
    with jarap.svg(width=260, height=260, svg_styles_as_str=".the_rect {fill: lime; stroke-width: 4; stroke: pink;}"):
        draw_sample_svg(jarap)

    assert jarap._render_page() == """\
<!doctype html><html lang='en-US'>
  <head><meta charset='UTF-8' /></head>
  <body>
    <svg height=260 version='1.1' width=260 xmlns='http://www.w3.org/2000/svg'>
      <style type='text/css'><![CDATA[.the_rect {fill: lime; stroke-width: 4; stroke: pink;}]]></style>
      <rect class='the_rect' height='200' width='200' x='25' y='25' />
      <circle cx='125' cy='125' fill='orange' r='75' />
      <polyline fill='none' points='50,150 50,200 200,200 200,100' stroke='red' stroke-width=4 />
      <line stroke='blue' stroke-width='4' x1='50' x2='200' y1='50' y2='200' />
    </svg>
  </body>
</html>"""
