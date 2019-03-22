import colorsys
import math
import os
import random

from yawrap import NavedYawrap, EmbedCss, EmbedJs


def make_random_data(hit_probability=0.1, max_frames=1024):
    assert 0.0 < hit_probability < 1.0

    for frame in range(max_frames):
        for sub_frame in range(10):
            if hit_probability > random.uniform(0, 1.0):
                mean = random.randint(2000, 2 ** 16 - 2000)  # 2 or 4 antennas
                antenna_power = [mean + random.randint(-2000, 2000) for _ in range(random.choice([2, 4]))]
                yield frame, sub_frame, antenna_power


TEST_DATA = [
    # TEST_DATA = list(make_random_data())
    (3, 9, [14457, 15025, 11557, 11674]),
    (10, 2, [50555, 49190]),
    (15, 2, [54671, 56954, 56002, 58069]),
    (18, 0, [42796, 40035]),
    (19, 4, [16389, 15203]),
    (29, 4, [55403, 52699]),
    (33, 1, [3654, 6138]),
    (47, 8, [14602, 14709]),
    (58, 4, [46450, 47549]),
    (69, 9, [7245, 7382, 10967, 10859]),
    (79, 9, [46524, 46454]),
    (85, 7, [22571, 22141, 24288, 22482]),
    (95, 5, [36231, 33559]),
    (105, 8, [38092, 38301]),
    (107, 9, [10947, 7909, 10112, 9682]),
    (118, 2, [38924, 38807]),
    (125, 2, [66927, 64972, 66053, 65515]),
    (127, 9, [27513, 27092]),
    (128, 4, [55438, 57552]),
    (130, 9, [14313, 15608]),
    (151, 4, [39559, 35762, 36089, 37118]),
    (161, 0, [35527, 34465, 35442, 35084]),
    (167, 6, [866, 341]),
    (174, 3, [285, 228, 667, 2577]),
    (180, 5, [1758, 2278]),
    (184, 7, [40020, 42077]),
    (187, 1, [53219, 52441]),
    (192, 3, [50683, 49216, 48512, 49855]),
    (199, 4, [30923, 30721]),
    (217, 8, [60211, 59842]),
    (219, 2, [53171, 50361, 52187, 51465]),
    (222, 4, [31982, 29384, 30502, 30018]),
    (232, 2, [33759, 34039]),
    (239, 9, [29416, 26608, 28967, 29021]),
    (240, 2, [33128, 30294, 31546, 33048]),
    (261, 3, [12932, 13531]),
    (271, 0, [10388, 10177, 9211, 7863]),
    (279, 8, [7231, 5610]),
    (284, 2, [33207, 30680, 29950, 29733]),
    (290, 2, [18529, 20379, 19145, 18139]),
    (298, 6, [57848, 59112, 59416, 59228]),
    (302, 5, [61347, 60491]),
    (322, 1, [49168, 49339]),
    (322, 8, [28147, 29211, 30902, 29586]),
    (325, 0, [44726, 44546, 44787, 44586]),
    (386, 6, [19376, 17331, 19686, 18461]),
    (404, 4, [29662, 29840]),
    (405, 5, [47493, 47728, 47934, 46822]),
    (422, 6, [41161, 43445, 42070, 43793]),
    (423, 5, [29953, 31858, 33289, 31222]),
    (425, 8, [14224, 15062, 16526, 14476]),
    (433, 6, [49436, 52624]),
    (473, 4, [57174, 56285]),
    (509, 6, [18081, 17395]),
    (518, 9, [44530, 46118, 47217, 47582]),
    (520, 0, [24049, 27508]),
    (543, 2, [52783, 50960]),
    (543, 5, [27123, 27516]),
    (550, 0, [32351, 33629]),
    (557, 8, [40000, 39010, 39043, 39278]),
    (562, 4, [26719, 24667]),
    (564, 1, [16171, 15468]),
    (564, 6, [3801, 3823]),
    (601, 2, [34902, 33338, 33513, 35246]),
    (602, 3, [39609, 40787, 40385, 42628]),
    (608, 9, [35258, 34828, 33025, 33337]),
    (610, 5, [59463, 60041]),
    (614, 2, [55082, 55663]),
    (620, 9, [38843, 39820, 40687, 38173]),
    (629, 3, [47970, 49671]),
    (637, 6, [35165, 32944]),
    (641, 2, [16409, 16487, 16273, 12992]),
    (648, 8, [51294, 49646]),
    (653, 8, [20880, 17896]),
    (655, 8, [11423, 11374, 8170, 8613]),
    (658, 1, [40343, 38879, 38903, 39386]),
    (668, 7, [47582, 48113]),
    (676, 9, [55853, 52272]),
    (677, 0, [49641, 49792]),
    (683, 9, [37911, 38076]),
    (687, 1, [54172, 52644, 52742, 50891]),
    (702, 9, [55686, 55336, 58367, 55358]),
    (713, 4, [35553, 33391]),
    (714, 1, [19932, 17431, 18068, 17020]),
    (718, 1, [52207, 50006, 51665, 51292]),
    (724, 1, [1365, -1329]),
    (746, 1, [43603, 43412]),
    (752, 6, [44849, 46457, 42933, 44974]),
    (754, 2, [60455, 60731]),
    (755, 1, [60853, 60887, 61021, 58521]),
    (772, 5, [22370, 21851, 18904, 20656]),
    (779, 6, [52081, 51952]),
    (796, 3, [63323, 64375, 64529, 62183]),
    (808, 8, [66518, 66715, 66260, 65305]),
    (810, 7, [22665, 20433, 23576, 21342]),
    (810, 9, [723, 1403, -57, -1018]),
    (829, 6, [5878, 4755, 4261, 5930]),
    (831, 9, [52834, 50486, 51241, 53117]),
    (838, 9, [4000, 3910]),
    (841, 5, [62661, 62111]),
    (855, 6, [42795, 42946]),
    (856, 3, [48538, 44866]),
    (871, 0, [54292, 52098, 51672, 54020]),
    (878, 3, [54439, 56160]),
    (881, 7, [33590, 32065, 32894, 32616]),
    (882, 3, [8078, 8796]),
    (888, 4, [40459, 40173, 43279, 40404]),
    (889, 6, [20992, 21543, 21494, 22235]),
    (900, 2, [17936, 17843]),
    (901, 4, [3699, 1359, 4219, 4079]),
    (908, 0, [31834, 29213, 30787, 29580]),
    (908, 1, [54215, 55677, 55719, 56068]),
    (933, 6, [41209, 41579]),
    (945, 5, [10249, 7711, 9586, 8363]),
    (948, 2, [28225, 30926]),
    (949, 8, [55336, 54704]),
    (953, 9, [56850, 59633]),
    (966, 0, [13264, 15303]),
    (966, 7, [11190, 13702, 11954, 11218]),
    (970, 9, [62610, 63943]),
    (976, 0, [8746, 8412, 5969, 5549]),
    (982, 2, [58112, 59248, 55855, 58710]),
    (991, 8, [60631, 59550, 62695, 58815]),
    (999, 7, [17358, 18929]),
    (1000, 9, [33154, 32514, 31495, 30468]),
    (1005, 7, [137, 2094]),
]


