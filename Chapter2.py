# -*- coding: UTF-8 -*-
# 檔案以UTF-8運行

# 資料結構
# List 的操作方法使得它非常簡單可以用來實作 stack（堆疊）。Stack 為一個遵守最後加入元素最先被取回（後進先出，"last-in, first-out"）規則的資料結構。你可以使用方法 append() 將一個項目放到堆疊的頂層。而使用方法 pop() 且不給定索引值去取得堆疊最上面的項目。
# 我們也可以將 list 當作 queue（佇列）使用，即最先加入元素最先被取回（先進先出，"first-in, first-out"）的資料結構。然而，list 在這種使用方式下效率較差。使用 append 和 pop 來加入和取出尾端的元素較快，而使用 insert 和 pop 來插入和取出頭端的元素較慢（因為其他元素都需要挪動一格）。
from collections import deque
queue = deque(["Eric", "John", "Michael"])
queue.append("Terry")           # Terry 加進來
queue.append("Graham")          # Graham 加進來
queue.popleft()                 # 第一個加進來的現在離開

queue.popleft()                 # 第二個加進來的現在離開

queue                           # queue 裡剩下的會按照加進來的順序排列

# 快速建立串列的方法
#1.
squares = []
for x in range(10):
    squares.append(x**2)
#2.
squares = list(map(lambda x: x**2, range(10)))
#3.
squares = [x**2 for x in range(10)]
# 找出兩個陣列中相異的元素
print([(x, y) for x in [1,2,3] for y in [3,1,4] if x != y])

# 巢狀的 List Comprehensions
matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]
print([[row[i] for row in matrix] for i in range(4)])
print(list(zip(*matrix)))
# [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]

# 串列的移除
a = [-1, 1, 66.25, 333, 333, 1234.5]
del a[0]
del a

# Set
basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
print(type(basket))
print(basket)
a = set('abracadabra')
print(type(a))

#Map
tel = {'jack': 4098, 'sape': 4139}
print(tel)
print(list(tel))
print('jack' in tel)
print(dict([('sape', 4139), ('guido', 4127), ('jack', 4098)]))
print({x: x**2 for x in (2, 4, 6)})
print(dict(sape=4139, guido=4127, jack=4098))

# 迴圈技巧
knights = {'gallahad': 'the pure', 'robin': 'the brave'}
for k, v in knights.items():
    print(k, v)

for i, v in enumerate(['tic', 'tac', 'toe']):
    print(i, v)

questions = ['name', 'quest', 'favorite color']
answers = ['lancelot', 'the holy grail', 'blue']
for q, a in zip(questions, answers):
    print('What is your {0}?  It is {1}.'.format(q, a))

print((1, 2, 3, 4) < (1, 2, 4)) # True
print((1, 2) < (1, 2, -1)) # True

# 6 Module
def fib(n):    # 寫出費波那契數列至第 n 位
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()

f = fib # 將函式做為變數傳遞
print(f(10)) 
print(f(5))

# import Chapter1
# 這並不會將 Chapter1 中定義的函式名稱直接加入當前的 namespace 中（詳情請見 Python 作用域 (Scope) 及命名空間 (Namespace)）；它只會加入 fibo 的模組名稱。
# from Chapter1 import foo as f
# Import 一個名為 spam 的模組時，直譯器首先會搜尋具有該名稱的內建模組。模組名稱列在 sys.builtin_module_names 當中。如果找不到，接下來會在變數 sys.path 所給定的資料夾清單之中，搜尋一個名為 spam.py 的檔案。sys.path 從這些位置開始進行初始化：
# 為了加快載入模組的速度，Python 將每個模組的編譯版本暫存在 __pycache__ 資料夾下，並命名為 module.version.pyc， 這裡的 version 是編譯後的檔案的格式名稱，且名稱通常會包含 Python 的版本編號。
# Import 套件時，Python 會搜尋 sys.path 裡的目錄，尋找套件的子目錄。
# 目錄中必須含有 __init__.py 檔案，才會被 Pyhon 當成套件

# import 為了避免不必要的副作用，在import時定義.* 要import的項目
# __all__ = ["echo", "surround", "reverse"]

# 7 I/O
yes_votes = 42_572_654 # 比較可讀的整數
total_votes = 85_705_149
percentage = yes_votes / total_votes
'{:-9} YES votes  {:2.2%}'.format(yes_votes, percentage)
# - 靠左對齊、9 至少9個字元寬
# 如果 yes_votes 的長度小於 9，則右側會填充空格。
# 2.2 → 總共 2 位整數部分和 2 位小數部分。
# % → 轉換為百分比（自動乘以 100，並加上 % 符號）。
# str() 函式的用意是回傳一個人類易讀的表示法，
# repr() 的用意是產生直譯器可讀取的表示法（如果沒有等效的語法，則造成 SyntaxError）。
print('We are the {} who say "{}!"'.format('knights', 'Ni'))
print('This {food} is {adjective}.'.format(food='spam', adjective='absolutely horrible'))

for x in range(1, 11):
    print(repr(x).rjust(2), repr(x*x).rjust(3), end=' ')
    # 注意前一列使用的 'end'
    print(repr(x*x*x).rjust(4))

import math
print('The value of pi is approximately %5.3f.' % math.pi)

#檔案讀寫
with open('workfile', 'w', encoding="utf-8") as f:
    f.write("testing...clark")
# wb 可以用 byte寫入，使用Byte有以下好處
# ✅ 適用於 非文字文件
# ✅ 避免編碼問題
# ✅ 記憶體效率更高
# ✅ 可進行 位元運算

