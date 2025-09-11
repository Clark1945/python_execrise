
### 數值運算
```python
2 + 2
>> 4
50 - 5*6
>> 20
(50 - 5*6) / 4
>> 5.0
8 / 5  # 除法總是回傳浮點數
>> 1.6
17 // 3  # 下取整除法捨棄小數部分
>> 5
17 % 3  # % 運算子回傳除法的餘數
>> 2

import math
result = 10 / 3  # 3.333...
print(math.ceil(result))  # 除法 進位輸出：4

import math
result = 10 / 3  # 3.333...
print(math.floor(result))  # 輸出：3

result = 10 / 3  # 3.333...
print(round(result))      # 輸出：3（四捨五入到整數）
print(round(result, 2))   # 輸出：3.33（保留兩位小數）

# 如果需要處理負數，math.floor() 和 math.ceil() 的行為會有所不同：
import math
print(math.floor(-3.7))  # 輸出：-4（向下取整）
print(math.ceil(-3.7))   # 輸出：-3（向上取整）
print(round(-3.7))       # 輸出：-4（四捨五入）

5**2 # 次方運算
```
### Decimal 提供整數運算
```python
from decimal import Decimal, ROUND_DOWN, ROUND_UP, ROUND_HALF_UP

# 定義兩個 Decimal 物件
a = Decimal('10')
b = Decimal('3')

# 除法運算
result = a / b
print(result)  # 輸出：3.333333333333333333333333333

from decimal import Decimal, ROUND_UP
result = Decimal('10') / Decimal('3')
print(result.quantize(Decimal('1'), rounding=ROUND_UP))  # 輸出：4
print(result.quantize(Decimal('1'), rounding=ROUND_DOWN))  # 輸出：3
print(result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))  # 輸出：3.33（保留兩位小數）
```

### Fraction 提供分數運算
```python
import math
from fractions import Fraction

result = Fraction(10, 3)
float_result = float(result)  # 轉為浮點數
print(math.ceil(float_result))   # 進位，輸出：4
print(math.floor(float_result))  # 捨去，輸出：3
print(round(float_result, 2))    # 四捨五入，輸出：3.33
```

- Python 字串無法被改變 --- 它們是 immutable。因此，嘗試對字串中某個索引位置賦值會產生錯誤：
- `string` 與 `list` 都可以 做 切片(slicing)
- 不同於字串是 immutable，list 是 mutable 型別，即改變 list 的內容是可能的
- 