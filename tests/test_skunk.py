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
    ax.add_artist(ab)

    box = skunk.Box(50, 50, 'sk2')
    ab = AnnotationBbox(box, (3 * np.pi / 2, -1),
                        xybox=(-5, 100),
                        xycoords='data',
                        boxcoords="offset points",
                        arrowprops=dict(arrowstyle="->"))

    ax.add_artist(ab)

    svg = skunk.insert(
        {
            'sk1': skunk.pltsvg(),
            'sk2': os.path.join(os.path.dirname(os.path.realpath(__file__)), 'skunk.svg')
        })

    with open('test-skunk.svg', 'w') as f:
        f.write(svg)


def test_skunk2():
    import numpy as np

    fig, axs = plt.subplots(ncols=2, squeeze=True)

    x = np.linspace(0, 2 * np.pi)
    axs[0].plot(x, np.sin(x))
    skunk.connect(axs[1], 'sk')
    plt.tight_layout()
    svg = skunk.pltsvg()

    for _ in range(5):
        svg = skunk.insert(
            {
                'sk': svg
            })

    with open('test-skunk2.svg', 'w') as f:
        f.write(svg)
