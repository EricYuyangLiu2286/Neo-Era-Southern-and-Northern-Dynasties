"""Read-only inspection of this build's tokenized spline network.

Primitive token IDs: rakaly/jomini crates/jomini/src/binary/lexer.rs.
Unknown identifiers remain hexadecimal; no guessed token dictionary or writer.
This is diagnostic evidence, not a substitute for the native engine.
"""
from pathlib import Path
import struct, sys, json, hashlib

def read(path):
    data=Path(path).read_bytes(); pos=0
    def token():
        nonlocal pos
        offset=pos; n=struct.unpack_from('<H',data,pos)[0]; pos+=2
        if n in (1,3,4): return {1:'=',3:'{',4:'}'}[n]
        fmts={12:'i',13:'f',14:'?',20:'I',359:'d',668:'Q',791:'q'}
        if n in fmts:
            f=fmts[n];v=struct.unpack_from('<'+f,data,pos)[0];pos+=struct.calcsize(f)
            return {'type':n,'value':v}
        if n in (15,23):
            size=struct.unpack_from('<H',data,pos)[0];pos+=2
            v=data[pos:pos+size].decode('utf-8');pos+=size
            return {'type':n,'value':v}
        return {'id':hex(n)}
    def block(end=False):
        result=[]
        while pos<len(data):
            x=token()
            if x=='}':
                assert end
                return result
            if x=='{':x=block(True)
            result.append(x)
        assert not end
        return result
    tree=block();assert pos==len(data)
    return data,tree

def compact(x,depth=0):
    if not isinstance(x,list):return x
    if depth>=3:return {'length':len(x),'first':x[:4]}
    return {'length':len(x),'first':[compact(v,depth+1) for v in x[:15]]}

if __name__=='__main__':
    b,t=read(sys.argv[1]);print(json.dumps({'sha256':hashlib.sha256(b).hexdigest(),'tree':compact(t)},ensure_ascii=False,indent=2))
