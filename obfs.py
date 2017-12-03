import math
import ast 
import codegen
import random
import string
import binascii
import zlib
import __builtin__

#cool thing based on an AST obfuscation article @jbremer.org that i played around with a bit.
#things this currently doesn't support:
#1. for..else..(used as obfuscation method+why would you even write something with a horrid syntax like that willingly)
#2. removing docstrings - later
#5. obj.func() doesn't replace func
#3. maybe other things, this wasn't tested very thoroughly:D


myprintables = string.printable.replace('{','').replace('}','') #maybe causing errors?
funxceptions = ['next']
aliases = {}
classes = []
funcs = []
def rename(st):
    return 'a'+str(zlib.adler32(st))

class hidinglol(ast.NodeTransformer):

    def visit_Str(self, node):
        if '{' in node.s or '}' in node.s:
            return node
        k = len(node.s)
        c = 1 if k >= 3 else 5 if k == 1 else 0 if k==0 else random.randint(2,4)
        if c==0:
            return ast.Str(s='')
        if c ==1:
            ran = random.randint(0,1)
            aleft=ast.Str(s=node.s[:len(node.s)/2+ran:])
            aright=ast.Str(s=node.s[len(node.s)/2+ran::])
            
            #if len(aleft.s) > 2:
            aleft = self.visit_Str(aleft)
            #if len(aright.s) > 2:
            aright = self.visit_Str(aright)
            return ast.BinOp(left=aleft,op=ast.Add(),right=aright)
        elif c==2: 
            return ast.Subscript(value=self.visit_Str(ast.Str(s=node.s[::-1])),slice=ast.Slice(lower=None,upper=None,step=ast.Num(n=-1)),ctx=ast.Load())
        
        elif c==3: 
            
            l=len(node.s)
            pre,suf = ''.join([random.choice(myprintables) for i in range(random.randint(1,2*l))]),''.join([random.choice(myprintables) for i in range(random.randint(1,2*l))])
      
            return ast.Subscript(value=ast.Str(s=pre+node.s+suf),slice=ast.Slice(lower=ast.Num(n=len(pre)),upper=ast.Num(n=len(pre)+l),step=ast.Num(n=1)),ctx=ast.Load())

        elif c==4: 
            step = random.randint(1,3)
            l=len(node.s)
            stuff = iter(node.s)
            res = ''.join([random.choice(myprintables) if i%step else stuff.next() for i in range(0,l*(step))])
            return ast.Subscript(value=ast.Str(s=res),slice=ast.Slice(lower=None,upper=None,step=ast.Num(n=step)),ctx=ast.Load())

        elif c==5:
            return ast.Call(func=ast.Name(id='chr',ctx=ast.Load()),args=[ast.Num(n=ord(node.s))],keywords=[],starargs=None,kwargs=None)

                              

    def visit_Num(self,node):
        if type(node.n)==int:
            return ast.Call(func=ast.Name(id='int',ctx=ast.Load()),args=[self.visit_Str(ast.Str(s=bin(node.n))),ast.Num(n=2)],keywords=[],starargs=None,kwargs=None)


        return node
    def visit_For(self,node): #in testing:)
        #add more convincing junk for loop(random choice of a few seemingly important code lines that dont do anything)
        fortarget=self.visit(ast.Name(id=''.join([random.choice(string.ascii_letters) for i in range(random.randint(3,8))]),ctx=ast.Load))
        junkfor = [ast.Assign(targets=[self.visit(node.target)],ctx=ast.Store(),
                    value=self.visit(ast.Num(n=id(''.join([random.choice(string.ascii_letters) for i in range(random.randint(3,8))]))))),
                   ast.If(test=ast.Compare(left=self.visit(node.target),ops=[ast.Eq()],comparators=[ast.Call(func=ast.Name(id='id',ctx=ast.Load()),args=[fortarget],keywords=[],starargs=None,kwargs=None)]),
                          body=[ast.Assign(targets=[self.visit(node.target)],ctx=ast.Store(),value=ast.BinOp(left=self.visit(node.target),op=ast.Sub(),
                            right=self.visit(ast.Num(n=1)))),ast.Assign(targets=[fortarget],ctx=ast.Store(),value=ast.BinOp(left=self.visit(node.target),op=ast.Add(),
                            right=self.visit(node.target)))],orelse=[])]
        return ast.For(target=fortarget,iter=ast.Call(func=ast.Name(id='range',ctx=ast.Load()),args=[self.visit(ast.Num(n=random.randint(10,100)))],keywords=[],starargs=None,kwargs=None),body=junkfor,orelse=[ast.For(target=self.visit(node.target),iter=self.visit(node.iter),body=[self.visit(i) for i in node.body],orelse=[self.visit(i) for i in node.orelse])])

    def visit_Name(self,node):
        print node.id
        if node.id == 'self':
            return node
        if node.id in aliases:
            return ast.Name(id=(rename(aliases[node.id]))) # super mega bad, if we have import os as ohnoes;ohnoes=ohnoes.getcwd()..
        if(node.id in vars(__builtin__).keys()):
            return node
        return ast.Name(id=(rename(node.id)))

    def visit_Import(self,node):
        for i in node.names:
            if i.asname:
                aliases[i.asname] = i.name
        return ast.Import(names=[ast.alias(name=i.name,asname=(rename(i.name))) for i in node.names])

    def visit_ImportFrom(self,node):
        return ast.ImportFrom(level=0,module=node.module,names=[ast.alias(name=i.name,asname=(rename(i.name))) for i in node.names])
    def visit_ClassDef(self,node):
        #print node.id
        global classes
        classes += [node.name]
        return ast.ClassDef(name=(rename(node.name)),bases=[self.visit(i) for i in node.bases],body=[self.visit(i) for i in node.body],decorator_list=node.decorator_list)

#really problematic:(
    def visit_Attribute(self,node):
        if isinstance(node.value,ast.Name):
            print '{}.{}'.format(node.value.id,node.attr)
        if 1: #should be - if this is something defined within the module
            return ast.Attribute(value=self.visit(node.value),attr=(rename(node.attr)),ctx=node.ctx)
        else:
            return node
        
    def visit_FunctionDef(self,node):
        global funcs
        funcs += [node.name]
        if node.name[:2]=='__' or node.name in funxceptions:
            newname=node.name
        else:
            newname=(rename(node.name))
        
        return ast.FunctionDef(name=newname,
                               args=ast.arguments(kwarg=node.args.kwarg,vararg=node.args.vararg,defaults=[self.visit(i) for i in node.args.defaults],args=[ast.Name(id=(rename(i.id)),ctx=ast.Param()) if i.id != 'self' else ast.Name(id='self',ctx=ast.Param()) for i in node.args.args]),decorator_list=node.decorator_list,body=[self.visit(i) for i in node.body],
                        )
a=hidinglol()               
tree=ast.parse(open(r'fileshell.py','r').read())
tree=a.visit(tree)
val = codegen.to_source(tree)
print val
f=open(r'simplecode.py','w')
f.write(val)
f.close()

def isp(n):
    if n in [0,1]:
        return 0
    for i in range(2,int(n**0.5+1)):
        if not n%i:
            return 0
    return 1

def divs(n):
    
    res = []
    if isp(n):
        return [n]
    for i in range(2,int(n**0.5+1)):
        if not n%i:
            res = res + divs(n/i) + [i]
            break  
    return res
def f6(n):
    d={}
    for i in divs(n):
        if i in d:
            d[i]+=1
        else:
            d[i]=1

    return d
