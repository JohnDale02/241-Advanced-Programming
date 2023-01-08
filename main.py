import numpy
import numpy as np  # used for arrays
from matplotlib import pyplot as plt   # importing for plotting
import random  # importing for randomizing weights
import seaborn as sns
import pandas as pd
class machineLearning:
    def __init__(self, records=None,size=0,weight=None,chngW=None,prices=None,MSE=0,impMSE=None, iter=None,init=None):
        self.records = records  # holding the data for file
        self.size = size  # holding the size of file (# of records)
        self.weight = weight  # holding a list of weights
        self.MSE = MSE  # holding list of MSE values for all records
        self.chngW = chngW  # holding list of calculated gradients
        self.prices = prices  # holding list of actual house prices
        self.impMSE = impMSE  # holding list of all updated MSE after changing weight (for plotting)
        self.iteration = iter # holding numbers (1- iteration #) for plotting
        self.weight1 = init  # initial weight, used for starting learning rates with the same weights

    def readFile(self, filename: str) -> None:  # function to store graph as network class attribute
        file = open(filename, 'r').readlines()[1:] # read all lines except titles
        size = 0
        datalist = []
        priceList = []
        for line in file:   # for each line
            size = 1+size    # size counter to get # of lines
            feature = [x.strip() for x in line.split(",")]  # strip and spliting each line
            LotFrontage = float(feature[1])    # setting temp features from line
            LotArea = float(feature[2])
            OverallQual = float(feature[3])
            OverallCond = float(feature[4])
            YearBuilt = float(feature[5])
            BsmtFinSF1 = float(feature[6])
            BsmtUnfSF = float(feature[7])
            TotalBsmtSF = float(feature[8])
            firstFlrSF = float(feature[9])
            secondFlrSF = float(feature[10])
            LowQualFinSF = float(feature[11])
            GrLivArea = float(feature[12])
            BsmtFullBath = float(feature[13])
            FullBath = float(feature[14])
            HalfBath = float(feature[15])
            BedroomAbvGr = float(feature[16])
            KitchenAbvGr = float(feature[17])
            TotRmsAbvGrd = float(feature[18])
            Fireplaces = float(feature[19])
            GarageCars = float(feature[20])
            GarageArea = float(feature[21])
            WoodDeckSF = float(feature[22])
            OpenPorchSF = float(feature[23])
            EnclosedPorch = float(feature[24])
            MoSold = float(feature[25])
            Price = float(feature[26])   # appending all temp (except price) features from line as a list into datalist
            datalist.append([LotFrontage,LotArea,OverallQual,OverallCond,YearBuilt,BsmtFinSF1,BsmtUnfSF,\
                             TotalBsmtSF,firstFlrSF,secondFlrSF,LowQualFinSF,GrLivArea,BsmtFullBath,FullBath,\
                             HalfBath,BedroomAbvGr,KitchenAbvGr,TotRmsAbvGrd,Fireplaces,GarageCars,GarageArea,\
                             WoodDeckSF,OpenPorchSF,EnclosedPorch,MoSold])
            priceList.append(Price)    # appending price into pricelist
        weightlist = []
        for i in range(0,25):
            weightlist.append(random.randrange(1,10))  # creating 25 random weights between 1-10
        self.size = size  #  number of datapoints
        self.records = np.array(datalist)   # holding all features data for all lines as array
        self.weight = np.array(weightlist)   # holding all current weights
        self.weight1 = self.weight  # keeping the first weight list, for comparing learning rates
        self.prices = np.array(priceList)  # array of all real prices
        return

    def pred(self):   # function to predict price given current weights
        predPrices = []
        for i in self.records:   # for each line
            predPrice = sum(np.multiply(self.weight,i[0:25]))  # sum (weights x feature values )
            predPrices.append(predPrice)  # append this to out list that holds predicted house prices
        self.pPrices = predPrices  # predicted prices list


    def loss(self):  # function to calculate MSE
        count = 0
        totalLoss = 0
        for i in self.pPrices:  # for each predicted house price
            loss = (i-prices[count])**2   # MSE formula
            count = count+1
            totalLoss = totalLoss + loss  # MSE formula
        self.MSE = totalLoss/self.size    # MSE formula, setting MSE total to self.MSE
        return

    def gradient(self):  # function for calculating gradient for changing weights
        x = np.array(self.records)   # array of all data
        x = x.transpose()   # transposing the array, x
        change = []
        for i in range(len(self.pPrices)):
            change.append(self.pPrices[i]-prices[i]) # appending difference in price to list
        change = np.array(change)   # creating array for multiplication
        chngMSE = (2/self.size)* (np.dot(x,change))  # GRADIENT FORMULA
        chngMSE = chngMSE.tolist()   # creating list to better organize
        newW = []
        for i in chngMSE:
            newW.append(i)
        self.chngW = newW  # final list of gradients for changing weights
        return

    def update(self,alpha):  # function for updating weights
        updateW = []
        for i in range(len(self.weight)):  # for 25 iterations
            updateW.append(self.weight[i] - alpha*self.chngW[i])   # newW = currentW - alpha * gradient
        self.weight = np.array(updateW)  # after changing weights, update weight attribute

    def train(self,learningRate):  # function to improve the MSE
        self.weight = self.weight1  # set weight to initial weight (useful for 2nd or 3rd run)
        count = 0
        iteration = []
        itMSE = []
        while count != 500:  # for 500 iterations
            self.pred()   # get the predicted house price
            self.loss()   # calculate the MSE with that predicted price
            itMSE.append(self.MSE)   # add that MSE to a list
            iteration.append(count)  # add the iteration to a list
            self.gradient()         # calculate the gradient for changing weights
            self.update(learningRate)  # update the weights
            count = count +1   # increase count
        self.iteration = iteration  # once done, set iteration attribute to list of iterations
        self.impMSE = itMSE         # once done, set impMSE attribute to list of MSE's
        print("MSE after",iteration[-1]+1,"iterations",itMSE[-1])  # line to give final MSE printout


