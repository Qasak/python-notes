## Scheme程序的语法和语义

一种语言的语法是将字符排列成正确的语句或表达式；语义是这些语句或表达式的含义。

例如，在数学表达式语言（以及许多编程语言）中，一加二的语法是“1+2”，语义是对两个数字进行加法运算，得到值3。

当我们确定一个表达式的值时，我们假设它是求值的；我们会说“1+2”的计算结果为3，并将其写为“1+2”⇒3。

Scheme语法与大多数其他编程语言不同。

| Java                                                         |      | Scheme                                                       |
| ------------------------------------------------------------ | ---- | ------------------------------------------------------------ |
|                                                              |      |                                                              |
| **if** (x.val() > 0) { **return** fn(A[i] + 3 * i,      **new** String[] {"one", "two"});} |      | (**if** (> (val x) 0)  (fn (+ (aref A i) (* 3 i))    (**quote** (one two))) |

Java有各种各样的语法约定（关键字、中缀运算符(infix operators)、三种括号、运算符优先级、点表示法、引号、逗号、分号），但是Scheme语法要简单得多：

- Scheme程序仅由*表达式*组成. 没有语句/表达式的区别.

- 数字 (e.g. `1`) ， 符号 (e.g. `A`) 都被成为*原子表达式* (*atomic expressions*); 他们不能被拆分. 它们与Java的对应部分相似，只是在Scheme中，+和>等运算符也是符号，它们的处理方式与 `A` 和 `fn`相同.

- 其他所有内容都是一个列表表达式

  一个 "(", 后跟零个或多个表达式，后跟一个 ")". 列表的第一个元素决定了它的含义:

  - 以关键字开头的列表, e.g. `(if ...)`,是一个*特殊形式* (*special form*); 其含义取决于关键字.
  - 以非关键字开头的列表, e.g. `(fn ...)`,是一个函数调用.

  

Scheme的优点是整个语言只需要5个关键字和8个句法形式(syntactic forms)。. 相比之下Python有33个关键字和 [110](https://docs.python.org/3/reference/grammar.html) 句法形式, Java 有50个关键字和[133](https://docs.oracle.com/javase/specs/jls/se7/html/jls-18.html) 个句法形式. 所有这些括号看起来都很吓人，但是Scheme语法具有简单和一致的优点。 (Some have joked that "Lisp" stands for "[***L**ots of **I**rritating **S**illy **P**arentheses*](http://www.google.com/search?q=Lots+of+Irritating+Silly+Parentheses)"; I think it stand for "[***L**isp **I**s **S**yntactically **P**ure*](http://www.google.com/search?hl=en&as_q=&as_epq=Lisp+Is+Syntactically+Pure)".)

在本页中，我们将讨论Scheme语言及其解释的所有要点（省略一些小细节），但我们将采取两个步骤来达到这一点，在定义近乎完整的Scheme语言之前，首先定义一个简化的语言。

## 语言1:*Lispy*计算器

Lispy计算器是Scheme的一个子集，只使用五种语法形式（两种原子形式、两种特殊形式和过程调用）。Lispy Calculator允许你在典型的计算器上进行任何计算，只要你熟悉前缀标记( prefix notation)。你可以做两件在典型计算器语言中没有的事情：“if”表达式和新变量的定义。下面是一个示例程序，它使用公式πr2计算半径为10的圆的面积：

```scheme
(define r 10)
(* pi (* r r))
```

以下是所有允许表达式的表格：

| 表达式                                                       | 语法                        | 语义和例子                                                   |
| ------------------------------------------------------------ | --------------------------- | ------------------------------------------------------------ |
| [变量引用](http://www.schemers.org/Documents/Standards/R5RS/HTML/r5rs-Z-H-7.html#%_sec_4.1.1) | *symbol*                    | 符号被解释为变量名；它的值就是变量的值<br /> Example: `r` ⇒ `10` (假设 `r` 之前被定义成10) |
| [常量字面(constant literal)](http://www.schemers.org/Documents/Standards/R5RS/HTML/r5rs-Z-H-7.html#%_sec_4.1.2) | *number*                    | 一个数的计算结果是它自己.<br /> Examples: `12 ⇒ 12` *or* `-3.45e+6 ⇒ -3.45e+6` |
| [条件](http://www.schemers.org/Documents/Standards/R5RS/HTML/r5rs-Z-H-7.html#%_sec_4.1.5) | `(if` *test conseq alt*`)`  | 计算 *test*；如果为true，则求值并返回*conseq*；否则为*alt*.<br />Example: `(if (> 10 20) (+ 1 1) (+ 3 3)) ⇒ 6` |
| [定义](http://www.schemers.org/Documents/Standards/R5RS/HTML/r5rs-Z-H-8.html#%_sec_5.2) | `(define` *symbol* *exp*`)` | 定义一个新变量，并给它赋值表达式*exp*.<br /> Examples: `(define r 10)` |
| [过程调用](http://www.schemers.org/Documents/Standards/R5RS/HTML/r5rs-Z-H-7.html#%_sec_4.1.3) | `(`*proc arg...*`)`         | 如果 *proc* 不是`if, define, `或 `quote` 之一，将其视为一个过程. 计算 *proc* 及其所有 *args*, 然后将该过程应用到*arg* 值列表. <br />Example: `(sqrt (* 2 8)) ⇒ 4.0` |

在该表的*语法*列中, *symbol* 必须是一个符号, *number* 必须是整数或浮点数, 其他斜体字可以是任何表达式.  *arg...* 标记是零个或多个 *arg*.

## 语言解释器做了什么？

语言解释器由两个部分构成:

1. **解析(Parsing)**:

    

   解析组件以字符序列的形式接收输入程序，根据语言的语法规则对其进行验证，并将程序转换为内部表示。在简单的解释器中，内部表示是一种树结构（通常称为抽象语法树）(abstract syntax tree) 它反映程序中语句或表达式的嵌套结构。

   

   在一个称为*编译器*的语言解释器程序中通常有一系列内部表示法，从抽象语法树开始，逐步发展到可由计算机直接执行的一系列指令. 

   

   Lispy解析器是用parse函数实现的.

   

2. **执行(Execution):** 然后根据语言的语义规则对内部表示进行处理，从而进行计算。Lispy的执行函数称为eval（请注意，它隐藏了Python同名的内置函数）.

>  program ➡ `parse` ➡ abstract-syntax-tree ➡ `eval` ➡ result

下面是一个简短的示例，说明我们希望parse和eval能够做什么（begin按顺序计算每个表达式并返回最后一个表达式）：

```bash
>> program = "(begin (define r 10) (* pi (* r r)))"

>>> parse(program)
['begin', ['define', 'r', 10], ['*', 'pi', ['*', 'r', 'r']]]

>>> eval(parse(program))
314.1592653589793
```

## 类型定义

让我们明确Scheme对象的表示：

```Python
Symbol = str              # A Scheme Symbol is implemented as a Python str
Number = (int, float)     # A Scheme Number is implemented as a Python int or float
Atom   = (Symbol, Number) # A Scheme Atom is a Symbol or Number
List   = list             # A Scheme List is implemented as a Python list
Exp    = (Atom, List)     # A Scheme expression is an Atom or List
Env    = dict             # A Scheme environment (defined below) 
                          # is a mapping of {variable: value}
```

## Parsing: `parse`, `tokenize` and `read_from_tokens`

传统上，语法分析分为两个部分: 词法分析(*lexical analysis*), 将输入的字符串分解成一系列 *tokens*, 句法分析(*syntactic analysis*), 将token组合成一个抽象的语法树. 

Lispy的token是括号、符号和数字. 词法分析有很多工具(比如 Mike Lesk and Eric Schmidt's [lex](http://dinosaur.compilertools.net/#lex)), 但是现在我们将使用一个非常简单的工具: Python的 `str.split`. 

函数 `tokenize`接受一个字符串作为输入；它在每个括号周围添加空格，然后调用 `str.split` 来得到token列表:

```python
def tokenize(chars: str) -> list:
    "Convert a string of characters into a list of tokens."
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()
```

```python
>>> program = "(begin (define r 10) (* pi (* r r)))"
>>> tokenize(program)
['(', 'begin', '(', 'define', 'r', '10', ')', '(', '*', 'pi', '(', '*', 'r', 'r', ')', ')', ')']
```

我们的函数 `parse` 将以一个程序的字符串作为输入, 调用 `tokenize` 来得到token列表, 然后调用 `read_from_tokens` 组合成一颗抽象语法树. 

`read_from_tokens` 查看第一个标记; 如果是一个 `')'` 说明语法错误. 如果是一个`'('`, 那么我们开始构建一个子表达式列表，直到找到匹配的 `')'`. 任何非圆括号token都必须是symbol或number.

 我们让Python来区分它们：对于每个非括号标记，首先尝试将其解释为int，然后解释为float，如果两者都不是，那么它一定是一个symbol. 

```python
def parse(program: str) -> Exp:
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))

def read_from_tokens(tokens: list) -> Exp:
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        L=[]
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)
    
def atom(token: str) -> Atom:
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)
```

## Evaluation: `eval`

We are now ready for the implementation of `eval`. As a refresher, we repeat the table of Lispy Calculator forms:



| Expression                                                   | Syntax                      | Semantics and Example                                        |
| ------------------------------------------------------------ | --------------------------- | ------------------------------------------------------------ |
| [variable reference](http://www.schemers.org/Documents/Standards/R5RS/HTML/r5rs-Z-H-7.html#%_sec_4.1.1) | *symbol*                    | A symbol is interpreted as a variable name; its value is the variable's value. Example: `r` ⇒ `10` (assuming `r` was previously defined to be 10) |
| [constant literal](http://www.schemers.org/Documents/Standards/R5RS/HTML/r5rs-Z-H-7.html#%_sec_4.1.2) | *number*                    | A number evaluates to itself. Examples: `12 ⇒ 12` *or* `-3.45e+6 ⇒ -3.45e+6` |
| [conditional](http://www.schemers.org/Documents/Standards/R5RS/HTML/r5rs-Z-H-7.html#%_sec_4.1.5) | `(if` *test conseq alt*`)`  | Evaluate *test*; if true, evaluate and return *conseq*; otherwise *alt*. Example: `(if (> 10 20) (+ 1 1) (+ 3 3)) ⇒ 6` |
| [definition](http://www.schemers.org/Documents/Standards/R5RS/HTML/r5rs-Z-H-8.html#%_sec_5.2) | `(define` *symbol* *exp*`)` | Define a new variable and give it the value of evaluating the expression *exp*. Examples: `(define r 10)` |
| [procedure call](http://www.schemers.org/Documents/Standards/R5RS/HTML/r5rs-Z-H-7.html#%_sec_4.1.3) | `(`*proc arg...*`)`         | If *proc* is anything other than one of the symbols `if, define, `or `quote` then it is treated as a procedure. Evaluate *proc* and all the *args*, and then the procedure is applied to the list of *arg* values. Example: `(sqrt (* 2 8)) ⇒ 4.0` |



Here is the code for `eval`, which closely follows the table: