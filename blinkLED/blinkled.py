#
# vim:fenc=utf-8:ff=unix:ts=4:sw=4:sts=4:et:
import RPi.GPIO as GPIO
import sys
import time

def parse_pattern(all_port,pattern_str):
    '''parse a config line in pattern text file

    config line format: <pattern> [<count>]
    <pattern>:
        01(needs for all_port)
        Aa(for part of all_port), Zz(means all_port)
    <count>: decimal, specify how long time continue this pattern'''
    p=pattern_str.strip().split()
    #default count=10
    if len(p)>=2:
        count=int(p[1])
    else:
        count=10
    #convert pattern to ports and pat_01
    p=p[0]
    if p[0] in '01Zz':
        ports=all_port
        if p[0]=='Z':
            pat_01=[1]*len(all_port)
        elif p[0]=='z':
            pat_01=[0]*len(all_port)
        else:
            pat_01=[1 if c=='1' else 0 for c in p[:len(all_port)]]
    else:
        pat_01=[]
        ports=[]
        for c in p:
            idx=ord(c.upper())-ord('A')
            if idx<len(all_port):
                pat_01.append(1 if c.isupper() else 0)
                ports.append(all_port[idx])
    return ports,pat_01,count

def gen_patterns(files):
    if len(files)==0:
        files=["pattern.txt"]
    for f in files:
        with open(f) as fn:
            for l in fn:
                l=l.strip()
                if l[0]=="#":
                    continue
                yield l

if __name__=='__main__':
    all_port=(5,7,11,13)
    #INIT-OUT all_port
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    for p in all_port:
        GPIO.setup(p,GPIO.OUT)
    #run patterns
    for pat_str in gen_patterns(sys.argv[1:]):
        print(pat_str)
        port,pattern,n=parse_pattern(all_port,pat_str)
        for pn,on in zip(port,pattern):
            GPIO.output(pn,GPIO.HIGH if on==1 else GPIO.LOW)
            pass
        time.sleep(0.01*n)
    #CLOSE-IN all_port
    for pn in all_port:
        GPIO.output(pn,GPIO.LOW)
        GPIO.setup(pn,GPIO.IN)
