class Verifier:
    def __init__(self, _verifier_num, _creteria_num) -> None:
        self.verifier_num=_verifier_num
        self.creteria_num=_creteria_num
 
    def verifier_TF(self, t, s, c):
        return verifier_list[self.verifier_num-1][self.creteria_num](t, s, c)
        
    def possibleComb(self):
        comb = set()
        for t in range(1, 6):
            for s in range(1, 6):
                for c in range(1, 6):
                    if self.verifier_TF(t, s, c):
                        comb.add((t, s, c))
        return comb
   
#region verifier functions

def verifier1_0(t, s, c):
    if t==1: return True
    else: return False

def verifier1_1(t, s, c):
    if t>1: return True
    else: return False
    
def verifier2_0(t, s, c):
    if t<3: return True
    else: return False
    
def verifier2_1(t, s, c):
    if t==3: return True
    else: return False
    
def verifier2_2(t, s, c):
    if t>3: return True
    else: return False
    
def verifier3_0(t, s, c):
    if s<3: return True
    else: return False
    
def verifier3_1(t, s, c):
    
    if s==3: return True
    else: return False
    
def verifier3_2(t, s, c):
    if s>3: return True
    else: return False
    
def verifier4_0(t, s, c):
    if s<4: return True
    else: return False
    
def verifier4_1(t, s, c):
    
    if s==4: return True
    else: return False
    
def verifier4_2(t, s, c):
    if s>4: return True
    else: return False
    
def verifier5_0(t, s, c):
    if t%2==0: return True
    else: return False
    
def verifier5_1(t, s, c):
    if t%2==1: return True
    else: return False
    
def verifier6_0(t, s, c):
    if s%2==0: return True
    else: return False
    
def verifier6_1(t, s, c):
    if s%2==1: return True
    else: return False
    
def verifier7_0(t, s, c):
    if c%2==0: return True
    else: return False
    
def verifier7_1(t, s, c):
    if c%2==1: return True
    else: return False
    
def verifier8_0(t, s, c):
    count=0
    if t==1: count+=1
    if s==1: count+=1
    if c==1: count+=1
    if count==0: return True
    else: return False
    
def verifier8_1(t, s, c):
    count=0
    if t==1: count+=1
    if s==1: count+=1
    if c==1: count+=1
    if count==1: return True
    else: return False
    
def verifier8_2(t, s, c):
    count=0
    if t==1: count+=1
    if s==1: count+=1
    if c==1: count+=1
    if count==2: return True
    else: return False
    
def verifier9_0(t, s, c):
    count=0
    if t==3: count+=1
    if s==3: count+=1
    if c==3: count+=1
    if count==0: return True
    else: return False
    
def verifier9_1(t, s, c):
    count=0
    if t==3: count+=1
    if s==3: count+=1
    if c==3: count+=1
    if count==1: return True
    else: return False
    
def verifier9_2(t, s, c):
    count=0
    if t==3: count+=1
    if s==3: count+=1
    if c==3: count+=1
    if count==2: return True
    else: return False
    
def verifier10_0(t, s, c):
    count=0
    if t==4: count+=1
    if s==4: count+=1
    if c==4: count+=1
    if count==0: return True
    else: return False
    
def verifier10_1(t, s, c):
    count=0
    if t==4: count+=1
    if s==4: count+=1
    if c==4: count+=1
    if count==1: return True
    else: return False
    
def verifier10_2(t, s, c):
    count=0
    if t==4: count+=1
    if s==4: count+=1
    if c==4: count+=1
    if count==2: return True
    else: return False
    
def verifier11_0(t, s, c):
    if t<s: return True
    else: return False
    
def verifier11_1(t, s, c):
    if t==s: return True
    else: return False
    
def verifier11_2(t, s, c):
    if t>s: return True
    else: return False
    
def verifier12_0(t, s, c):
    if t<c: return True
    else: return False
    
def verifier12_1(t, s, c):
    if t==c: return True
    else: return False
    
def verifier12_2(t, s, c):
    if t>c: return True
    else: return False
    
def verifier13_0(t, s, c):
    if s<c: return True
    else: return False
    
def verifier13_1(t, s, c):
    if s==c: return True
    else: return False
    
def verifier13_2(t, s, c):
    if s>c: return True
    else: return False
    
def verifier14_0(t, s, c):
    if t < s and t < c: return True
    else: return False
    
def verifier14_1(t, s, c):
    if s<t and s<c: return True
    else: return False    

def verifier14_2(t, s, c):
    if c<t and c<s: return True
    else: return False
    
def verifier15_0(t, s, c):
    if t>s and t>c: return True
    else: return False
    
