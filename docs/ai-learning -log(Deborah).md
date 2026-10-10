unittest Asserections is a way in which python check if the result is what is expected
```python
import unittest

def add(a, b):
    return a + b 


class TestAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

if __name__ == "__main__":
    unittest.main()

```

1. IMPORT UNITTEST:
import unittest import python's built-in testing tools.

2. class TestAdd(unittest.TestCase):
it create a class for our test.

3. def test_add(self):
this is the test function, python uses the naming to discover test method automatically.

4. self.assertEqual(add(2, 3), 5)

five(5) most important uinittest Asserections:
1. assertEqual():
   it checks weather two values are equal .

2. assertNotEqual()
   it checks weather two values are not equal, it also means this two value should be different.

3. assertTrue()
   it checks weather something is True.

4. assertFalse()
   it checks weather something is False.

5. assertin()
   it checks weather something exist in another thing, such as list or a string.


DATACLASS
dataclass is a special kind of class that make it easier to store data.

```python
from dataclasses import dataclass
@dataclass
class Ticket:
    id: str
    title: str
    category: str
    affected_users: int
    priority: str
    status: str
    assigned_to: bool

Ticket1 = Ticket("T001", "Campus Wi-Fi is down", "Network", "high", 15, "critical", "open", None)
print(Ticket1)

```

1. import dataclass:
   it gives us access to python's dataclass decorator.

2. @dataclass:
   it tells python to give the class some automatically generated methods.

dataclass does the followng automatically:
1. it creates ___init__().
2. it creates a useful string representation.
3. it allows us to compare objects.
