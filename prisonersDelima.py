import random
import qlearn
import matplotlib.pyplot as plt

qEpsilon=0.1			# Q-Learning exploration rate
qLambda=0.95			# Q-Learning future discount rate
qAlpha=0.2				# Q-Learning learning rate

def Cumulative(lists):
    cu_list = []
    length = len(lists)
    cu_list = [sum(lists[0:x + 1]) for x in range(0, length)]
    return cu_list

def __tit_for_tat(history):
    if(len(history)>0):
        return(history[-1][1])
    else:
        return 'd'

def _randomChoice(history):
    return(random.choice(('c','d')))
    
def c_10_per(history): #static function for testing
    #print("history",history)
    if len(history) == 0:        
        return 'd'    
    if len(history) > 0:
        check = [x[1] for x in history]   
        #print("check",check)     
        if 'c' in check:  
            # print("c1")  
            number = random.randint(1,11)
            if number == 10 :
                    return 'd'
            else:
                    return 'c'
        else:
            return 'd'


def divye_strategy(history):
    #print("in divye")
    check = [x[1] for x in history]
    if len(check)>0:
        if check.count('c')/len(check) >= 0.25:
            return('d')
        else:
            return('c')
    else:
        return('d')

def shubham_strategy(history):
	if len(history) > 0:
		if history[-1]==('c','c') or history[-1]==('d','c'):
			return(history[-1][0])
		else:
			if history[-1][1]=='c':
				return 'd'
			else:
				return 'c'
	else:
		return 'c'
        
#def shrinath_statergy(hist){					#My stratergy
#	move <- NA
#	if len(hist) == 0:
#	        return('c') 
#	else:
#        check = [x[1] for x in history]
#        check.count('c')/len(check) >= 0.35
#        n_hist <- mean(hist)
#	     if (mean_hist >=0 && mean_hist<=0.25){
#	                move <- 0
#	         }else{
#	                move <-1
#	         }
#	 
#	 return(move)
#}  
    

def __always_defect(history):
    #print('c1')
    return('d')

stategyFunc={
        0 :__tit_for_tat, #priyanka statergy
        1:_randomChoice, 
        2:c_10_per, #shrinaths statergy
        3:divye_strategy,  #divye steatergy
        4:__always_defect, #gauvrav statergy
        5:shubham_strategy #shubhams statergy
    }
class prisonersDelima:
    p_map={('c','c'):(2,2),
           ('c','d'):(0,5),
           ('d','c'):(5,0),
           ('d','d'):(0,0)}
    def __init__(self,internalStatergy,_n_plyer=2,n_iter=1111):
        #self.plr_func = _plr_func
        self.n_iter = n_iter
        self.history=[]
        #print(internalStatergy)
        self.internalStatergy=stategyFunc[internalStatergy]

    def set_plr_func(self,plrFunct):
        self.plr_func = plrFunct

    def one_round(self):
        #print(self.internalStatergy)
        #op=self.internalStatergy(self.history)
        self.history.append((self.internalStatergy(self.history),self.plr_func(self.history)))
        return(self.history[-1])
    def n_round(self):
        return([self.one_round() for _ in range(self.n_iter)])
    
    def evaluate_points(history):
        # print("bla bla")
        # print("history",history)
        vals=[prisonersDelima.p_map[x] for x in history]
        lst=[*zip(*vals)]
        return([sum(x) for x in lst])
    def plot_scoreMap(self):
        vals=[prisonersDelima.p_map[x] for x in self.history]
        lst=[*zip(*vals)]
        p1=Cumulative(lst[0])
        aiR = Cumulative(lst[1])
        plt.plot(aiR,'r',label="Q_ai")
        plt.plot(p1,'b',label="pl_1")
        plt.xlabel("iterations")
        plt.ylabel("score along itretions")
        plt.legend()
        plt.show()
        
        


if __name__=="__main__":
    pd=prisonersDelima(5)
    ai=qlearn.QLearn(epsilon=qEpsilon,lambd=qLambda,alpha=qAlpha)
    ai.setActions(['c','d'])
    def take_action(history):
        #print("in Q")
        if len(history) > 0: 
            pnts=prisonersDelima.evaluate_points(history)
            reward = pnts[1] -pnts[0]
            state=history[-1]
            ai.learn(state,reward)
            choice=ai.do(state)
            return(choice)
        else:
            return('c')
    
    pd.set_plr_func(take_action)
    roundStates=pd.n_round()
    #print(roundStates)
    finalVals=prisonersDelima.evaluate_points(roundStates)
    pd.plot_scoreMap()
    #print(finalVals)
    #print(finalVals)
