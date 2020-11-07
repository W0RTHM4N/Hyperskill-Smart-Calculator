import re

variables = {}


def get_variable(input_):
    expression = input_.replace(" ", "").split("=")

    if len(expression) > 2:
        return "Invalid assignment"

    for sign in expression[0]:
        if sign.isalpha():
            continue
        else:
            return "Invalid identifier"

    if len(expression) == 1:
        return 0

    try:
        float(expression[1])
    except (ValueError, IndexError):
        if expression[1] not in variables.keys():
            return "Invalid assignment"

    variables[expression[0]] = variables[expression[1]] if expression[1] in variables.keys() else expression[1]
    return 0


def format_input(expression):
    if "**" in expression or "//" in expression:
        return 0

    new_expression = expression.replace(" ", "")

    new_expression = re.sub(r"\++", "+", new_expression)

    new_expression = re.split("(-+)", new_expression)
    for i in range(len(new_expression)):
        if "-" in new_expression[i]:
            if len(new_expression[i]) % 2 == 0:
                new_expression[i] = "+"
            else:
                new_expression[i] = "-"
    new_expression = "".join(new_expression)

    new_expression = re.split("([+\\-*/()])", new_expression)

    while "" in new_expression:
        new_expression.remove("")

    return new_expression


def to_postfix(expression):
    reversed_notation = []
    operators = []
    signs = "+-/*"

    for item in expression:
        if item == "(":
            operators.append(item)
        elif item == ")":
            left_missing = True
            while operators:
                if operators[-1] != "(":
                    reversed_notation.append(operators.pop())
                else:
                    operators.pop()
                    left_missing = False
                    break
            if left_missing:
                return 0
        elif item in signs:
            if not operators or operators[-1] == "(" or \
               item in signs[2:] and operators[-1] in signs[:2]:
                operators.append(item)
            else:
                while operators:
                    if operators[-1] in signs[:2] and item in signs[2:] or operators[-1] == "(":
                        break
                    else:
                        reversed_notation.append(operators.pop())
                operators.append(item)
        else:
            reversed_notation.append(item)

    while operators:
        reversed_notation.append(operators.pop())

    if "(" in reversed_notation or ")" in reversed_notation:
        return 0

    return reversed_notation


def evaluate(expression):
    stack = []
    for item in expression:
        if item.isdigit():
            stack.append(item)
        elif item in variables:
            stack.append(variables[item])
        elif len(stack) > 1:
            if item == "+":
                b = int(stack.pop())
                a = int(stack.pop())
                stack.append(a + b)
            elif item == "-":
                b = int(stack.pop())
                a = int(stack.pop())
                stack.append(a - b)
            elif item == "*":
                b = int(stack.pop())
                a = int(stack.pop())
                stack.append(a * b)
            elif item == "/":
                b = int(stack.pop())
                a = int(stack.pop())
                stack.append(a // b)
    return stack[0]


while True:
    command = input()

    if not command:
        continue
    elif "=" in command:
        exp = get_variable(command)
        if exp: print(exp)
        continue
    elif command == "/help":
        print("""
This program calculates the result of an expression, received as input in any format (spaces are ignored, "--" is considered a "+").

The current version doesn't support exponents (**, ^) and operates only with integers (to match the requirements of the task).

Examples:
ab = 13; - assigns the value "13" to a variable "ab"
x=0;
ab; - prints the value ("13") of the variable "ab"
23 - 1 * (x / 3) + ab;
23-1*(x/3)+ab;
23- 1*(x / 3 )+ab;
23 ---1*(x / 3) +++++++++ ab;

Commands:
/help - prints the help message
/exit - finishes the execution""")
        continue
    elif command == "/exit":
        print("Bye!")
        break
    elif command[0] == "/":
        print("Unknown command")
    elif command in variables.keys():
        print(variables[command])
    else:
        infix_notation = format_input(command)
        if not infix_notation:
            print("Invalid expression")
            continue
        if len(infix_notation) == 1:
            try:
                print(int(command))
            except ValueError:
                print("Invalid expression" if get_variable(command) else "Unknown variable")
        else:
            postfix_notation = to_postfix(infix_notation)
            if postfix_notation == 0:
                print("Invalid expression")
                continue
            try:
                print(evaluate(postfix_notation))
            except (TypeError, ValueError):
                print("Invalid expression")
