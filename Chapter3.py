# -*- coding: UTF-8 -*-
# 檔案以UTF-8運行
# 含括 Python官方文件教學手冊第9至12章

# 9 類別
# 建立一個列表


# 命名空間是從名稱到物件的對映。大部分的命名空間現在都是以 Python 的 dictionary 被實作，但通常不會以任何方式被察覺（除了性能），且它可能會在未來改變。
# 命名空間的例子有：內建名稱的集合（包含如 abs() 的函式，和內建的例外名稱）；模組中的全域 (global) 名稱；和在函式調用中的區域 (local) 名稱。

# 例如，運算式中的 z.real，real 是物件 z 的一個屬性。嚴格來說，模組中名稱的參照都是屬性參照：在運算式 modname.funcname 中，
# modname 是模組物件而 funcname 是它的屬性。在這種情況下，模組的屬性和模組中定義的全域名稱碰巧有一個直接的對映：他們共享了相同的命名空間！

# 屬性可以是唯讀的或可寫的。在後者的情況下，對屬性的賦值是可能的。模組屬性是可寫的：你可以寫 modname.the_answer = 42。可寫屬性也可以用 del 陳述式刪除。
# 例如，del modname.the_answer 將從名為 modname 的物件中刪除屬性 the_answer。

# 命名空間在不同的時刻被建立，並且有不同的壽命。當 Python 直譯器啟動時，含有內建名稱的命名空間會被建立，並且永遠不會被刪除。
# 當模組定義被讀入時，模組的全域命名空間會被建立；一般情況下，模組的命名空間也會持續到直譯器結束。
# 被直譯器的頂層調用 (top-level invocation) 執行的陳述式，不論是從腳本檔案讀取的或是互動模式中的，會被視為一個稱為 __main__ 的模組的一部分，因此它們具有自己的全域命名空間。（內建名稱實際上也存在一個模組中，它被稱為 builtins。）

# 命名空間的生命周期
# Python 中的命名空間有不同的生命週期，這決定了變數的可用性：

# 內建命名空間（Built-in Namespace）

# 內建函式（如 len()、print()）和異常（如 Exception）都位於 builtins 模組中。
# 這個命名空間自 Python 啟動時就存在，並且 直到直譯器結束才會消失。
# 全域命名空間（Global Namespace）

# 這是模組的命名空間，例如在 mymodule.py 中定義的變數 the_answer 就位於 mymodule 的全域命名空間。
# 這個命名空間 通常持續到程式結束。
# 區域命名空間（Local Namespace）

# 這是函式或方法執行時建立的變數範圍，函式執行完畢後，這個命名空間就會被釋放。

def scope_test():
    def do_local():
        spam = "local spam"

    def do_nonlocal():
        nonlocal spam
        spam = "nonlocal spam"

    def do_global():
        global spam
        spam = "global spam"

    spam = "test spam"
    do_local()
    print("After local assignment:", spam)
    do_nonlocal()
    print("After nonlocal assignment:", spam)
    do_global()
    print("After global assignment:", spam)

scope_test()
print("In global scope:", spam)


# 當進入 class definition，一個新的命名空間將會被建立，並且作為區域作用域——因此，所有區域變數的賦值將進入這個新的命名空間。特別是，函式定義會在這裡連結新函式的名稱。

# 正常地（從結尾處）離開 class definition 時，一個 class 物件會被建立。基本上這是一個包裝器 (wrapper)，裝著 class definition 建立的命名空間內容；
# 我們將在下一節中更加了解 class 物件。原始的區域作用域（在進入 class definition 之前已生效的作用域）會恢復，在此 class 物件會被連結到 class definition 標頭中給出的 class 名稱（在範例中為 ClassName）。


# 屬性參照(attribute reference)
class MyClass:
    """一個簡單的類別範例"""
    i = 12345
    def f(self):
        return 'hello world'
MyClass.i

# 實例化(instantiation)
def __init__(self):
    self.data = []

class Dog:

    kind = 'canine'         # class variable shared by all instances

    def __init__(self, name):
        self.name = name    # instance variable unique to each instance

d = Dog('Fido')
e = Dog('Buddy')
d.kind                  # shared by all dogs
'canine'
e.kind                  # shared by all dogs
'canine'
d.name                  # unique to d
'Fido'
e.name                  # unique to e
'Buddy'

# 如果屬性名稱同時出現在一個實例和一個 class 中，則屬性的尋找會以實例為優先：。
class Warehouse:
   purpose = 'storage'
   region = 'west'

