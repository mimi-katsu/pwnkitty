class TestMod:
    name = 'Test Module'
    label = 'test'
    help_str = 'test function'
    is_async = False
    def __init__(self, pwnkitty):
        self.pwnkitty = pwnkitty

    def test_func(args):
        print('Test func success')

    action = test_func
