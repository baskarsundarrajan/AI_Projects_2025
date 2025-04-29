const chats = [
    {
        "sender": "user",
        "timestamp": "9:00am",
        "chat": "Hey, can you help me write a Python function to reverse a string?"
    },
    {
        "sender": "ai",
        "timestamp": "9:01am",
        "chat": {
            "response": "Sure! Here's a simple function to reverse a string:<br/><br/>__CODEBLOCK_0__<br/><br/>Example usage:<br/><br/>__CODEBLOCK_1__",
            "code": [
                [
                    "def reverse_string(s):\n    return s[::-1]",
                    "python"
                ],
                [
                    "reverse_string(\"hello\")  # Output: 'olleh'",
                    ""
                ]
            ]
        }
    },
    {
        "sender": "user",
        "timestamp": "9:05am",
        "chat": "How do I check if a number is prime in Python?"
    },
    {
        "sender": "ai",
        "timestamp": "9:06am",
        "chat": {
            "response": "Here's a function to check if a number is prime:<br/><br/>__CODEBLOCK_0__<br/><br/>Try it like this:<br/><br/>__CODEBLOCK_1__",
            "code": [
                [
                    "def is_prime(n):\n    if n <= 1:\n        return False\n    for i in range(2, int(n ** 0.5) + 1):\n        if n % i == 0:\n            return False\n    return True",
                    "python"
                ],
                [
                    "is_prime(7)  # Output: True",
                    ""
                ]
            ]
        }
    },
    {
        "sender": "user",
        "timestamp": "9:10am",
        "chat": "Can you show me how to sort a list in Python?"
    },
    {
        "sender": "ai",
        "timestamp": "9:11am",
        "chat": {
            "response": "You can sort a list using the `sorted()` function or the `sort()` method:<br/><br/>__CODEBLOCK_0__<br/><br/>Both will give you a sorted list:<br/><br/>__CODEBLOCK_1__",
            "code": [
                [
                    "numbers = [5, 2, 9, 1]\nsorted_numbers = sorted(numbers)\nnumbers.sort()",
                    "python"
                ],
                [
                    "[1, 2, 5, 9]",
                    ""
                ]
            ]
        }
    },
    {
        "sender": "user",
        "timestamp": "9:15am",
        "chat": "What's the difference between a list and a tuple?"
    },
    {
        "sender": "ai",
        "timestamp": "9:16am",
        "chat": {
            "response": "Lists are mutable, tuples are immutable. Here's a quick example:<br/><br/>__CODEBLOCK_0__<br/><br/>Trying to modify a tuple results in an error:<br/><br/>__CODEBLOCK_1__",
            "code": [
                [
                    "my_list = [1, 2, 3]\nmy_tuple = (1, 2, 3)",
                    "python"
                ],
                [
                    "my_tuple[0] = 4  # TypeError: 'tuple' object does not support item assignment",
                    ""
                ]
            ]
        }
    },
    {
        "sender": "user",
        "timestamp": "9:20am",
        "chat": "How do I read a file in Python?"
    },
    {
        "sender": "ai",
        "timestamp": "9:21am",
        "chat": {
            "response": "You can read a file using the `open()` function:<br/><br/>__CODEBLOCK_0__<br/><br/>This will print each line in the file:<br/><br/>__CODEBLOCK_1__",
            "code": [
                [
                    "with open('file.txt', 'r') as f:\n    for line in f:\n        print(line.strip())",
                    "python"
                ],
                [
                    "# Output depends on file content",
                    ""
                ]
            ]
        }
    },
    {
        "sender": "user",
        "timestamp": "9:25am",
        "chat": "Show me how to handle exceptions in Python."
    },
    {
        "sender": "ai",
        "timestamp": "9:26am",
        "chat": {
            "response": "Use try-except blocks to handle exceptions:<br/><br/>__CODEBLOCK_0__<br/><br/>This will catch the error and print a message:<br/><br/>__CODEBLOCK_1__",
            "code": [
                [
                    "try:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print(\"Cannot divide by zero\")",
                    "python"
                ],
                [
                    "Cannot divide by zero",
                    ""
                ]
            ]
        }
    },
    {
        "sender": "user",
        "timestamp": "9:30am",
        "chat": "What's a lambda function?"
    },
    {
        "sender": "ai",
        "timestamp": "9:31am",
        "chat": {
            "response": "Lambda functions are anonymous functions. Here's an example:<br/><br/>__CODEBLOCK_0__<br/><br/>This returns 25:<br/><br/>__CODEBLOCK_1__",
            "code": [
                [
                    "square = lambda x: x * x\nsquare(5)",
                    "python"
                ],
                [
                    "25",
                    ""
                ]
            ]
        }
    },
    {
        "sender": "user",
        "timestamp": "9:35am",
        "chat": "How do I merge two dictionaries?"
    },
    {
        "sender": "ai",
        "timestamp": "9:36am",
        "chat": {
            "response": "You can use the `|` operator in Python 3.9+:<br/><br/>__CODEBLOCK_0__<br/><br/>Merged dictionary:<br/><br/>__CODEBLOCK_1__",
            "code": [
                [
                    "dict1 = {'a': 1}\ndict2 = {'b': 2}\nmerged = dict1 | dict2",
                    "python"
                ],
                [
                    "{'a': 1, 'b': 2}",
                    ""
                ]
            ]
        }
    }
]

export default chats
