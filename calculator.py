
def addition(x, y):
    return x + y

def subtract(x, y):
    return x-y

def multiply(x, y):
    return x*y

def divide(x, y):
    if y != 0:
        return x / y
    else:
        return "Error: Cannot divide by zero"


x = float(input("Enter first number: "))
y = float(input("Enter second number: "))
operation= input("chose wish operator + - * / ")

match operation:
    case '+':
     result = addition(x, y) 
    case '-':
        result = subtract(x,y)   
    case '*' :
        result = multiply(x,y)
    case '/' :
        result = divide(x,y)     
    case _:  
        result = "Invalid operation"


print(f"The result is: {result}")


