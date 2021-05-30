from lzma import compress, FORMAT_XZ, CHECK_NONE, decompress, FILTER_LZMA2

from client import packaging


def main():
    # Program to check if a number is prime or not
    num = '35827166471799293901187590011469386458700646222597313289239616663581878231607847670865366492473226107023909051440722985247671490277488547367298888836712899'

    pack = packaging('Data', num)

    my_filters = [
        {"id": FILTER_LZMA2},
    ]

    num1 = compress(pack, FORMAT_XZ, CHECK_NONE, None, my_filters)

    num2 = decompress(num1)

    print("Hello")


if __name__ == "__main__":
    main()
