# generated_code.py

from typing import List, Any


def add(a: int, b: int) -> int:
    """
    Return the sum of two integers.
    If non-integers are provided but are numeric, they will be converted to int.
    """
    try:
        return int(a) + int(b)
    except Exception as e:
        raise TypeError(f"add() expects two numbers that can be converted to int. Error: {e}")


def reverse_string(s: str) -> str:
    """
    Return the reversed string of s.
    If None is passed, raises a TypeError.
    """
    if s is None:
        raise TypeError("reverse_string() expects a string, got None")
    # Ensure it's a string
    s = str(s)
    return s[::-1]


def find_max(nums: List[Any]) -> Any:
    """
    Return the maximum element from a list of numbers.
    Raises ValueError if the list is empty.
    """
    if nums is None:
        raise TypeError("find_max() expects a list, got None")
    if not isinstance(nums, (list, tuple)):
        raise TypeError("find_max() expects a list or tuple of comparable items")
    if len(nums) == 0:
        raise ValueError("find_max() expects a non-empty list")

    # Use Python's built-in max which will raise if items are not comparable
    return max(nums)


# Example usage when run directly (not executed on import)
if __name__ == "__main__":
    print("add(2,3) =", add(2, 3))
    print("reverse_string('abc') =", reverse_string("abc"))
    print("find_max([1,4,2]) =", find_max([1, 4, 2]))
