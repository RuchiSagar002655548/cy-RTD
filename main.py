from my-test-package.sample_module import say_hello

print(say_hello())

def greet(name: str) -> str:
    """
    Greet the user with the given name.

    :param name: Name of the user.
    :return: A greeting message.
    """
    return f"Hello, {name}!"


def add(self, a: int, b: int) -> int:
    """
    Add two numbers.

    :param a: First number.
    :param b: Second number.
    :return: Sum of the numbers.
    """
    return a + b

    
    
