import random
import time


class goalBasedAgent():
    def __init__(self):
        # goal based agent implenetation
        # taking input the dimensions of our env
        self.rows = int(input("No of rows of env "))
        self.cols = int(input("No of cols of env "))
        # creating a 2d array as our envirnoment
        self.env = [[0 for __ in range(self.cols)] for _ in range(self.rows)]
        self.dest = random.randint(
            0, self.rows-1), random.randint(0, self.cols-1)
        
          # add the happiness factor to the agent
        self.happy = self.rows * self.cols
        # initializing the happiness factor with the total number of grids
        self.degraders = []
        self.idxs = []
        for i in range(random.randint(1, self.cols)):
            # there can be atmost n numbers of degraders where n represents the number of number of cols
            # each degrader degrades the happiness factor by a value between 1 to number of rows
            self.degraders.append(random.randint(1, self.rows))
            self.idxs.append(((random.randint(0, self.rows - 1)),(random.randint(0, self.cols - 1))))
        # print("idxs ", self.idxs)
        # print("dgraders ", self.degraders)
        for idx,value in enumerate(self.degraders):
            self.env[self.idxs[idx][0]][self.idxs[idx][1]] = value;


        self.pos = [0, 0]
        self.env[self.dest[0]][self.dest[1]] = 'd'
        self.env = [
            [0,1,2,3,'d']
            ]
        self.printEnv()

    def printEnv(self):
        self.env[self.pos[0]][self.pos[1]] = 'a'
        print("Env : \n")
        for i in self.env:
            for j in i:
                print(j,end=" ")
            print("\n")
        self.env[self.pos[0]][self.pos[1]] = 0

    def cost(self, next):
        # calculating cost based on the distance from destination point
        if (next[0] < 0 or next[0] > self.rows-1 or next[1] < 0 or next[1] > self.cols):
            return 10000
        return ((self.dest[0]-next[0])**2 + (self.dest[1] - next[1])**2) ** 0.5

    def simulate(self):

        while (self.pos[0] != self.dest[0] or self.pos[1] != self.dest[1]):
            # up down left right
            distArr = [
                self.cost([self.pos[0], self.pos[1]+1]),
                self.cost([self.pos[0], self.pos[1]-1]),
                self.cost([self.pos[0]+1, self.pos[1]]),
                self.cost([self.pos[0]-1, self.pos[1]]),
            ]
            posArr = [
                [self.pos[0], self.pos[1]+1],
                [self.pos[0], self.pos[1]-1],
                [self.pos[0]+1, self.pos[1]],
                [self.pos[0]-1, self.pos[1]],
            ]
            self.decide(distArr,posArr)
            self.printEnv()
        print("Reaced Destination")


    def decide(self, distArr, posArr):
        min_ = min(distArr)
        index = (distArr.index(min_))
        if(self.env[posArr[index][0]][posArr[index][1]] != 'd' and self.env[posArr[index][0]][posArr[index][1]] != 'v' ):
            self.happy -= self.env[posArr[index][0]][posArr[index][1]]
        self.pos = posArr[index]
        return True
    def all_min(self,lst):
        if not lst:
            return []  # Return an empty list if the input list is empty

        min_value = min(lst)
        indices = [index for index, value in enumerate(lst) if value == min_value]
        return indices

class utilityBasedAgent(goalBasedAgent):
    random.seed(time.time())

    def __init__(self):
        super().__init__()
      
    def decide(self, distArr, posArr):
        degraderPresence = [
                            self.checkDegrader((self.pos[0], self.pos[1]+1)),
                            self.checkDegrader((self.pos[0], self.pos[1]-1)),
                            self.checkDegrader((self.pos[0]+1, self.pos[1])),
                            self.checkDegrader((self.pos[0]-1, self.pos[1])),
                           ]

        stuck = True
        # print("dg presn ",degraderPresence)

        for i in degraderPresence:
            stuck = stuck and i ==9999
        if(stuck):
            print("Sorry I am stuck")
            goalBasedAgent.simulate(self);
            exit()



        # min_ = 
        max_happy_idx =self.all_min(degraderPresence);
        # for i in min_:
        #     max_happy_idx.append(degraderPresence.index(i))

        distDict = {index: value for index, value in enumerate(distArr)}
        sorted_dist = dict(sorted(distDict.items(), key=lambda item: item[1]))
        # print("sorted distance ",sorted_dist)
        # print("postion ",posArr)
        # print("current pos ",self.pos)

        for index in sorted_dist:
            if(index in max_happy_idx):
                self.env[self.pos[0]][self.pos[1]] = 'v';
                if(self.env[posArr[index][0]][posArr[index][1]] != 'd' and self.env[posArr[index][0]][posArr[index][1]] != 'v' ):
                    self.happy -= self.env[posArr[index][0]][posArr[index][1]]
                self.pos = posArr[index]
                break

            else:
                pass     
        return True


    def checkDegrader(self,next):
        # should return wheather a degrader is present or not
        k =0 
        if (next[0] < 0 or next[0] > self.rows-1 or next[1] < 0 or next[1] > self.cols-1): 
            # that means the value is outside matrix
            return 9999;
        elif(self.env[next[0]][next[1]] == 'v'):
            return 9999;
        elif(self.env[next[0]][next[1]]!= 'd'):
            k = self.env[next[0]][next[1]]
        return k

    def simulate(self):
        super().simulate()
        print("Happiness Level ",self.happy, "/", self.rows*self.cols)

agent = utilityBasedAgent()
agent.simulate()

