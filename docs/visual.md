# Visual

## restrict showing how many detail of `DataFrame`

```python
from kinoko.visual import pd_showing_detail
from IPython.display import display

with pd_showing_detail(max_cols=10, max_colwidth=800):
    df = ...
    display(df)  # or print(df)
```

