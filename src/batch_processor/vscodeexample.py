def greet(name):
    """Simple greeting function"""
    return f"Hello, {name}!"


def main():
    """Main function"""
    message = greet("World")
    print(message)


if __name__ == "__main__":
    main()