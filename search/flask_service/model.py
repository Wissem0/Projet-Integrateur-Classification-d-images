class Attribute:
    SYMBOLS = ('0', '1')
    attribute = None

    def __init__(self, attribute: str):
        if attribute in self.SYMBOLS:
            self.attribute = attribute
        else:
            raise ValueError('Not a valid symbol: \'' + attribute + '\' not in ' + str(self.SYMBOLS))


class Example:
    name = None
    attributes = None
    def __init__(self, name: str, attributes: list[Attribute]):
        if name:
            self.name = name
        else:
            raise ValueError('Example name should not be empty.')

        if attributes:
            self.attributes = attributes
        else:
            ValueError('An example should have at least one attribute.')

    def __len__(self):
        return len(self.attributes)

    def __int__(self,base:int=10):
        s = ""
        for at in self.attributes :
            s+=at
        return int(s,base=base)

    def __str__(self):
        return str((self.name,self.attributes))

    # Hamming distance
    def distance(self, e2) -> int:
        if len(self) != len(e2):
            raise ValueError(
                "Binary vectors should have same length (len(e1)=" + str(len(self)) + ",len(e2)=" + str(len(e2))+")")
        return sum( [ int(bit) for bit in bin( Example.__int__(self, base=2) ^ Example.__int__(e2, base=2) )[2:]] )


class Dataset:
    examples = []
    features = []
    def __init__(self, features: list[str], examples: list[Example]):
        self.features = features
        for example in examples:
            self.append(example)
    def __len__(self):
        return len(self.examples)
    def __str__(self):
        return "Dataset of "+str(len(self.features))+" features and " +str(len(self.examples))+" examples"

    def append(self, example: Example):
        if len(example) == len(self.features) and not self.examples:
            raise ValueError('Example has ' + str(len(example)) + ' feature: ' + len(self.features) + ' required.')
        self.examples.append(example)