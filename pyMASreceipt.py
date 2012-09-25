import asn1
from collections import namedtuple
MASattr = namedtuple('MASattr', 'type version value')

MAS_types = { 2: 'Bundle Identifier',
              3: 'Application Version',
              4: 'Opaque Value',
              5: 'SHA-1 Hash',
             17: 'In-App Purchase Receipt' }

def unwind(input):
    ret_val = []
    while not input.eof():
        tag = input.peek()
        if tag[1] == asn1.TypePrimitive:
            tag, value = input.read()
            ret_val.append((tag[2], tag[0], value))
        elif tag[1] == asn1.TypeConstructed:
            ret_val.append((tag[2], tag[0]))
            input.enter()
            ret_val.append(unwind(input))
            input.leave()
    return ret_val

def extract_data(asn1_seq):
    ret_val = []
    for i,x in enumerate(asn1_seq):
        if (type(x) is tuple):
            if len(x) == 3:
                if x[2] == '1.2.840.113549.1.7.1':
                    ret_val.append(asn1_seq[i+2][0][2])
        elif (type(x) is list):
            sub_val = extract_data(x) 
            if (type(sub_val) is list):
                ret_val.extend(sub_val)
            else:
                ret_val.append(sub_val)
    if len(ret_val) == 1:
        return ret_val[0]
    return ret_val

def parse_receipt(rec):
    ret_val = []
    for y in [z for z in rec if type(z) is list]:
        try:
            dec = asn1.Decoder()
            dec.start(y[2][2])
            ret_val.append(MASattr(MAS_types.get(y[0][2], '0x%02X' % y[0][2]), y[1][2], unwind(dec)[0][-1]))
        except:
            ret_val.append(MASattr(MAS_types.get(y[0][2], '0x%02X' % y[0][2]), y[1][2], y[2][2]))
    return ret_val

dec = asn1.Decoder()
# Read from the 'receipt' file
dec.start(open('receipt', 'rb').read())
payload = extract_data(unwind(dec))
dec = asn1.Decoder()
dec.start(payload)

# Final decoded receipt is here
receipt = parse_receipt(unwind(dec)[1])