w1 = Warehouse()
print(w1.purpose, w1.region)
# storage west
w2 = Warehouse()
w2.region = 'east'
print(w2.purpose, w2.region)
# storage east
# 資料屬性可能被 method 或是被物件的一般使用者（「客戶端」）所參照。也就是說，class 不可用於實作純粹抽象的資料型別。事實上，在 Python 中沒有任何可能的方法，可強制隱藏資料——這都是基於慣例。（另一方面，以 C 編寫的 Python 實作可以完全隱藏實作細節並且在必要時控制物件的存取；這可以被以 C 編寫的 Python 擴充所使用。）
class BaseClassName:
    i=0
class DerivedClassName(BaseClassName):
    i=0

# 執行 derived class 定義的過程，與執行 base class 相同。當 class 物件被建構時，base class 會被記住。這是用於解析屬性參照：如果一個要求的屬性無法在該 class 中找到，則會繼續在 base class 中搜尋。假如該 base class 本身也是衍生自其他 class，則這個規則會遞迴地被應用。

# class DerivedClassName(BaseClassName, Base3):
#     pass

# 在大多數情況下，最簡單的例子裡，你可以這樣思考，對於繼承自 parent class（父類別）的屬性，其搜尋規則為：深度優先、從左到右、在階層裡重疊的相同 class 中不重複搜尋。因此，假如有一個屬性在 DerivedClassName 沒有被找到，則在 Base1 搜尋它，接著（遞迴地）在 Base1 的 base class 中搜尋，假如在那裡又沒有找到的話，會在 Base2 搜尋，依此類推。

# 「私有」(private) 實例變數，指的是不在物件內部便無法存取的變數，這在 Python 中是不存在的。但是，大多數 Python 的程式碼都遵守一個慣例：前綴為一個底線的名稱（如：_spam）應被視為 API （應用程式介面）的非公有 (non-public) 部分（無論它是函式、方法或是資料成員）。這被視為一個實作細節，如有調整，亦不另行通知。

# 既然 class 私有的成員已有一個有效的用例（即避免名稱與 subclass 定義的名稱衝突），這種機制也存在另一個有限的支援，稱為 name mangling（名稱修飾）。任何格式為 __spam（至少兩個前導下底線，最多一個尾隨下底線）的物件名稱 (identifier) 會被文本地被替換為 _classname__spam，在此 classname 就是去掉前導下底線的當前 class 名稱。只要這個修飾是在 class 的定義之中發生，它就會在不考慮該物件名稱的語法位置的情況下完成。

# 產生器是一個用於建立疊代器的簡單而強大的工具。它們的寫法和常規的函式一樣，但當它們要回傳資料時，會使用 yield 陳述式。每次在產生器上呼叫 next() 時，它會從上次離開的位置恢復執行（它會記得所有資料值以及上一個被執行的陳述式）。
def reverse(data):
    for index in range(len(data)-1, -1, -1):
        yield data[index]
for char in reverse('golf'):
    print(char)

# 某些簡單的產生器可以寫成如運算式一般的簡潔程式碼，所用的語法類似 list comprehension（串列綜合運算），但外層為括號而非方括號。這種運算式被設計用於產生器將立即被外圍函式 (enclosing function) 所使用的情況。產生器運算式與完整的產生器定義相比，程式碼較精簡但功能較少，也比等效的 list comprehension 更為節省記憶體。
sum(i*i for i in range(10))                 # sum of squares
285

xvec = [10, 20, 30]
yvec = [7, 5, 3]
sum(x*y for x,y in zip(xvec, yvec))         # dot product
260

unique_words = set(word for line in page  for word in line.split())

valedictorian = max((student.gpa, student.name) for student in graduates)

data = 'golf'
list(data[i] for i in range(len(data)-1, -1, -1))
['f', 'l', 'o', 'g']

# 對於日常檔案和目錄管理任務，shutil 模組提供了更容易使用的高階介面：
import shutil
shutil.copyfile('data.db', 'archive.db')
'archive.db'
shutil.move('/build/executables', 'installdir')

# glob 模組提供了一函式可以從目錄萬用字元中搜尋並產生檔案列表：
import glob
glob.glob('*.py')
['primes.py', 'random.py', 'quote.py']

# 通用工具腳本常需要處理命令列引數。這些引數會以 list（串列）形式存放在 sys 模組的 argv 屬性中。例如以下 demo.py 檔案：
import sys
print(sys.argv)
['demo.py', 'one', 'two', 'three']

# argparse 模組提供了一種更複雜的機制來處理命令列引數。以下腳本可擷取一個或多個檔案名稱，並可選擇要顯示的行數：
import argparse

parser = argparse.ArgumentParser(
    prog='top',
    description='Show top lines from each file')
parser.add_argument('filenames', nargs='+')
parser.add_argument('-l', '--lines', type=int, default=10)
args = parser.parse_args()
print(args)