class Attribute:
    SYMBOLS = ('0', '1')
    attribute = None

    def __init__(self, attribute: str):
        if attribute in self.SYMBOLS:
            self.attribute = attribute
        else:
            raise ValueError('Not a valid symbol: \'' + attribute + '\' not in ' + str(self.SYMBOLS))
    
    def __str__(self) :
        return str(self.attribute)


class Example:
    
    def __init__(self, name: str, attributes: list[Attribute]):
        
        self.name = None
        self.attributes = []

        if type(name) != str: 
            raise TypeError("name should be of type str")
        if type(attributes) != list: 
            raise TypeError("attributes should be of type list")
            
        if name:
            self.name = name
        else:
            raise ValueError('Example name should not be empty.')

        if attributes:
            for at in attributes :
                if type(at) != Attribute: 
                    raise TypeError("attributes should only contain elements of type Attribute")
                self.attributes.append(at)
        else:
            ValueError('An example should have at least one attribute.')

    def __len__(self):
        return len(self.attributes)

    # Looking forward to implement __int__ with 'base' argument. Issue: can't specify 'base' for non str object 
    def get_bin_value(self) -> int :
        return int(''.join([str(a) for a in self.attributes]),base=2)
        
    def __str__(self):
        return str((self.name,self.attributes))

    # Hamming distance
    def hamming_distance(self, e2) -> int:
        if len(self) != len(e2):
            raise ValueError(
                "Binary vectors should have same length (len<"+self.name+">=" + str(len(self)) + ",len<"+e2.name+">=" + str(len(e2))+")")
        return sum( [ int(bit) for bit in bin( Example.get_bin_value(self) ^ Example.get_bin_value(e2) )[2:]] )


class Dataset:
    examples = []
    features = []
    def __init__(self, features: list[str], examples: list[Example]):
        self.features = list.copy(features)
        print("self.features " + str(self.features))
        for example in examples:
            self.append(example)
    def __len__(self):
        return len(self.examples)
    def __str__(self):
        return "Dataset of "+str(len(self.features))+" features and " +str(len(self.examples))+" examples"

    def append(self, example: Example):
        if len(example.attributes) == len(self.features):
            self.examples.append(example)
        else :
            raise ValueError('Example <'+example.name+'> has ' + str(len(example.attributes)) + ' attribute(s): ' + str(len(self.features)) + ' required.')