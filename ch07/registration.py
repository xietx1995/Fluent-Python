registry = []


def register(func):
    print(f'running register({func})')
    registry.append(func)
    return func


@register
def f1():
    print('runing f1()')


@register
def f2():
    print('runing f2()')


def f3():
    print('runing f3()')


def main():
    print('running main()')
    print('registry ->', registry)
    f1()
    f2()
    f3()


if __name__ == '__main__':
    main()
