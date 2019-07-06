# Getting started

## Installation

### Installing Python and pip

Before installing Kinoko, you need to make sure you have Python and `pip`
– the Python package manager – up and running. You can verify if you're already
good to go with the following commands:

``` sh
python --version
# Python 2.7.13 or above
pip --version
# pip 9.0.1 or above
```

Or else, you can install them by either of following

- [pyenv](https://github.com/pyenv/pyenv#homebrew-on-macos)
    ```bash
    curl https://pyenv.run | bash
    ```
- [Anaconda](https://www.anaconda.com/distribution/)
    ```bash
    curl https://repo.anaconda.com/archive/Anaconda3-2019.03-MacOSX-x86_64.sh | bash
    ```

### Installing Kinoko

using either the PyPI repo or directly from GitHub

- official PyPI repo
    ```bash
    pip install kinoko
    ```
- directly from GitHub code
    ```bash
    pip install git+https://github.com/koyo922/kinoko@master # or other branch
    ```

??? tip "Speedup in mainland China"
    consider using Aliyun mirror of PyPI for speed up
    ```bash
    pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com kinoko
    ```

## Usage

A few demos below:

### chasing HTTP-redirection(3xx)

```bash
$ chaseurl --help
Usage:
    chase_url [options]

Options:
    -i INPUT --input=INPUT               input file [default: /dev/stdin]
                                         BETTER TO USE FILE THAN PIPE, for a meaningful progressbar
    -o OUTPUT --output=OUTPUT            output file [default: /dev/stdout]
    -m MAX_DEPTH --max_depth=MAX_DEPTH   max depth of redirection [default: 5]
    -t TEMPLATE --template=TEMPLATE      output template [default: {n_jumps}    {url}   {tgt_url}]
                                         supported elements: (n_jumps, url, tgt_url, all_jumps, exception)
                                         NOTE: curly braces are needed, <tab> need to be bash-escaped via $'\t'

$ echo 'http://www.jingdong.com' | chaseurl 2>/dev/null
2       http://www.jingdong.com https://www.jd.com/
```

```bash
$ echo -e 'http://www.jingdong.com\nhttp://www.baidu.com' > url.txt
$ chaseurl -i url.txt -o 'redir.txt' --template '{tgt_url}'
$ cat redir.txt
https://www.jd.com/
http://www.baidu.com
```

!!! note

    - `#!bash 2>/dev/null` suppress the progress bar output
    - default output template is `'{n_jumps}\t{url}\t{tgt_url}'`

### get `logger` object

```python tab='script.py'
from kinoko.misc.log_writer import init_log
logger = init_log(__name__)
...
logger.info('msg: %s', msg)
```

```bash tab='call from console'
LEVEL=DEBUG python script.py
# default LEVEL=INFO
```

!!! caution
    The default logger in python `logging` module is not multiprocess-rotation-safe;
    we are planing to fix it in version 1.1.0

### bash utils

```bash
$ colormsg "some message" WARNING # default LEVEL=INFO
==> some message # in yellow color
```

!!! warning
    `colormsg` does not work on Mac Bash

```bash
# turn on 64GB of virtual memory at /home/work/swap
vmem.sh -a on -s 64 -f /home/work/swap
```

### csv utils

aggregate a tsv/csv file

```bash
cat <<'EOF' > infile.tsv
21      male      永强      1
22      male      永强      2
20      female      刘英      3
20      female      刘英      4
EOF

# aggregation by first 3 columns, summing the last column
aggtsv --infile infile.tsv --sep $'\t' \
    -k 0 1 2 -r 3 -a sum
21      male      永强      1
22      male      永强      2
20      female      刘英      7
```

patch a tsv file via one or more reference files

```bash
$ cat <<'EOF' > ref.tsv
jiaose  角色  juese
xxx 色情词 <DEL>
EOF

$ cat <<'EOF' > in.tsv
field1  field2  角色  jiaose  field4
field1  field2  角色  jiaose  field4
field1  field2  色情词 xxx field4
EOF

$ patchtsv -r ref.tsv -d $'\t' \
    -i in.tsv -o out.tsv \
    -k 3 2 -v 3
$ cat out.tsv
field1  field2  角色  juese   field4
field1  field2  角色  juese   field4
```

### functional utils

sliding window of any sequence

```python
>>> from kinoko.func import sliding
>>> for grp in sliding(range(10), size=5 , step=3):
...     print(grp)
...
[0, 1, 2, 3, 4]
[3, 4, 5, 6, 7]

>>> for grp in sliding(range(10), size=5 , step=3, skip_non_full=False):
...     print(grp)
...
[0, 1, 2, 3, 4]
[3, 4, 5, 6, 7]
[6, 7, 8, 9]
[9]
```

C-equivalent static vars of function

```python
>>> from kinoko.func import static_vars
>>> @static_vars(counter=0)
... def foo():
...     foo.counter += 1
...     print(foo.counter * 10)
...
... foo()
10
... foo()
20
... foo()
30
```
