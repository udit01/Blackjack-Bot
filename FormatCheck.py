import sys;

def Check(name):
    f=open(name);   
    Names=["5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","A2","A3","A4","A5","A6","A7","A8","A9","22","33","44","55","66","77","88","99","1010","AA"];
    Options=["H","D","S","P"];
    if(not(len(f.readlines()) == len(Names))):
        print("Incorrect Number of Lines");
        return False;
    cou=0;   
    for l in f.readlines():
        sp=l.strip().split('\t');
        if(not(sp[0]==Names[cou]) or not(len(sp)==2)):
            print("Line Format Incorrect");
            return False;
        sp=    [ob in Options for ob in sp[1].split()];
        if(not(len(sp)==10)):   
            print("Line Format Incorrect");
            return False;
               
    return True;
def main():

    if(not(len(sys.argv) == 2)):
        print("Exactly one command line argument required");
        sys.exit();
    else:
        print(Check(sys.argv[1]));
       
if __name__ == "__main__":
    main()