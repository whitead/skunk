# skunk  <img src="https://raw.githubusercontent.com/whitead/skunk/main/tests/skunk.svg">


Insert SVGs into matplotlib

```sh
pip install skunk
```


## Overwrite Subplot

```py
import skunk
import numpy as np
import os
import matplotlib.pyplot as plt

fig, axs = plt.subplots(ncols=2, squeeze=True)

x = np.linspace(0, 2 * np.pi)
axs[0].plot(x, np.sin(x))

# important line where we set ID
skunk.connect(axs[1], 'sk')

plt.tight_layout()

# Overwrite using file path to my svg
# Can also use string
svg = skunk.insert(
    {
        'sk': 'skunk.svg'
    })

with open('replaced.svg', 'w') as f:
    f.write(svg)
```

### Output

![image](https://user-images.githubusercontent.com/908389/132105794-f178b4c1-3378-46b9-81d8-18f8e2435a83.png)


## SVG in Annotation

Read about [annotation boxes first](https://matplotlib.org/stable/gallery/text_labels_and_annotations/demo_annotation_box.html)

```py
import numpy as np

fig, ax = plt.subplots(figsize=(300/72, 300/72))

x = np.linspace(0, 2 * np.pi)
ax.plot(x, np.sin(x))

# new code: using skunk box with id sk1
box = skunk.Box(50, 50, 'sk1')
ab = AnnotationBbox(box, (np.pi / 2, 1),
                    xybox=(-5, -100),
                    xycoords='data',
                    boxcoords="offset points",
                    arrowprops=dict(arrowstyle="->"))
ax.add_artist(ab)

# sknunk box with id sk2
box = skunk.Box(50, 50, 'sk2')
ab = AnnotationBbox(box, (3 * np.pi / 2, -1),
                    xybox=(-5, 100),
                    xycoords='data',
                    boxcoords="offset points",
                    arrowprops=dict(arrowstyle="->"))

ax.add_artist(ab)

# insert current figure into itself at sk1
# insert svg file in sk2
svg = skunk.insert(
    {
        'sk1': skunk.pltsvg(),
        'sk2': 'skunk.svg'
    })

with open('replaced2.svg', 'w') as f:
    f.write(svg)
```

### Output

![image](https://user-images.githubusercontent.com/908389/132105868-f0e4ae23-3ebf-4630-b230-8279d5791169.png)
