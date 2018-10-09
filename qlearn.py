

import random

class QLearn:
  masterQ={}
  historyA=[]
  historyS=[]
  def __init__(self,epsilon=0.1,alpha=0.2,lambd=0.5):
    self.q={}#QLearn.masterQ
    self.oldstate=None
    self.actions=None

    self.epsilon=epsilon
    self.alpha=alpha
    self.lambd=lambd

  def setActions(self,actions):
    self.actions=actions

  def getQ(self,state,action):
    return self.q.get((state,action),0.0)
  def setQ(self,state,action,value):
    self.q[(state,action)]=value

  def do(self,state):
    self.oldstate=state
    # if random.random()<self.epsilon:
    #   action=random.choice(self.actions)
    # else:
    q=[self.getQ(state,a) for a in self.actions]
    i=q.index(max(q))
    action=self.actions[i]
    self.oldaction=action
    self.historyA.append(action)
    self.historyS.append(state)
    return action

  def learn(self,newstate,reward):
    if self.oldstate==None: return

    oldq=self.getQ(self.oldstate,self.oldaction)
    maxqnew=max([self.getQ(newstate,a) for a in self.actions])
    self.setQ(self.oldstate,self.oldaction,oldq+self.alpha*(reward+self.lambd*maxqnew-oldq))
