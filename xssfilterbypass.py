import urllib
import random

def f1(string):

    userinput = string

    userinput = userinput.replace('<script>', '')
    userinput = userinput[:50]
    userinput = userinput.replace('"', "")
    userinput = urllib.url2pathname(userinput)
    if userinput != urllib.url2pathname(string):
        userinput = f1(userinput)

    return userinput


winlist = ['good!', 'the force is strong with this one..', 'it\'s a shrubbery!']  
print 'injection objective - {}'.format('"><script>alert("foo")<\script>')
while 1:
    userinput = raw_input('your input: ')
    a = f1(userinput)
    print 'After sanitation:\n\n{}'.format(a)
    if a == '"><script>alert("foo")<\script>':
        print random.choice(winlist)
        break
