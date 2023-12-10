"""
Code for converting ASCII art to SVG format.
"""

"""
Globals
"""
###
### Javascript code to inject into the SVGs to ensure consistent size
###
# JS to ensure that bounding rectangle fits the text
RECTANGULAR_SVG_JS_INJECT = """\
window.addEventListener('load',function() {
    var bounding_rect = document.getElementById("bounding-rect");
    var text = document.getElementById("ascii");
    var bb_text = text.getBBox();
    // Change the rectangle size to fit the text
    bounding_rect.setAttribute("width", bb_text.width);
    bounding_rect.setAttribute("height", bb_text.height);
}, false);"""

# JS to make text element square
SQUARE_SVG_JS_INJECT = """\
window.addEventListener('load',function() {
    var bounding_rect = document.getElementById("bounding-rect");
    var text = document.getElementById("ascii");
    var bb_text = text.getBBox();
    // Change the font size so that the height and width match up
    var font_size = Math.round(1e3 * bb_text.height / bb_text.width) / 1e3;
    text.setAttribute("font-size", font_size + "px");
    // Adjust size of bounding rectangle
    bb_text = text.getBBox();
    bounding_rect.setAttribute("width", bb_text.width);
    bounding_rect.setAttribute("height", bb_text.height);
}, false);"""

"""
ASCII -> SVG conversion
"""


def ascii_to_svg(txt):
    """
    Takes an ASCII text string and converts it into an SVG image.
    """
    # Do a search-and-replace for characters that will create rendering
    # isssues.
    # txt = txt.replace("&", "&amp;")
    # txt = txt.replace('"', "&quot;")
    # txt = txt.replace("<", "&lt;")
    # txt = txt.replace(">", "&gt;")
    # txt = txt.replace(" ", "&#160;")

    lines = txt.split("\n")
    width = len(lines[0])
    height = len(lines)

    svg_start = f"""\
<!DOCTYPE html>
<html>
<body>
<meta charset="ASCII">

<svg height="{height}" width="{width}">
    """

    svg_middle = ""
    svg_end = """\
</svg>
</body>
</html>"""

    # Add <tspan> elements in the middle
    dy = round(100 / len(lines), 3)
    y = dy
    for (ii, line) in enumerate(lines):
        middle = f"""<text x="0" dy="{y:0.3f}%" fill="black" xml:space="preserve">{line}</text>"""
        svg_middle += middle + "\n"
        y += dy

    return svg_start + svg_middle + svg_end