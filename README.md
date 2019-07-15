# kinoko

[![Build Status](https://travis-ci.org/koyo922/kinoko.svg?branch=master)](https://travis-ci.org/koyo922/kinoko)
[![codecov](https://codecov.io/gh/koyo922/kinoko/branch/master/graph/badge.svg)](https://codecov.io/gh/koyo922/kinoko)
[![PyPI version](https://badge.fury.io/py/kinoko.svg)](https://badge.fury.io/py/kinoko)
[![Python versions](https://img.shields.io/badge/python-2.7%20|%203.6-blue.svg)](https://www.python.org/downloads/release)
![platform](https://img.shields.io/badge/platform-mac%20os%20|%20linux-lightgrey.svg)

python/bash package for Japanese NLP and many other utils

Quick Start
---

```bash
# Official Site
pip install -U -i https://pypi.python.org/simple --trusted-host pypi.python.org kinoko

# Speedup in China using Alibaba Cloud
pip install -U -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com kinoko
```

Example
---

### one-line web server

Server side:

```python
from __future__ import unicode_literals
from typing import Text
from kinoko.misc.web import RESTful # 1. import the decorator

@RESTful(port=8004, route='/') # 2. using the decorator to turns ordinary function
def introduce(name, friends):
    friends = friends if isinstance(friends, Text) else ', '.join(friends)  # maybe Tuple[Text, ...]
    return '{} has friends: {}'.format(name.upper(), friends)

introduce.serve() # 3. start listening
```

Client side:

```bash
$ curl 'http://localhost:8004?name=yongqiang' -d 'friends=赵四'
YONGQIANG has friends: 赵四%
$ curl 'http://localhost:8004?name=yongqiang' -d 'friends=yutian' -d 'friends=赵四'
YONGQIANG has friends: yutian, 赵四% 
```

### chasing URL redirection

```bash
# 1. install the latest version of pip and kinoko
# 2. usage as below
$ chaseurl -h
Usage:
    chase_url [options]

Options:
    -i INPUT --input=INPUT               input file [default: /dev/stdin]
                                         BETTER TO USE FILE THAN PIPE, for a meaningful progressbar
    -o OUTPUT --output=OUTPUT            output file [default: /dev/stdout]
    -m MAX_DEPTH --max_depth=MAX_DEPTH   max depth of redirection [default: 5]
    -t TEMPLATE --template=TEMPLATE      output template [default: $'{n_jumps}\t{url}\t{tgt_url}']
                                         supported elements: (n_jumps, url, tgt_url, all_jumps, exception)
                                         NOTE: curly braces are needed, <tab> need to be bash-escaped via $'\t'

# 3. demo
$ echo 'http://www.jingdong.com' | chaseurl -t $'{n_jumps}\t{url}\t{tgt_url}' 2>/dev/null | cat -T
2^Ihttp://www.jingdong.com^Ihttps://www.jd.com/ # using `cat -T` maps `\t` into `^I` which is clearer
# echo pipe here for simplicity; please use real file in production(which shows proper progress bar)
```

Maintainer
---
### owners
* qianweishuo(qzy922@gmail.com)

### committers
* qianweishuo(qzy922@gmail.com)
