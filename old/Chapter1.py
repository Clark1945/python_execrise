# -*- coding: UTF-8 -*-
# 檔案以UTF-8運行

# 基本 Number 與 String 與 List 的操作
print("Here start the first chapter in Python official Document")
print(9/5) # division always returns a floating-point number
print(10/3) 
print(10//3) # floor division discards the fractional part
print(10**2) # 10 square
print('use \'Python\' to develop app')
print('C:\some\name')  
print(r'C:\some\name')  # aviod \n create a new line
print(3*"A"+"BC") # repeat string with *
print("Python"[0:1] + " " + "Python"[-1])
word="Python"
# word[1] = "G" # String can be index, but it is immutable which mean you can not change a single character in a string.
print(word)
squares = [1,4,9]
print(squares + [16,25])
# print(squares + 16 + 25) only list concatenation is allowed
squares[:] = []
print(squares)

# 流程控制
x=1
if x < 0:
    x = 0
    print('Negative changed to zero')
elif x == 0:
    print('Zero')
else:
    print("bigger than 0")

words = ['cat', 'window', 'defenestrate']
for w in words:
    print(w, len(w))

# Create a sample collection
users = {'Hans': 'active', 'Éléonore': 'inactive', '景太郎': 'active'}

# Strategy:  Iterate over a copy
for user, status in users.copy().items():
    if status == 'inactive':
        del users[user]

print(users)

# Strategy:  Create a new collection
active_users = {}
for user, status in users.items():
    if status == 'active':
        active_users[user] = status

# (range()不是一個list而是一種可迭代物件)
a = ['Mary', 'had', 'a', 'little', 'lamb']
for i in range(len(a)):
    print(i, a[i])

for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '*', n//x)
            break
    else:
        # loop fell through without finding a factor
        print(n, 'is a prime number')
# 當 else 子句用於迴圈時，相較於搭配 if 陳述式使用，它的行為與 try 陳述式中的 else 子句更為相似：try 陳述式的 else 子句在沒有發生例外 (exception) 時執行，而迴圈的 else 子句在沒有任何 break 發生時執行。更多有關 try 陳述式和例外的介紹，見處理例外。

def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
        case 401|403:
            return "Authorization failed"
        case _: # 通用字元，相當於switch case 的 default
            return "Something's wrong with the internet"

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def where_is(point):
    match point:
        case Point(x=0, y=0):
            print("Origin")
        case Point(x=0, y=y):
            print(f"Y={y}")
        case Point(x=x, y=0):
            print(f"X={x}")
        case Point():
            print("Somewhere else")
        case _:
            print("Not a point")
where_is(None)
where_is(Point(0,1))
where_is(Point(3,3))

class Point:
    __match_args__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y
def where_is(points):
    match points:
        case []:
            print("No points")
    # 我們可以在模式中加入一個 if 子句，稱為「防護 (guard)」。如果該防護為假，則 match 會繼續嘗試下一個 case 區塊。請注意，值的擷取會發生在防護的評估之前：
        case Point(x, y) if x == y:
            print(f"Y=X at {x}")
        case [Point(0, 0)]:
            print("The origin")
        case [Point(x, y)]:
            print(f"Single point {x}, {y}")
        case [Point(0, y1), Point(0, y2)]:
            print(f"Two on the Y axis at {y1}, {y2}")
        case _:
            print("Something else")

# 定義列舉
from enum import Enum
class Color(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'

def print_color():
    color = Color(input("Enter your choice of 'red', 'blue' or 'green': "))
    match color:
        case Color.RED:
            print("I see red!")
        case Color.GREEN:
            print("Grass is green")
        case Color.BLUE:
            print("I'm feeling the blues :")


def fib(n):    # write Fibonacci series less than n
    """Print a Fibonacci series less than n.""" # 這是一種方法註解
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()
# 函式執行時會建立一個新的符號表 (symbol table) 來儲存該函式內的區域變數 (local variable)。
# 更精確地說，所有在函式內的變數賦值都會把該值儲存在一個區域符號表。然而，在引用一個變數時，會先從區域符號表開始搜尋，其次為外層函式的區域符號表，其次為全域符號表 (global symbol table)，
# 最後為所有內建的名稱。因此，在函式中，全域變數及外層函式變數雖然可以被引用，但無法被直接賦值（除非全域變數是在 global 陳述式中被定義，或外層函式變數在 nonlocal 陳述式中被定義）。

# 在一個函式被呼叫的時候，實際傳入的參數（引數）會被加入至該函式的區域符號表。因此，引數傳入的方式為傳值呼叫 (call by value)（這裡傳遞的值永遠是一個物件的參照 (reference)，而不是該物件的值）。
#  [1] 當一個函式呼叫別的函式或遞迴呼叫它自己時，在被呼叫的函式中會建立一個新的區域符號表。

f = fib(100)

i = 5
def f(arg=i):
    print(arg)
i = 6
f() # 印出5
# 這裡的 arg 在 f 被定義時就已經設定為 5，不會隨 i 之後的變化而改變。因此，函式 f 其實是「帶有隱藏狀態」的，因為它持有了一個「定義時」的變數值。

def f(lst=[]):  # 預設參數是一個空列表
    lst.append(1)
    print(lst)

f()  # [1]
f()  # [1, 1]
f()  # [1, 1, 1]  (!!!)
# ####################################################################### 這段超重要，超危險

def standard_arg(arg): # (Positional-or-Keyword Arguments
    print(arg)

def pos_only_arg(arg, /): # (Positional-Only Parameters)
    print(arg)

def kwd_only_arg(*, arg): # 僅限關鍵字引數 (Keyword-Only Arguments)
    print(arg)

def combined_example(pos_only, /, standard, *, kwd_only):
    print(pos_only, standard, kwd_only)


def foo(name, **kwds):
    return 'name' in kwds # name 會衝突抱錯
foo(1, **{'names': 2})

def parrot(voltage, state='a stiff', action='voom'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.", end=' ')
    print("E's", state, "!")

# 誰還用Object啊，這根本超方便
d = {"voltage": "four million", "state": "bleedin' demised", "action": "VOOM"}
parrot(**d)

# Lambda 超不可思義
def make_incrementor(n):
    return lambda x: x + n
f = make_incrementor(1)
print(f(1))
print(f(f(1)))
print(f(f(f(f(1)))))

def f(ham: str, eggs: str = 'eggs') -> str:
    print("Annotations:", f.__annotations__) # 印出函式的註釋出來
    return ham + ' and ' + eggs

f('spam')

# 對於 Python，大多數的專案都遵循 PEP 8 的樣式指南；它推行的編碼樣式相當可讀且賞心悅目。每個 Python 開發者都應該花點時間研讀；這裡是該指南的核心重點：
# 用 4 個空格縮排，不要用 tab 鍵。
# 4 個空格是小縮排（容許更大的巢套深度）和大縮排（較易閱讀）之間的折衷方案。Tab 鍵會造成混亂，最好別用。
# 換行，使一行不超過 79 個字元。
# 換行能讓使用小顯示器的使用者方便閱讀，也可以在較大顯示器上並排陳列多個程式碼檔案。
# 用空行分隔函式和 class（類別），及函式內較大塊的程式碼。
# 如果可以，把註解放在單獨一行。
# 使用說明字串。
# 運算子前後、逗號後要加空格，但不要直接放在括號內側：a = f(1, 2) + g(3, 4)。
# Class 和函式的命名樣式要一致；按慣例，命名 class 用 UpperCamelCase（駝峰式大小寫），命名函式與 method 用 lowercase_with_underscores（小寫加底線）。永遠用 self 作為 method 第一個引數的名稱（關於 class 和 method，詳見 初見 class）。
# 若程式碼是為了用於國際環境時，不要用花俏的編碼。Python 預設的 UTF-8 或甚至普通的 ASCII，就可以勝任各種情況。
# 同樣地，若不同語言使用者閱讀或維護程式碼的可能性微乎其微，就不要在命名時使用非 ASCII 字元。