def dB(value, base=2.0 ** 16):
    value = min(base, max(1, value))
    return round(-20.0 * math.log(base / float(value), 10), 3)


def int16_to_log_color(value_u16, lightness=0.6, saturation=0.5):
    int16_base = 2.0 ** 16
    value_db = dB(value_u16, int16_base)
    minimum = dB(0)
    maximum = dB(int16_base)
    return warm_cool_color(value_db, minimum, maximum, lightness, saturation)


def warm_cool_color(value, minimum, maximum, lightness=0.4, saturation=0.7):
    # value is linear - it casts it over min:max scale (scale can be inverted)
    # hue = 0 or 1.0 is red, 0.33 is green, 0.66 is blue
    relative_value = (value - minimum) / float(maximum - minimum)
    # let's make minimum - blue: 0.66, and max - red at 1.0
    hue = 0.5 + 0.5 * relative_value
    return color_from_hue(hue, lightness, saturation)


def color_from_hue(hue, lightness=0.4, saturation=0.7):
    # hue = 0 or 1.0 is red, 0.33 is green, 0.66 is blue
    hue = min(1.0, max(0.0, hue))
    col = colorsys.hls_to_rgb(hue, lightness, saturation)
    return "#%02x%02x%02x" % tuple(min(255, int(c * 255)) for c in col)


def test_color():
    for k in range(10):
        int16_to_log_color(2 ** k)


def get_ant_data(dumps, frame, sub_frame):
    for f, s, antennas in dumps:
        if f == frame and s == sub_frame:
            return antennas


CSS = """\
    body {
        margin: 0;
        font-family: Verdana, sans-serif;
    }
    td {
        padding: 5px;
    }
    .ant_table_svg {
    }
    .legend {
        padding: 1px;
        margin: 1px;
        border-radius: 2px;
    }
    .ant_pow_val td {
        padding: 7px;
        margin: 2px;
    }
    .nav_main_panel {
        list-style-type: none;
        margin: 0;
        padding: 0;
        width: 17%;
        background-color: #f1f1f1;
        position: fixed;
        height: 100%;
        overflow: auto;
    }
    .nav_group_div a {
        display: block;
        color: #000;
        padding: 8px 16px;
        text-decoration: none;
    }

    .nav_group_div a.active {
        background-color: #4CAF50;
        color: white;
    }
    .nav_group_div.active {
        background-color: #fdf8fa;
        color: white;
    }
    .nav_page.with_bookmarks {
        background: #DDD;
    }
    .nav_group_div a:hover:not(.active) {
        background-color: #555;
        color: white;
    }
    .main_content_body {
        margin-left:17%;
        padding:1px 16px;
    }
    #tooltip {
        background: #e6e6e6;
        border: 1px solid #abc;
        border-radius: 3px;
        padding: 5px;
    }
"""