# 要讀取檔案的內容，可呼叫 f.read(size)，它可讀取一部份的資料，並以字串（文字模式）或位元組串物件（二進制模式）形式回傳。
# size 是個選擇性的數字引數。當 size 被省略或為負數時，檔案的全部內容會被讀取並回傳；如果檔案是機器記憶體容量的兩倍大時，這會是你的問題。
# 否則，最多只有等同於 size 數量的字元（文字模式）或 size 數量的位元組串（二進制模式）會被讀取及回傳。如果之前已經到達檔案的末端，f.read() 會回傳空字串（''）。
with open('workfile', 'rb') as f:
    print(f.read())
    print(f.read())

避免一次讀取造成OOM
f.readline() #'This is the first line of the file.\n'
f.readline() #'Second line of the file\n'
f.readline()
for line in f:
    print(line, end='')
# Python 支援一個普及的資料交換格式，稱為 JSON (JavaScript Object Notation)。標準模組 json 可接收 Python 資料階層，並將它們轉換為字串表示法；這個過程稱為 serializing（序列化）。從字串表示法中重建資料則稱為 deserializing（反序列化）。在序列化和反序列化之間，表示物件的字串可以被儲存在檔案或資料中，或通過網路連接發送到遠端的機器
import json
x = [1, 'simple', 'list']
json.dumps(x) # '[1, "simple", "list"]' #將物件序列化成text file

# 若 f 是一個已開啟、可讀取的 binary file 或 text file 物件，要再次解碼物件的話
x = json.load(f)

# 8.
# 常見的（至少）兩種不同的錯誤類別為：語法錯誤 (syntax error) 和例外 (exception)
class B(Exception):
    pass
class C(B):
    pass
class D(C):
    pass
for cls in [B, C, D]:
    try:
        raise cls() # 拋出例外
    except D:
        print("D")
    except C:
        print("C")
    except B:
        print("B")

# Exception 可以在例外名稱後面指定一個變數，這個變數被綁訂到一個例外實例上，參數通常儲存在args屬性中
try:
    raise Exception('spam', 'eggs')
except Exception as inst:
    print(type(inst))    # the exception type
    print(inst.args)     # arguments stored in .args
    print(inst)          # __str__ allows args to be printed directly,
                         # but may be overridden in exception subclasses
    x, y = inst.args     # unpack args
    print('x =', x)
    print('y =', y)
# <class 'Exception'>
# ('spam', 'eggs')
# ('spam', 'eggs')
# x = spam
# y = eggs

# BaseException 是由全部的例外所共用的 base class。它的 subclass（子類別）之一，Exception，則是所有非嚴重例外 (non-fatal exception) 的 base class。有些例外不是 Exception 的 subclass，而它們通常不會被處理，因為它們是用來指示程式應該終止。這些例外包括了由 sys.exit() 所引發的 SystemExit，以及當使用者想要中斷程式時所引發的 KeyboardInterrupt。

# 陳述式有一個選擇性的 else 子句，使用時，該子句必須放在所有 except 子句之後。如果一段程式碼必須被執行，但 try 子句又沒有引發例外時，這個子句很有用。例如：
for arg in sys.argv[1:]:
    try:
        f = open(arg, 'r')
    except OSError:
        print('cannot open', arg)
    else:
        print(arg, 'has', len(f.readlines()), 'lines')
        f.close()

# raise 唯一的引數就是要引發的例外。該引數必須是一個例外實例或例外 class（衍生自 BaseException 的 class，例如 Exception 與它的 subclass）。如果一個例外 class 被傳遞，它會不含引數地呼叫它的建構函式 (constructor) ，使它被自動建立實例 (implicitly instantiated)：

def divide(x, y):
    try:
        result = x / y
    except ZeroDivisionError:
        print("division by zero!")
    else:
        print("result is", result)
    finally:
        print("executing finally clause")

# 在某些情況下，必須回報已經發生的多個例外。在並行框架 (concurrency framework) 中經常會出現這種情況，當平行的 (parallel) 某些任務可能已經失效，但還有其他用例 (use case) 希望能繼續執行並收集多個例外，而不是只有引發第一個例外時。
# 內建的 ExceptionGroup 會包裝一個例外實例 (exception instance) 的 list（串列），使得它們可以一起被引發。由於它本身就是一個例外，因此它也可以像任何其他例外一樣被捕獲。
def f():
    excs = [OSError('error 1'), SystemError('error 2')]
    raise ExceptionGroup('there were problems', excs)
try:
    f()
except Exception as e:
    print(f'caught {type(e)}: e')

# 請注意，被巢套在例外群組中的例外必須是實例，而不是類型。這是因為在實務上，這些例外通常是已經被程式引發並捕獲的例外，類似以下的模式：
excs = []
for test in tests:
    try:
        test.run()
    except Exception as e:
        excs.append(e)

if excs:
   raise ExceptionGroup("Test Failures", excs)

# 當一個例外是為了被引發而建立時，它通常會伴隨著一些資訊被初始化，這些資訊描述了當下發生的錯誤。在某些情況，在例外被捕獲之後添加資訊會很有用。為此，例外具有一個 add_note(note) method（方法），它可以接受一個字串並將其添加到例外的註解清單中。標準的回溯呈現會在例外之後列出所有的註解，並按照其被添加的順序來排列。
try:
    raise TypeError('bad type')
except Exception as e:
    e.add_note('Add some information')
    e.add_note('Add some more information')
    raise