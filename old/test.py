import math
from fractions import Fraction

result = Fraction(10, 3)
float_result = float(result)  # 轉為浮點數
print(math.ceil(float_result))   # 進位，輸出：4
print(math.floor(float_result))  # 捨去，輸出：3
print(round(float_result, 2))    # 四捨五入，輸出：3.

print("Good"[1:3])
print("Good"[-1])
print("Good"[-1:-3:-1])
print("Good"[::-1]) # dooG
print("Good"[-2:]) # o d

print([1] + [2,3])

rgb = ["Red", "Green", "Blue"]
rgba = rgb
print(id(rgb) == id(rgba))  # 它們參照到同一物件
rgba.append("Alpha")
print(rgba)
print(rgb)
rgb.append("AlphaGo")
print(rgb)
print(rgba)
rgba[0] = "Yallow"
print(rgb)
print(rgba)

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
# 透過將所有元素替換為空串列的方式來清空串列
letters[:] = []

class Point:
    __match_args__ = ('x', 'y') # 定義模式中屬性們的特定位置。
    def __init__(self, x, y):
        self.x = x
        self.y = y

p=Point(1,y='ANC')
match p:
    case Point(1,'ANC'):
        print('1 ANC')
    case _:
        print('1 other')

class B(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    pass

class C(B):
    pass

class D(C):
    pass

for cls in [D, C, B]:
    try:
        raise B(1,2,3,4,5)
    except D:
        print("D")
    except C:
        print("C")
    except B:
        print("B")
    except Exception as e:
        print(e)
        print(e.args)