if __name__ == "__main__":

    MLTrain = machineLearning()
    MLTrain.readFile("train.csv")
# Question 2: Analyzing data
    # - number of records
    print("Number of Records: ",MLTrain.size)

    # - mean price
    prices = MLTrain.prices
    tot = sum(prices)
    size = MLTrain.size
    mean = float(tot/size)
    print("Mean Price: ",mean)

    # - min price
    print("Min House Price: ",min(prices))

    # - max price
    max = max(prices)
    print("Max House Price: ",max)

    # - sdev
    errors = []
    for i in prices:
        error = (i - mean)**2
        errors.append(float(error))
    TotError = sum(errors)
    SDev = TotError/size
    print("Standard Deviation: ",SDev)

# Question 3: Histogram of Sales Prices
    a = np.array(prices)
    bin = [max/6,2*max/6,3*max/6,4*max/6,5*max/6,max]
    plt.hist(a, bins=bin)
    plt.title("Histogram of Sales Prices")
    plt.show()

# Question 4: Comparing 4 features
    GrLivArea = []
    BedroomAbvGr = []
    TotalBsmtSF = []
    FullBath = []   # creating lists with feature values for all 818 datapoints
    for i in MLTrain.records:
        GrLivArea.append(i[11])
        BedroomAbvGr.append(i[15])
        TotalBsmtSF.append(i[7])
        FullBath.append((i[15]))
    data = {'GrLivArea': GrLivArea, 'BedroomAbvGr': BedroomAbvGr, 'TotalBsmtSF': TotalBsmtSF,'FullBath': FullBath}
    pairs = pd.DataFrame(data)  # creating dataframe for pairplot
    sns.pairplot(pairs)  # pairplot
    plt.show()

#--------------Part 2: ------------------------

    MLTrain.train(10e-9)
    plt.title("MSE vs Iterations")
    plt.xlabel("Iterations")
    plt.ylabel("MSE")
    plt.plot(MLTrain.iteration, MLTrain.impMSE, color="red",label="MSE w/ a=10^-9")

    MLTrain.train(10e-8)
    plt.plot(MLTrain.iteration,MLTrain.impMSE, color="blue",label="MSE w/ a=10^-8")
    plt.legend()
    plt.show()