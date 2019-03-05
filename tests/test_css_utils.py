from yawrap.utils import form_css

RAW_CSSs = """
      .a_div a {
        color: #000;
        display: block;
        padding: 8px 16px;
        text-decoration: none;
      }
      .a_div a.active {
        background-color: #4CAF50;
        color: white;
      }
      .a_div a:hover:not(.active) {
        background-color: #555;
        color: white;
      }
      .a_div.active {
        background-color: #fdf8fa;
        color: white;
      }
      .a_div_b.with_bookmarks {
        background: #DDD;
      }
      .main_content_body {
        height: 1000px;
        margin-left: 25%;
        padding: 1px 16px;
      }"""

STRUCTURIZED_CSS = {
    '.main_content_body': {
        'height': '1000px',
        'margin-left': '25%',
        'padding': '1px 16px'
    },
    '.a_div a': {
        'color': '#000',
        'display': 'block',
        'padding': '8px 16px',
        'text-decoration': 'none'
    },
    '.a_div a.active': {
        'background-color': '#4CAF50',
        'color': 'white'
    },
    '.a_div a:hover:not(.active)': {
        'background-color': '#555',
        'color': 'white'
    },
    '.a_div.active': {
        'background-color': '#fdf8fa',
        'color': 'white'
    },
    '.a_div_b.with_bookmarks': {
        'background': '#DDD'
    }
}


def test_forming_empty_css_from_empty_dict():
    assert '' == form_css({})


def test_forming_empty_css2_from_empty_str():
    assert '' == form_css("")


def test_forming_css_with_empty_rule():
    assert form_css({'selector': {}}) == '\n  selector {}'


def test_forming_css():
    result = form_css(STRUCTURIZED_CSS, indent_level=3)
    assert result == RAW_CSSs
