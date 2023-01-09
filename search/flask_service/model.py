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
            self.attributes = [str(at) for at in attributes]
        else:
            ValueError('An example should have at least one attribute.')

    def __len__(self):
        return len(self.attributes)

    def __int__(self,base:int=10):
        return int(''.join(self.attributes),base=base)

    def __str__(self):
        return str((self.name,self.attributes))

    # Hamming distance
    def hamming_distance(self, e2) -> int:
        if len(self) != len(e2):
            raise ValueError(
                "Binary vectors should have same length (len<"+self.name+">=" + str(len(self)) + ",len<"+e2.name+">=" + str(len(e2))+")")
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
        if len(example) == len(self.features):
            self.examples.append(example)
        else :
            raise ValueError('Example <'+example.name+'> has ' + str(len(example)) + ' feature(s): ' + str(len(self.features)) + ' required.')