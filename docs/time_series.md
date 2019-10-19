# Time Series Analysis Tool

## Python implementation of the famous UCR DTW algorithm

For theoretical details,
please read the [paper](https://www.cs.ucr.edu/~eamonn/SIGKDD_trillion.pdf) or this [article]()
 
Usage below:

```python
from kinoko.time_series.dtw import UCR_DTW
import numpy as np
import pytest

# `dist_cb` means "callback function for distance", you can try `abs(x-y)` etc.
# `window_frac` is the fraction of query length used as window during various LB calculation
# for "Euclidean Distance" instead of DTW, just set window_frac to zero
ucr_dtw = UCR_DTW(dist_cb=lambda x,y: (x-y)**2, window_frac=0.05)

x1 = np.linspace(0, 50, 100, endpoint=False)
y1 = 3.1 * np.sin(x1 / 1.5) + 3.5

x2 = np.linspace(0, 25, 50, endpoint=False)  # half slice of x1
y2 = 3.1 * np.sin((x2 + 4) / 1.5) + 3.5  # same function but slided 4-units toward west

# `content` can be a `Iterable`(stream) of float/int, of any length
# `query` is supposed to be a sequence of fixed length, which would be loaded into RAM
loc, dist, _stat = ucr_dtw.search(content=y1, query=y2)
assert 8 == loc  # 4 unit / 0.5 gap = 8
assert pytest.approx(0) == dist  # almost zero
```

!!!caution "Known Issues"

   - Currently, it only supports ==float/int== sequence
    - vectors or even `object`s can not be uniformly `norm`ed
    - hook mechanism seems like a "Premature Optimization"
      
   - Speed is approximately same as [another Python implementation](https://github.com/JozeeLin/ucr-suite-python/blob/master/DTW.ipynb)
     Completed time/memory efficiency comparison with the [original C implementation](https://github.com/klon/ucrdtw/blob/master/src/ucrdtw.c)
     was not conducted.
     
   - It is ==NOT production-ready==, use it with caution.
