class TestMod:
    def __init__(self, pwnkitty):
        self.name = 'Test Module'
        self.label = 'test'
        self.action = self.test_func
        self.pwnkitty = pwnkitty
        self.help_str = 'test function'
        self.is_async = False
    def test_func(self, args):
        print('Test func success')