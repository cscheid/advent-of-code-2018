import re

r = re.compile(r"#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)")
def parse_claim(l):
    result = r.match(l.strip())
    return Claim(*(list(int(i) for i in result.groups())))

class Claim:
    def __init__(self, i, x, y, width, height):
        self.i = i
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def __repr__(self):
        return "#%s @ %s,%s: %sx%s" % (self.i, self.x, self.y, self.width, self.height)
    
def load_all_claims(l):
    claims = []
    for c in l:
        claims.append(parse_claim(c))
    claims.sort(key=lambda claim: (claim.x, claim.y))
    return claims


# plane sweep to process claims
def process_claims(claims):
    def event_key(event):
        if event[0] == 'insert':
            return (event[1].x, event[1].y)
        elif event[0] == 'delete':
            return (event[1].x + event[1].width, event[1].y + event[1].height)
        else:
            raise Exception("bad event type: %s" % event)

    events = [ ("insert", c) for c in claims ] + \
             [ ("delete", c) for c in claims ]
    events.sort(key = event_key)
    
    # points to beginning of events
    current_x = events[0][1].x

    y_interval = []
    total_claims = 0

    def event_x(event):
        if event[0] == 'insert':
            return event[1].x
        elif event[0] == 'delete':
            return event[1].x + event[1].width

    valid_claims = set()
    invalid_claims = set()
    
    def count_claims(strip_width):
        nonlocal total_claims
        claim_set = set()
        current_y = 0
        for (next_y, next_i) in y_interval:
            if len(claim_set) == 1:
                valid_claims.update(claim_set)
            if len(claim_set) > 1:
                total_claims += strip_width * (next_y - current_y)
                invalid_claims.update(claim_set)
            if next_i in claim_set:
                claim_set.remove(next_i)
            else:
                claim_set.add(next_i)
            current_y = next_y
        assert len(claim_set) == 0

    for this_event in events:
        if event_x(this_event) != current_x:
            count_claims(event_x(this_event) - current_x)
            current_x = event_x(this_event)

        if this_event[0] == 'insert':
            claim = this_event[1]
            y_interval.append((claim.y, claim.i))
            y_interval.append((claim.y + claim.height, claim.i))
            y_interval.sort(key = lambda interval: interval[0])
        elif this_event[0] == 'delete':
            y_interval = list(v for v in y_interval if v[1] != this_event[1].i)
    return (total_claims, valid_claims.difference(invalid_claims))
            