def verifier15_1(t, s, c):
    if s>t and s>c: return True
    else: return False    

def verifier15_2(t, s, c):
    if c>t and c>s: return True
    else: return False 
    
def verifier16_0(t, s, c):
    count=0
    if t%2==0: count+=1
    if s%2==0: count+=1
    if c%2==0: count+=1
    if count>=2: return True
    else: return False
    
def verifier16_1(t, s, c):
    count=0
    if t%2==0: count+=1
    if s%2==0: count+=1
    if c % 2 == 0: count += 1
    if count<2: return True
    else: return False
    
def verifier17_0(t, s, c):
    count=0
    if t%2==0: count+=1
    if s%2==0: count+=1
    if c%2==0: count+=1
    if count==0: return True
    else: return False
    
def verifier17_1(t, s, c):
    count=0
    if t%2==0: count+=1
    if s%2==0: count+=1
    if c%2==0: count+=1
    if count==1: return True
    else: return False
    
def verifier17_2(t, s, c):
    count=0
    if t%2==0: count+=1
    if s%2==0: count+=1
    if c%2==0: count+=1
    if count==2: return True
    else: return False
    
def verifier17_3(t, s, c):
    count=0
    if t%2==0: count+=1
    if s%2==0: count+=1
    if c%2==0: count+=1
    if count==3: return True
    else: return False

def verifier18_0(t, s, c):
    if (t+s+c)%2==0: return True
    else: return False
    
def verifier18_1(t, s, c):
    if (t+s+c)%2==1: return True
    else: return False
    
def verifier19_0(t, s, c):
    if (t+s)<6: return True
    else: return False
    
def verifier19_1(t, s, c):
    if (t+s)==6: return True
    else: return False

def verifier19_2(t, s, c):
    if (t+s)>6: return True
    else: return False
    
def verifier20_0(t, s, c):
    if t==s==c: return True
    else: return False
    
def verifier20_1(t, s, c):
    if t==s and s!=c: return True
    elif s==c and c!=t: return True
    elif c==t and t!=s: return True
    else: return False
    
def verifier20_2(t, s, c):
    if t!=s and s!=c and c!=t: return True
    else: return False
    
def verifier21_0(t, s, c):
    if t==s and s!=c: return True
    elif s==c and c!=t: return True
    elif c==t and t!=s: return True
    else: return False
    
def verifier21_1(t, s, c):
    if (t==s==c) or (t!=s and s!=c and c!=t): return True
    else: return False
    
def verifier22_0(t, s, c):
    if t<s<c: return True
    else: return False
    
def verifier22_1(t, s, c):
    if t>s>c: return True
    else: return False
    
def verifier22_2(t, s, c):
    if verifier22_0(t, s, c) or verifier22_1(t, s, c): return False
    else: return True
    
def verifier23_0(t, s, c):
    if (t+s+c)<6: return True
    else: return False
    
def verifier23_1(t, s, c):
    if (t+s+c)==6: return True
    else: return False
    
def verifier23_2(t, s, c):
    if (t+s+c)>6: return True
    else: return False
    
def verifier24_0(t, s, c):
    if t+1==s==c-1: return True
    else: return False
    
def verifier24_1(t, s, c):
    if t+1==s and s!=c-1: return True
    elif t+1!=s and s==c-1: return True
    else: return False
    
def verifier24_2(t, s, c):
    if verifier24_0(t, s, c) or verifier24_1(t, s, c): return False
    else: return True

def verifier25_0(t, s, c):
    if verifier25_1(t, s, c) or verifier25_2(t, s, c): return False
    else: return True
    
def verifier25_1(t, s, c):
    if t+1==s and s!=c-1: return True
    elif t+1!=s and s==c-1: return True
    elif t-1==s and s!=c+1: return True
    elif t-1!=s and s==c+1: return True
    else: return False
    
def verifier25_2(t, s, c):
    if t+1==s==c-1: return True
    elif t-1==s==c+1: return True
    else: return False
    
def verifier26_0(t, s, c):
    if t<3: return True
    else: return False
    
def verifier26_1(t, s, c):
    if s<3: return True
    else: return False
    
def verifier26_2(t, s, c):
    if c<3: return True
    else: return False
    
def verifier27_0(t, s, c):
    if t<4: return True
    else: return False
    
def verifier27_1(t, s, c):
    if s<4: return True
    else: return False
    
def verifier27_2(t, s, c):
    if c<4: return True
    else: return False
    
def verifier28_0(t, s, c):
    if t==1: return True
    else: return False
    
def verifier28_1(t, s, c):
    if s==1: return True
    else: return False
    
