# TODO: Should I do this or not ????
class BinaryAttribute:
    SYMBOLS = ('0', '1')

    def __init__(self, attribute: str):
        if attribute in self.SYMBOLS:
            self.attribute = attribute
        else:
            raise ValueError('Not a valid symbol: \'' + attribute + '\' not in ' + str(self.SYMBOLS))


class Example:
    def __init__(self, name: str, attributes: list[BinaryAttribute]):
        if name:
            self.name = name
        else:
            raise ValueError('Example name should not be empty.')

        if attributes:
            self.attributes = attributes
        else:
            ValueError('An example should have at least one attribute.')

    def __len__(self):
        len(self.attributes)


class Dataset:
    examples = []

    def __init__(self, features: list[str], examples: list[Example]):
        self.features = features
        for example in examples:
            self.append(example)

    def append(self, example: Example):
        if len(example) == len(self.features) and not self.examples:
            raise ValueError('Example has ' + str(len(example)) + ' feature: ' + len(self.features) + ' required.')
        self.examples.append(example)
