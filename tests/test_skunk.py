from matplotlib.offsetbox import AnnotationBbox
import skunk
import numpy as np
import os
import matplotlib.pyplot as plt


def test_setup():
    import numpy as np

    fig, ax = plt.subplots(figsize=(300/72, 300/72))

    x = np.linspace(0, 2 * np.pi)
    ax.plot(x, np.sin(x))

    box = skunk.Box(50, 50, 'sk1')
    ab = AnnotationBbox(box, (np.pi / 2, 1),
                        xybox=(-5, -100),
                        xycoords='data',
                        boxcoords="offset points",
                        arrowprops=dict(arrowstyle="->"))

    ax.add_artist(ab)
    with open('test-setup.svg', 'w') as f:
        f.write(skunk.pltsvg())


def test_skunk():
    import numpy as np

    fig, ax = plt.subplots(figsize=(300/72, 300/72))

    x = np.linspace(0, 2 * np.pi)
    ax.plot(x, np.sin(x))

    box = skunk.Box(50, 50, 'sk1')
    ab = AnnotationBbox(box, (np.pi / 2, 1),
                        xybox=(-5, -100),
                        xycoords='data',
                        boxcoords="offset points",
                        arrowprops=dict(arrowstyle="->"))

    box = skunk.Box(50, 50, 'sk2')
    ab = AnnotationBbox(box, (3 * np.pi / 2, 1),
                        xybox=(-5, 100),
                        xycoords='data',
                        boxcoords="offset points",
                        arrowprops=dict(arrowstyle="->"))

    ax.add_artist(ab)

    svg = skunk.insert(
        {
            'sk1': skunk.pltsvg(),
            'sk2': os.path.join(os.path.realpath(__file__), 'skunk.svg')
        })

    with open('test-skunk.svg', 'w') as f:
        f.write(svg)