def verifier28_2(t, s, c):
    if c==1: return True
    else: return False

def verifier29_0(t, s, c):
    if t==3: return True
    else: return False
    
def verifier29_1(t, s, c):
    if s==3: return True
    else: return False
    
def verifier29_2(t, s, c):
    if c==3: return True
    else: return False
    
def verifier30_0(t, s, c):
    if t==4: return True
    else: return False
    
def verifier30_1(t, s, c):
    if s==4: return True
    else: return False
    
def verifier30_2(t, s, c):
    if c==4: return True
    else: return False
    
def verifier31_0(t, s, c):
    if t>1: return True
    else: return False
    
def verifier31_1(t, s, c):
    if s>1: return True
    else: return False
    
def verifier31_2(t, s, c):
    if c>1: return True
    else: return False
    
def verifier32_0(t, s, c):
    if t>3: return True
    else: return False
    
def verifier32_1(t, s, c):
    if s>3: return True
    else: return False
    
def verifier32_2(t, s, c):
    if c>3: return True
    else: return False
    
def verifier33_0(t, s, c):
    if t%2==0: return True
    else: return False

def verifier33_1(t, s, c):
    if s%2==0: return True
    else: return False
    
def verifier33_2(t, s, c):
    if c%2==0: return True
    else: return False
    
def verifier33_3(t, s, c):
    if t%2==1: return True
    else: return False
    
def verifier33_4(t, s, c):
    if s%2==1: return True
    else: return False
    
def verifier33_5(t, s, c):
    if c%2==1: return True
    else: return False
    
def verifier34_0(t, s, c):
    if t<=s and t<=c: return True
    else: return False
    
def verifier34_1(t, s, c):
    if s<=t and s<=c: return True
    else: return False    

def verifier34_2(t, s, c):
    if c<=t and c<=s: return True
    else: return False
    
def verifier35_0(t, s, c):
    if t>=s and t>=c: return True
    else: return False
    
def verifier35_1(t, s, c):
    if s>=t and s>=c: return True
    else: return False    

def verifier35_2(t, s, c):
    if c>=t and c>=s: return True
    else: return False 
    
def verifier36_0(t, s, c):
    if (t+s+c)%3==0: return True
    else: return False
    
def verifier36_1(t, s, c):
    if (t+s+c)%4==0: return True
    else: return False
    
def verifier36_2(t, s, c):
    if (t+s+c)%5==0: return True
    else: return False
    
def verifier37_0(t, s, c):
    if t+s==4: return True
    else: return False
    
def verifier37_1(t, s, c):
    if t+c==4: return True
    else: return False 
    
def verifier37_2(t, s, c):
    if c+s==4: return True
    else: return False

def verifier38_0(t, s, c):
    if t+s==6: return True
    else: return False
    
def verifier38_1(t, s, c):
    if t+c==6: return True
    else: return False 
    
def verifier38_2(t, s, c):
    if c+s==6: return True
    else: return False
    
def verifier39_0(t, s, c):
    if t==1: return True
    else: return False
    
def verifier39_1(t, s, c):
    if s==1: return True
    else: return False
    
def verifier39_2(t, s, c):
    if c==1: return True
    else: return False
        
def verifier39_3(t, s, c):
    if t>1: return True
    else: return False
    
def verifier39_4(t, s, c):
    if s>1: return True
    else: return False
    
def verifier39_5(t, s, c):
    if c>1: return True
    else: return False
    
def verifier40_0(t, s, c):
    if t<3: return True
    else: return False
    
def verifier40_1(t, s, c):
    if s<3: return True
    else: return False
        
def verifier40_2(t, s, c):
    if c<3: return True
    else: return False
        
def verifier40_3(t, s, c):
    if t==3: return True
    else: return False
    
def verifier40_4(t, s, c):
    if s==3: return True
    else: return False
        
def verifier40_5(t, s, c):
    if c==3: return True
    else: return False
        
def verifier40_6(t, s, c):
    if t>3: return True
    else: return False
    
def verifier40_7(t, s, c):
    if s>3: return True
    else: return False
        
def verifier40_8(t, s, c):
    if c>3: return True
    else: return False
    
def verifier41_0(t, s, c):
    if t<4: return True
    else: return False

def verifier41_1(t, s, c):
    if s<4: return True
    else: return False
        
def verifier41_2(t, s, c):
    if c<4: return True
    else: return False
        
def verifier41_3(t, s, c):
    if t==4: return True
    else: return False
    
def verifier41_4(t, s, c):
    if s==4: return True
    else: return False
        
def verifier41_5(t, s, c):
    if c==4: return True
    else: return False
        
