#
# vim:fenc=utf-8:ff=unix:ts=4:sw=4:sts=4:et:

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
        pat_01=[1 if c.isupper() else 0 for c in p]
        ports=[all_port[ord(c)-ord('A')] for c in p.upper()]
    return ports,pat_01,count
if __name__=='__main__':
    #DEBUG
    all_port=(3,5,7,11,13)
    for pat_str in '''AbEdC
        Z
        z
        10100
        ACedb 30'''.split("\n"):
        print(pat_str.strip())
        print(parse_pattern(all_port,pat_str))
