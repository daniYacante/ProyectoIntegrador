import platform
import os
#<H1,{<e3,3>,<e15,3>}>
elementos=[
    r"<H1,{<e11,0>,<e12,2>}>",
    r"<E1,{<e51,3>,<e52,1>}>",
    r"<C1,{<e3,3>,<e15,3>},30.0>",
    r"<C2,{<e4,3>,<e16,3>},30.0>",
    r"<C3,{<e8,3>,<e20,3>},30.0>",
    r"<C4,{<e31,3>,<e32,2>},30.0>",
    r"<C5,{<e27,2>,<e28,2>},30.0>",
    r"<C6,{<e3,3>,<e4,1>},30.0>",
    r"<C7,{<e28,2>,<e41,1>},30.0>",
    r"<P4,{<e58,1>,<e59,1>},50.0>",
    r"<P5,{<e28,1>,<e29,1>},20.0>",
    r"<P6,{<e1,1>,<e2,1>},30.0>"
]
if platform.system()=="Linux":
    comando="python3"
elif platform.system()=="Windows":
    comando=""
os.system(f"{comando} uber.py -create_map mapa.txt")
for elm in elementos:
    os.system(f"{comando} uber.py -load_movil_element \"{elm}\"")