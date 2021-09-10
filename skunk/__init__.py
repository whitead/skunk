from os import replace
from matplotlib.offsetbox import DrawingArea
from matplotlib.patches import Rectangle
import io
import matplotlib.pyplot as plt
import matplotlib as mpl
import xml.etree.ElementTree as ET
import os


class Box(DrawingArea):
    """A subclass of matplotlib DrawingArea that can be replaced
    """

    def __init__(self, width, height, gid):
        super().__init__(width, height)
        p = Rectangle((0, 0), width, height)
        self.add_artist(p)
        p.set_gid(gid)


def connect(ax, gid):
    """Adds a rectangle to given matplotlib artist that can be replaced

    :param ax: matplotlib artist that has `add_artist`, like axes
    :param gid: string that is used for key to replace later
    """
    p = Rectangle((0, 0), 1, 1)
    ax.add_artist(p)
    p.set_gid(gid)


def pltsvg(fig=None, **kwargs):
    """Outputs current SVG of matplotlib figure.

    :para fig: If `fig=None`, it extracts from current figure.
    :param: forwarded to `savefig`
    :returns: SVG as `str`
    """
    with io.BytesIO() as output:
        if fig is None:
            plt.savefig(output, format='svg', **kwargs)
        else:
            fig.savefig(output, format='svg', **kwargs)
        return output.getvalue().decode()


def display(svg):
    """A convenience function to dispaly SVG string in Jupyter Notebook
    """
    import IPython.display as display
    import base64
    data = base64.b64encode(svg.encode('utf8'))
    display.display(display.HTML('<img src=data:image/svg+xml;base64,' + data.decode() + '>'))


def _extract_loc(e):
    path = e.attrib['d']
    spath = path.split()
    x, y = [], []
    a1, a2 = x, y
    for s in spath:
        try:
            a1.append(float(s))
            a1, a2 = a2, a1
        except ValueError:
            continue
    return min(x), min(y), max(x) - min(x), max(y) - min(y)


def _rewrite_svg(svg, rdict):
    ns = "http://www.w3.org/2000/svg"
    root, idmap = ET.XMLID(svg)
    parent_map = {c: p for p in root.iter() for c in p}
    for rk, rv in rdict.items():
        if rk in idmap:
            e = idmap[rk]
            # try to use id width/height
            # case when we have image
            if 'width' in e.attrib:
                x, y = e.attrib['x'], -float(e.attrib['y'])
                # make new node
                # to hold things
                new_e = ET.SubElement(
                    parent_map[e], f'{{{ns}}}g', {'id': f'{rk}-g'})
                parent_map[e].remove(e)
                dx, dy = float(e.attrib['width']), float(e.attrib['height'])
                e = new_e
            else:
                # relying on there being a path object inside to give clue
                # to size
                c = list(e)[0]
                x, y, dx, dy = _extract_loc(c)
                e.remove(c)
            # set attributes on SVG so loc and width/height are correct
            try:
                rr = ET.fromstring(rv)
            except ET.ParseError:
                raise ValueError('Your given replacement object is not valid SVG (perhaps filepath was not valid?)')
            rr.attrib['x'] = str(x)
            rr.attrib['y'] = str(y)
            rr.attrib['width'] = str(dx)
            rr.attrib['height'] = str(dy)
            e.insert(0, rr)
        else:
            raise UserWarning('Warning, could not find skunk key', rk)
    ET.register_namespace("", ns)
    return ET.tostring(root, encoding="unicode", method='xml')


def insert(replacements, svg=None):
    """Replaces elements by `id` in `svg`

    :param replacements: Dictionary where key is id from :class:`Box` or :func:`connect`.
        Value is :class:`matplotlib.figure.Figure`, path to SVG file, or `str` of SVG.
    :param svg: SVG text that will be modified. If `None`, current matplotlib figure will be used.
    :returns: SVG as string
    """
    if svg is None:
        svg = pltsvg()
    if type(replacements) != dict:
        raise ValueError('Must pass dictionary of skunk id: svg')
    # check over keys to figure out types
    for k in replacements:
        if type(replacements[k]) == mpl.figure.Figure:
            replacements[k] = pltsvg(replacements[k])
        elif type(replacements[k]) == str and os.path.exists(replacements[k]):
            with open(replacements[k]) as f:
                replacements[k] = f.read()

    # ok now do it
    svg = _rewrite_svg(svg, replacements)
    return svg
