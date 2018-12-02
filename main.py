ANCHORS_FULLTIME = []
ANCHORS_DEFAULT_NUMBER = 2

class Day(object):
    def __init__(self):
        self.blocks = []

    def __repr__(self):
        output = ''
        for block in self.blocks:
            output += str(block) + '\n'
        return output


class Block(object):
    def __init__(self, hour, **kwargs):
        # Require kwargs
        # self.name
        self.hour = hour  # upgrade to datetime and timedelta length
        
        # Default 2 anchors per block
        if 'num_anchors' in kwargs:
            self.num_anchors = kwargs['num_anchors']
        else:
            self.num_anchors = ANCHORS_DEFAULT_NUMBER

        # Default allow any anchor
        if 'matching_anchors' in kwargs:
            self.matching_anchors = self.matching_anchors
        else:
            self.matching_anchors = ANCHORS_FULLTIME

        # Optionally set specific anchors
        if 'anchors' in kwargs:
            self.anchors = kwargs['anchors']
        else:
            self.anchors = []

    def __repr__(self):
        if self.anchors:
            anchors = self.anchors
        else:
            anchors = 'Empty'
        return f'Block {self.hour}, {self.num_anchors} anchors: {anchors}'


class Anchor(object):
    def __init__(self, name, **kwargs):
        self.name = name

    def __repr__(self):
        return self.name



if __name__ == "__main__":
    nora = Anchor(name='Nora')
    brad = Anchor(name='Brad')
    baker = Anchor(name='Baker')
    hope = Anchor(name='Hope')
    kristen = Anchor(name='Kristen')
    tim = Anchor(name='Tim')

    day = Day()
    for i in range(1, 10):
        day.blocks.append(
            Block(
                hour=i,
                anchors=[nora]
            )
        )

    print(day)
    