import asn1
from collections import namedtuple
MASattr = namedtuple('MASattr', 'type version value')

# The following attributes were determined from looking at the JSON attributes for a MAS app and the output
# of mdls /path/to/the.app and comparing values to the receipt dump:
#
# 0x01: Product ID - can be used with: http://itunes.apple.com/WebObjects/MZStore.woa/wa/viewSoftware?id=PRODUCTID&mt=8
# 0x04: Opaque Value = Unique Mac App Store compatible numeric mapping to AppleID
#                      as discovered by MagerValp here: http://magervalp.github.com/2013/03/19/poking-around-in-masreceipts.html
#                      Also used in: com.apple.storeagent
# 0x08: Purchase Date
# 0x0A: Parental Content Rating
# 0x10: kMDItemAppStoreInstallerVersionID
#
# Additional material for reading: http://www.mactech.com/sites/default/files/Jalkut-Would_You_Like_a_Receipt_With_That.pdf
# Seems to indicate a few new types:
# 0x00: Receipt type
# 0x0C: LastAuthTime as seen in com.apple.storeagent (likely set at time of download?)
# 
# Apple documentation:
# https://developer.apple.com/library/mac/releasenotes/General/ValidateAppStoreReceipt/Chapters/ReceiptFields.html
# 0x13: Original version number of application purchased
# 0x15: Receipt expiration date
#
# More are listed in the Apple documentation regarding In-App purchases

MAS_types = { 1: 'Product ID',
              2: 'Bundle Identifier',
              3: 'Application Version',
              4: 'Opaque Value',
              5: 'SHA-1 Hash',
              8: 'Purchase Date',
             10: 'Parental Content Rating',
             16: 'App Store Installer Version ID',
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
