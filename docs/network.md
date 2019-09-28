# Network

## Usage

### chasing HTTP-redirection(3xx)

```python
from kinoko.misc.network.chase_redirection import chase_redirection, ChaseError

try:
    all_jumps = chase_redirection('http://www.cyberciti.biz/tips/', max_depth=3)
    # http redirected to https
    assert ['http://www.cyberciti.biz/tips/', 'https://www.cyberciti.biz/tips/'] == all_jumps
except ChaseError:
    ...
```

### `proxying()` in context manager style

```python
from kinoko.misc.network.proxy import proxing

# `url` default to 'http://172.17.0.1:1082' , the IP for docker host
with proxing(url='http://ip:port'):
    ...  # downloading something beyond GFW
# outside the `with` statement, proxy settings are restored to its old value
```