def verifier41_6(t, s, c):
    if t>4: return True
    else: return False
    
def verifier41_7(t, s, c):
    if s>4: return True
    else: return False
        
def verifier41_8(t, s, c):
    if c>4: return True
    else: return False
    
def verifier42_0(t, s, c):
    if t < s and t < c: return True
    else: return False
    
def verifier42_1(t, s, c):
    if s<t and s<c: return True
    else: return False    

def verifier42_2(t, s, c):
    if c<t and c<s: return True
    else: return False
    
def verifier42_3(t, s, c):
    if t>s and t>c: return True
    else: return False
    
def verifier42_4(t, s, c):
    if s>t and s>c: return True
    else: return False    

def verifier42_5(t, s, c):
    if c>t and c>s: return True
    else: return False 
    
def verifier43_0(t, s, c):
    if t<s: return True
    else: return False
    
def verifier43_1(t, s, c):
    if t==s: return True
    else: return False
    
def verifier43_2(t, s, c):
    if t>s: return True
    else: return False
    
def verifier43_3(t, s, c):
    if t<c: return True
    else: return False
    
def verifier43_4(t, s, c):
    if t==c: return True
    else: return False
    
def verifier43_5(t, s, c):
    if t>c: return True
    else: return False

def verifier44_0(t, s, c):
    if s<t: return True
    else: return False
    
def verifier44_1(t, s, c):
    if s==t: return True
    else: return False
    
def verifier44_2(t, s, c):
    if s>t: return True
    else: return False
    
def verifier44_3(t, s, c):
    if s<c: return True
    else: return False
    
def verifier44_4(t, s, c):
    if s==c: return True
    else: return False
    
def verifier44_5(t, s, c):
    if s>c: return True
    else: return False
    
def verifier45_0(t, s, c):
    count=0
    if t==1: count+=1
    if s==1: count+=1
    if c==1: count+=1
    if count==0: return True
    else: return False
    
def verifier45_1(t, s, c):
    count=0
    if t==1: count+=1
    if s==1: count+=1
    if c==1: count+=1
    if count==1: return True
    else: return False
    
def verifier45_2(t, s, c):
    count=0
    if t==1: count+=1
    if s==1: count+=1
    if c==1: count+=1
    if count==2: return True
    else: return False
    
def verifier45_3(t, s, c):
    count=0
    if t==3: count+=1
    if s==3: count+=1
    if c==3: count+=1
    if count==0: return True
    else: return False
    
def verifier45_4(t, s, c):
    count=0
    if t==3: count+=1
    if s==3: count+=1
    if c==3: count+=1
    if count==1: return True
    else: return False
    
def verifier45_5(t, s, c):
    count=0
    if t==3: count+=1
    if s==3: count+=1
    if c==3: count+=1
    if count==2: return True
    else: return False
    
def verifier46_0(t, s, c):
    count=0
    if t==3: count+=1
    if s==3: count+=1
    if c==3: count+=1
    if count==0: return True
    else: return False
    
def verifier46_1(t, s, c):
    count=0
    if t==3: count+=1
    if s==3: count+=1
    if c==3: count+=1
    if count==1: return True
    else: return False
    
def verifier46_2(t, s, c):
    count=0
    if t==3: count+=1
    if s==3: count+=1
    if c==3: count+=1
    if count==2: return True
    else: return False    

def verifier46_3(t, s, c):
    count=0
    if t==4: count+=1
    if s==4: count+=1
    if c==4: count+=1
    if count==0: return True
    else: return False
    
def verifier46_4(t, s, c):
    count=0
    if t==4: count+=1
    if s==4: count+=1
    if c==4: count+=1
    if count==1: return True
    else: return False
    
def verifier46_5(t, s, c):
    count=0
    if t==4: count+=1
    if s==4: count+=1
    if c==4: count+=1
    if count==2: return True
    else: return False

def verifier47_0(t, s, c):
    count=0
    if t==1: count+=1
    if s==1: count+=1
    if c==1: count+=1
    if count==0: return True
    else: return False
    
def verifier47_1(t, s, c):
    count=0
    if t==1: count+=1
    if s==1: count+=1
    if c==1: count+=1
    if count==1: return True
    else: return False
    
def verifier47_2(t, s, c):
    count=0
    if t==1: count+=1
    if s==1: count+=1
    if c==1: count+=1
    if count==2: return True
    else: return False
    
def verifier47_3(t, s, c):
    count=0
    if t==4: count+=1
    if s==4: count+=1
    if c==4: count+=1
    if count==0: return True
    else: return False
    