SVG_JS = """
function showTT(evt, text) {
  let tooltip = document.getElementById("tooltip");
  tooltip.innerHTML = text;
  tooltip.style.display = "block";
  tooltip.style.left = evt.pageX + 10 + 'px';
  tooltip.style.top = evt.pageY + 10 + 'px';
}

function hideTT() {
  var tooltip = document.getElementById("tooltip");
  tooltip.style.display = "none";
}
"""


class AntennaDataView(NavedYawrap):
    resources = [
        EmbedCss(CSS),
        EmbedJs(SVG_JS),
    ]

    def fill_sub_page(self, fr, sf, powers):
        with self.tag("h3"):
            self.text("Antenna Dump %s.%s" % (fr, sf))

        with self.tag("table", klass="ant_pow_val"):
            with self.tag("tr"):
                self.line("td", "Frame:")
                self.line("td", str(fr))
            with self.tag("tr"):
                self.line("td", "Sub-frame")
                self.line("td", str(sf))
            with self.tag("tr"):
                self.line("td", "lnCellId")
                self.line("td", "166")

            for i, power in enumerate(powers):
                with self.tag("tr"):
                    self.line("td", "Antenna %d mean power" % i)
                    style = "background-color:%s;" % int16_to_log_color(power)
                    self.line("td", "%.2f dB (%s)" % (dB(power), power), style=style)


def test_basic_svg(out_dir):
    target_file = os.path.join(out_dir, 'index.html')
    visualize_dumps(target_file, TEST_DATA)


def visualize_dumps(target_file, input_data):
    max_frames = 1024
    sub_frames_in_frame = 10
    entry_height = 9
    frames_per_row = 10
    img_virtual_width = 1200

    rect_padding = 0.1 * entry_height
    radius = "%.2f" % (0.1 * entry_height)
    total_entries = max_frames * sub_frames_in_frame
    entries_per_row = float(frames_per_row * sub_frames_in_frame)
    img_virtual_height = (total_entries + entries_per_row - 1) / entries_per_row * entry_height
    entry_width = img_virtual_width / entries_per_row
    half_padding = rect_padding / 2.0

    j = AntennaDataView(target_file, "Snapshot Table")

    with j.tag("h3"):
        j.text("Antenna data snapshot table")

    with j.tag("table", width="100%"):
        with j.tag("tr"):
            j.line("td", "collected at")
            j.line("td", "2019-03-21 12:34:53")
        with j.tag("tr"):
            j.line("td", "snapshot file name")
            j.line("td", "Snapshot_MRATS-72992_0000_000452_000043_L2R-20171113-1406_60us.zip")

    with j.tag("table", width="100%"):
        with j.tag("tr"):
            for k in range(8):
                value = 2.0 ** (2 * (k + 1))
                with j.tag("td", style="padding: 0px;"):
                    style = "background-color: %s;" % int16_to_log_color(value)
                    with j.tag("div", align="center", width="100%", klass="legend", style=style):
                        j.text("%.0f dB" % dB(value))

    j.line("div", id="tooltip", display="none", style="position: absolute; display: none;")
    view_box = "0 0 %s %s" % (img_virtual_width, img_virtual_height)
    with j.svg(width="100%", height="100%", klass="ant_table_svg", viewBox=view_box):
        j.line('rect', width="100%", height="100%", fill="#f1f1f1", stroke_color="#dadada")

        for frame in range(max_frames):
            for sub_frame in range(sub_frames_in_frame):

                antennas = get_ant_data(input_data, frame, sub_frame)
                if not antennas:
                    continue

                sub_file_path = j.calc_rel_path("plots", 'ant_%04d_%02d.html' % (frame, sub_frame))
                sub_title = "Frame: %d.%d" % (frame, sub_frame)
                sub = j.sub(sub_file_path, sub_title)
                sub.fill_sub_page(frame, sub_frame, antennas)

                num_of_antennas = float(len(antennas))

                abs_entry_index = frame * sub_frames_in_frame + sub_frame
                col_index = abs_entry_index % entries_per_row
                row_index = abs_entry_index // entries_per_row
                ant_height = (entry_height - rect_padding) / num_of_antennas

                x = col_index * entry_width + half_padding
                y0 = row_index * entry_height + half_padding

                with j.local_link(sub_file_path, onmousemove="showTT(evt, '%s');" % sub_title, onmouseout="hideTT();"):
                    for yi, antenna_power in enumerate(antennas):
                        y = y0 + yi * entry_height / num_of_antennas
                        fill = int16_to_log_color(antenna_power)

                        w = entry_width - rect_padding
                        j.line('rect', x=x, y=y, width=w, height=ant_height, rx=radius, ry=radius, fill=fill)

            x = ((frame * sub_frames_in_frame) % entries_per_row) * entry_width
            y = ((frame * sub_frames_in_frame) // entries_per_row) * entry_height
            j.line("line", x1=x, x2=x, y1=y + rect_padding, y2=y + entry_height - half_padding, stroke="#888")

    j.render_all_files()
