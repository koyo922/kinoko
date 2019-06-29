# Specimen for some useful formats

## Admonition

```markdown
!!! example "A Example"
    This is an admonition box of type 'example' and title 'A Example' .
```
    
!!! example "A Example"
    This is an admonition box of type 'example' and title 'A Example' .
    
??? note "Available Admonition Types"
     
    !!!note
    
    !!!example
    
    !!!hint "hint/tip/important"

    !!!caution "attention/caution/warning"
    
    !!!danger "danger/error"
    
## Task List

```markdown
- [X] item 1
    * [X] item A
    * [ ] item B
        more text
        + [x] item a
        + [ ] item b
- [ ] item 2
```

- [X] item 1
    * [X] item A
    * [ ] item B
        more text
        + [x] item a
        + [ ] item b
- [ ] item 2

## Keys

```markdown
++cmd+alt+"&Uuml;"++
```

++cmd+alt+"&Uuml;"++

## Mark

```markdown
==mark me==

==smart==mark==
```
==mark me==

==smart==mark==

## Smart Symbols

```markdown
(c) +/- --> =/= 1st 2nd etc.
```

(c) +/- --> =/= 1st 2nd etc.


## Tilde for ~~Deletion~~ and ~Subscript~

```markdown
~~Delete me~~

CH~3~CH~2~OH

text~a\ subscript~
```

~~Delete me~~

CH~3~CH~2~OH

text~a\ subscript~

## Inline Code

```markdown
this is some inline code `#!python sqr = lambda n: n^2` .
```

this is some inline code `#!python sqr = lambda n: n^2` .

## Magic Link / Email

```markdown
- Just paste links directly in the document like this: https://google.com.
- Or even an email address: fake.email@email.com.
```

- Just paste links directly in the document like this: https://google.com.
- Or even an email address: fake.email@email.com.

## Foot Note
 
```markdown
identifiers [^1] or names [^Granovetter et al. 1998]

[^1]: foot note for identifier1 .
[^Granovetter et al. 1998]:
    foot note for name 'Granovetter et al. 1998'. 
```

identifiers [^1] or names [^Granovetter et al. 1998]

[^1]: foot note for identifier1 .
[^Granovetter et al. 1998]:
    foot note for name 'Granovetter et al. 1998'. 

## [Critic](https://facelessuser.github.io/pymdown-extensions/extensions/critic)

!!! note
    The demo code below also gets rendered, please check 
    the [official manual](https://facelessuser.github.io/pymdown-extensions/extensions/critic) for refenrence.

```critic-markup
Here ==is some== {--incorrect--} Markdown.  I am adding this{++ here++}.

And here is a comment on {==some
 text==}{>>This works quite well. I just wanted to comment on it.<<}. Substitutions {~~is~>are~~} great!

General block handling.

{--

* test remove
* test remove
    * test remove

--}

{++

* test add
* test add
    * test add

++}
```

Here ==is some== {--incorrect--} Markdown.  I am adding this{++ here++}.

And here is a comment on {==some
 text==}{>>This works quite well. I just wanted to comment on it.<<}. Substitutions {~~is~>are~~} great!

General block handling.

{--

* test remove
* test remove
    * test remove

--}

{++

* test add
* test add
    * test add

++}

## SuperFences(for Tabed Blocks)

~~~markdown
```python hl_lines="1 3" linenums="2" tab="Python3"
"""Some file."""
import foo.bar
import foo.bar.baz
```

```C tab=
#include 

int main(void) {
  printf("hello, world\n");
}
```
~~~

```python hl_lines="1 3" linenums="2" tab="Python3"
"""Some file."""
import foo.bar
import foo.bar.baz
```

```C tab=
#include 

int main(void) {
  printf("hello, world\n");
}
```

## Math

```markdown
$$
\frac{n!}{k!(n-k)!} = \binom{n}{k}
$$

\begin{align}
    p(v_i=1|\mathbf{h}) & = \sigma\left(\sum_j w_{ij}h_j + b_i\right) \\
    \label{eq:relative-theory} E &= mc^2
\end{align}

$\eqref{eq:relative-theory}$ was discovered by Albert Einstein.
```

$$
\frac{n!}{k!(n-k)!} = \binom{n}{k}
$$

\begin{align}
    p(v_i=1|\mathbf{h}) & = \sigma\left(\sum_j w_{ij}h_j + b_i\right) \\
    \label{eq:relative-theory} E &= mc^2
\end{align}

Equation $\eqref{eq:relative-theory}$ was discovered by Albert Einstein.

!!! note "How to numbering and reference the equations"
    `#!latex \label{eq:myeq1}` and `#!latex \eqref{eq:myeq1}` are needed  
    read https://github.com/mkdocs/mkdocs/issues/253#issuecomment-199447897 for reference

## Details

```markdown
???+ note "Open styled details"

    ??? danger "Nested details!"
        And more content again.
        
    ???+ success
        Content.
```

???+ note "Open styled details"

    ??? danger "Nested details!"
        And more content again.
        
    ???+ success
        Content.