def verifier47_4(t, s, c):
    count=0
    if t==4: count+=1
    if s==4: count+=1
    if c==4: count+=1
    if count==1: return True
    else: return False
    
def verifier47_5(t, s, c):
    count=0
    if t==4: count+=1
    if s==4: count+=1
    if c==4: count+=1
    if count==2: return True
    else: return False

def verifier48_0(t, s, c):
    if t<s: return True
    else: return False
    
def verifier48_1(t, s, c):
    if t==s: return True
    else: return False
    
def verifier48_2(t, s, c):
    if t>s: return True
    else: return False
    
def verifier48_3(t, s, c):
    if t<c: return True
    else: return False
    
def verifier48_4(t, s, c):
    if t==c: return True
    else: return False
    
def verifier48_5(t, s, c):
    if t>c: return True
    else: return False
    
def verifier48_6(t, s, c):
    if s<c: return True
    else: return False
    
def verifier48_7(t, s, c):
    if s==c: return True
    else: return False
    
def verifier48_8(t, s, c):
    if s>c: return True
    else: return False     
    
#endregion

verifier_list=[
    [verifier1_0, verifier1_1],
    [verifier2_0, verifier2_1, verifier2_2],
    [verifier3_0, verifier3_1, verifier3_2],
    [verifier4_0, verifier4_1, verifier4_2],
    [verifier5_0, verifier5_1],
    [verifier6_0, verifier6_1],
    [verifier7_0, verifier7_1],
    [verifier8_0, verifier8_1, verifier8_2],
    [verifier9_0, verifier9_1, verifier9_2],
    [verifier10_0, verifier10_1, verifier10_2],
    [verifier11_0, verifier11_1, verifier11_2],
    [verifier12_0, verifier12_1, verifier12_2],
    [verifier13_0, verifier13_1, verifier13_2],
    [verifier14_0, verifier14_1, verifier14_2],
    [verifier15_0, verifier15_1, verifier15_2],
    [verifier16_0, verifier16_1],
    [verifier17_0, verifier17_1, verifier17_2, verifier17_3],
    [verifier18_0, verifier18_1],
    [verifier19_0, verifier19_1, verifier19_2],
    [verifier20_0, verifier20_1, verifier20_2],
    [verifier21_0, verifier21_1],
    [verifier22_0, verifier22_1, verifier22_2],
    [verifier23_0, verifier23_1, verifier23_2],
    [verifier24_0, verifier24_1, verifier24_2],
    [verifier25_0, verifier25_1, verifier25_2],
    [verifier26_0, verifier26_1, verifier26_2],
    [verifier27_0, verifier27_1, verifier27_2],
    [verifier28_0, verifier28_1, verifier28_2],
    [verifier29_0, verifier29_1, verifier29_2],
    [verifier30_0, verifier30_1, verifier30_2],
    [verifier31_0, verifier31_1, verifier31_2],
    [verifier32_0, verifier32_1, verifier32_2],
    [verifier33_0, verifier33_1, verifier33_2, verifier33_3, verifier33_4, verifier33_5],
    [verifier34_0, verifier34_1, verifier34_2],
    [verifier35_0, verifier35_1, verifier35_2],
    [verifier36_0, verifier36_1, verifier36_2],
    [verifier37_0, verifier37_1, verifier37_2],
    [verifier38_0, verifier38_1, verifier38_2],
    [verifier39_0, verifier39_1, verifier39_2, verifier39_3, verifier39_4, verifier39_5],
    [verifier40_0, verifier40_1, verifier40_2, verifier40_3, verifier40_4, verifier40_5, verifier40_6, verifier40_7, verifier40_8],
    [verifier41_0, verifier41_1, verifier41_2, verifier41_3, verifier41_4, verifier41_5, verifier41_6, verifier41_7, verifier41_8],
    [verifier42_0, verifier42_1, verifier42_2, verifier42_3, verifier42_4, verifier42_5],
    [verifier43_0, verifier43_1, verifier43_2, verifier43_3, verifier43_4, verifier43_5],
    [verifier44_0, verifier44_1, verifier44_2, verifier44_3, verifier44_4, verifier44_5],
    [verifier45_0, verifier45_1, verifier45_2, verifier45_3, verifier45_4, verifier45_5],
    [verifier46_0, verifier46_1, verifier46_2, verifier46_3, verifier46_4, verifier46_5],
    [verifier47_0, verifier47_1, verifier47_2, verifier47_3, verifier47_4, verifier47_5],
    [verifier48_0, verifier48_1, verifier48_2, verifier48_3, verifier48_4, verifier48_5, verifier48_6, verifier48_7, verifier48_8]
]
    
    