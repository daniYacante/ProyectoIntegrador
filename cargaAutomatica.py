import platform
import os
#<H1,{<e3,3>,<e15,3>}>
elementos=[
    r"<H1,{<e11,0>,<e12,20>}>",
    r"<E1,{<e51,30>,<e52,10>}>",
    r"E8 <e51,30> <e52,20>",
    r"C1 <e3,30> <e15,30> 30.0",
    r"<C2,{<e4,30>,<e16,30>},30.0>",
    r"<C3,{<e8,30>,<e20,30>},30.0>",
    r"<C4,{<e31,30>,<e32,20>},30.0>",
    r"<C5,{<e27,20>,<e28,20>},30.0>",
    r"<C6,{<e3,30>,<e4,10>},30.0>",
    r"<C7,{<e28,20>,<e41,10>},30.0>",
    r"C8 <e24,20><e12,40> 10",
    r"C9 <e24,4><e12,56> 10",
    r"P1 <e24,25><e12,35> 100",
    r"<P4,{<e58,10>,<e59,10>},50.0>",
    r"<P5,{<e28,10>,<e29,10>},20.0>",
    r"<P6,{<e1,10>,<e2,10>},30.0>"
]
if platform.system()=="Linux":
    comando="python3"
elif platform.system()=="Windows":
    comando=""
os.system(f"{comando} uber.py -create_map mapa.txt")
for elm in elementos:
    os.system(f"{comando} uber.py -load_movil_element \"{elm}\"")