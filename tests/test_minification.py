import pytest
import re
import time

from yawrap import HtmlFormatter
from yawrap._yawrap import Yawrap
from yawrap._formatter import _HtmlFormatterOption


SAMPLE_1_PRETTY = """\
<!doctype html>
<html lang="en-US">
  <head>
    <meta charset="UTF-8" />
    <title>title</title>
    <style>
    main {
        color: #b0baba;
    }</style>
  </head>
  <body>
    <div class="thing">
      <div id="00">that 00</div>
      <div id="01">that 01</div>
      <div id="02">that 02</div>
      <div id="03">that 03</div>
    </div>
    <div class="thing">
      <div id="10">that 10</div>
      <div id="11">that 11</div>
      <div id="12">that 12</div>
      <div id="13">that 13</div>
    </div>
    <div class="thing">
      <div id="20">that 20</div>
      <div id="21">that 21</div>
      <div id="22">that 22</div>
      <div id="23">that 23</div>
    </div>
  </body>
</html>"""

SAMPLE_1_MIN = re.sub("\s*\>\n\s*\<", "><", SAMPLE_1_PRETTY)

SAMPLE_1_LIMITTED_W = """\
<!doctype html><html lang="en-US"><head><meta charset="UTF-8" /><title>title</title><style>
    main {
        color: #b0baba;
    }</style></head><body><div class="thing"><div id="00">that 00</div><div id="01">that 01</div><div id="02">that 02</div>
<div id="03">that 03</div></div><div class="thing"><div id="10">that 10</div><div id="11">that 11</div><div id="12">that 12</div><div id="13">that 13</div></div><div class="thing"><div id="20">that 20</div><div id="21">that 21</div><div id="22">
that 22</div><div id="23">that 23</div></div></body></html>"""  # noqa: E501

SAMPLE_1_NEWLINES = """\
<!doctype html><html lang="en-US"><head><meta charset="UTF-8" /><title>title</title>
<style>
    main {
        color: #b0baba;
    }</style>
</head>
<body><div class="thing"><div id="00">that 00</div>
<div id="01">that 01</div>
<div id="02">that 02</div>
<div id="03">that 03</div>
</div>
<div class="thing"><div id="10">that 10</div>
<div id="11">that 11</div>
<div id="12">that 12</div>
<div id="13">that 13</div>
</div>
<div class="thing"><div id="20">that 20</div>
<div id="21">that 21</div>
<div id="22">that 22</div>
<div id="23">that 23</div>
</div>
</body>
</html>
"""

MINIFICATION_TEST = [
    (HtmlFormatter.yattag_indent, SAMPLE_1_MIN, SAMPLE_1_PRETTY),
    (HtmlFormatter.no_indent, SAMPLE_1_PRETTY, SAMPLE_1_MIN),
    (HtmlFormatter.limited_line_width, SAMPLE_1_MIN, SAMPLE_1_LIMITTED_W),
    (HtmlFormatter.new_line_each_end, SAMPLE_1_MIN, SAMPLE_1_NEWLINES),
]


@pytest.mark.parametrize("min_option, input_html, reference_result", MINIFICATION_TEST,
                         ids=[str(i[0]) for i in enumerate(MINIFICATION_TEST)])
def test_minification(min_option, input_html, reference_result):

    Yawrap.html_formatter = min_option
    raw_text_result = Yawrap.html_formatter(input_html)
    assert raw_text_result == reference_result


@pytest.fixture(scope="module")
def a_huge_page():
    class MyRap(Yawrap):
        def make_huge_page(self):
            for _ in range(30):
                with self.tag("div", klass="quite_long_class_name"):
                    for __ in range(30):
                        for ___ in range(30):
                            self.text("That is a frequently occurring text.")

    rap = MyRap("", "")
    rap.make_huge_page()
    return rap


def test_check_timings(a_huge_page):

    def measure_exec_time(current_formatter):
        a_huge_page.__class__.html_formatter = current_formatter
        start = time.clock()
        a_huge_page._render_page()
        stop = time.clock()
        return stop - start

    timings = _HtmlFormatterOption(*map(measure_exec_time, HtmlFormatter))

    performance_order_as_assumed = (timings == tuple(sorted(timings)))
    assert performance_order_as_assumed, "\n".join([
        "", "WARNING:", "Seems that html formatter's performance is different than assumed.",
        "That list is supposed to be in order of execution time:", "",
        "\n".join("%-36s takes %0.3fms" % ("HtmlFormatter.%s()" % n, t * 1000)
                  for n, t in zip(timings._fields, timings)), "",
        "Skip that test if it's a problem.", "",
    ])
