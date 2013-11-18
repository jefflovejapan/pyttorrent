import struct

SIZE_PSTR_LEN = 1
SIZE_RESERVED_BYTES = 8
SIZE_INFO_HASH = 20
SIZE_PEER_ID = 20
HANDSHAKE_WITHOUT_PROTOCOL_LEN = 49
SIZE_TOTAL_HANDSHAKE = 68

class Handshake(object):
    def __init__(self, peer_id='',  
            pstr='BitTorrent protocol', 
            reserved='\x00\x00\x00\x00\x00\x00\x00\x00', 
            info_hash='', handshake_str=''):
        
        if not peer_id and not info_hash:
            if not handshake_str:
                raise Exception('Expected argument handshake_str.')
            else:
                if len(handshake_str) != SIZE_TOTAL_HANDSHAKE:
                    raise Exception('Incorrect handshake size.')
                pstrlen, pstr, reserved, info_hash, peer_id = self.explode(handshake_str)
        
        elif handshake_str:
            raise Exception('Unexpected argument handshake_str.')
        
        self.peer_id = peer_id
        self.pstrlen = len(pstr)
        self.pstr = pstr
        self.reserved = reserved
        self.info_hash = info_hash


    def explode(self, handshake_str):
        start_i = 0
        pstrlen = struct.unpack('B', handshake_str[start_i])[0]
        
        # JEFF - maybe choose a more radically different constant name to not 
        # confuse with pstrlen variable or...
        start_i += SIZE_PSTRLEN
        pstr = handshake_str[start_i : pstrlen + start_i]
        
        # JEFF - do len(pstr) here -- no need for separate var
        start_i += pstrlen
        reserved = handshake_str[start_i : start_i + SIZE_RESERVED_BYTES]
        
        start_i += SIZE_RESERVED_BYTES
        info_hash = handshake_str[start_i : start_i + SIZE_INFO_HASH]
        
        start_i += SIZE_PEER_ID
        peer_id = handshake_str[start_i:]
        
        return pstrlen, pstr, reserved, info_hash, peer_id


    def __str__(self):
        return "%s%s%s%s%s" % (chr(self.pstrlen), self.pstr, self.reserved, self.info_hash, self.peer_id,)


def parse_handshake(buffer):
    if not buffer:
        return None, buffer
    # JEFF - maybe add method to check that this is the BitTorrent protocol
    pstr_len = struct.unpack('B', buffer[0])[0]
    handshake_size = pstr_len + HANDSHAKE_WITHOUT_PROTOCOL_LEN

    if handshake_size <= len(buffer):
        handshake = Handshake(handshake_str = buffer[0:handshake_size])
        return handshake, buffer[handshake_size:]
    else:
        return None, buffer