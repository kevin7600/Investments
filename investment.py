import csv
import math

def cleanText(txt):
    return ' '.join(txt.split())

def CreateList():
    filename="sp-500-historical-annual-returns.csv"
    # filename="UILSourceAnnual.csv"
    csv_file = csv.reader(open(filename), delimiter=",")
    readValues=False
    #get the start of values, and create dictionary
    myList=[]
    for row in csv_file:
        for i in range(len(row)):
            row[i]=cleanText(row[i])

        if readValues==False:
            if row==['date','value']:    
                readValues=True
        else:
            year=int(row[0][0:4])#first 4 characters are year
            interstRate=float(row[1])
            myList.append([year,interstRate])
    return myList

def GetAverageAnnualReturns(startYear, endYear, myData):
    state=0#0=find start year index, 1=do running calculations to find average annual interst
    countNumYears=0
    cumulativeInterst=1 #
    addativeCululativeInterest=0
    UILCumulativeInterest=1
    UILAddativeCululativeInterst=0
    UILMinInterest=.75
    UILMaxInterest=13.75
    for i in range(len(myData)):
        if state==0:
            if myData[i][0]==startYear:#found start year. Do fencepost calculations
                state=1
                cumulativeInterst *= 1+(myData[i][1]*.01)
                addativeCululativeInterest += myData[i][1]*.01
                
                #UIL calculations:
                curYearInterestPercent=myData[i][1]
                if myData[i][1]<UILMinInterest:
                    curYearInterestPercent=UILMinInterest
                elif myData[i][1]>UILMaxInterest:
                    curYearInterestPercent=UILMaxInterest
                UILCumulativeInterest *= 1+(curYearInterestPercent*.01)
                UILAddativeCululativeInterst += curYearInterestPercent*.01                

                countNumYears += 1
        else:#state==1
            if startYear + countNumYears != myData[i][0]:
                print("ERROR, data years are out of order")
                quit(-1)
            
            if myData[i][0]<= endYear:#calculate
                cumulativeInterst *= 1+(myData[i][1]*.01)
                addativeCululativeInterest += myData[i][1]*.01
                
                #UIL calculations:
                curYearInterestPercent=myData[i][1]
                if myData[i][1]<.75:
                    curYearInterestPercent=.75
                elif myData[i][1]>13.75:
                    curYearInterestPercent=13.75
                UILCumulativeInterest *= 1+(curYearInterestPercent*.01)
                UILAddativeCululativeInterst += curYearInterestPercent*.01                

                countNumYears += 1
            else:#we are past endYear, end the calculations
                break
    annualAverageReturn= ((cumulativeInterst**(1/float(countNumYears))) - 1.0)* 100
    annualAverageReturnAddative= (addativeCululativeInterest / float(countNumYears)) * 100
    UILAnnualAverageReturn=((UILCumulativeInterest**(1/float(countNumYears))) - 1.0) * 100
    UILAnnualAverageReturnAddative= (UILAddativeCululativeInterst / float(countNumYears)) * 100
    return annualAverageReturn, annualAverageReturnAddative, UILAnnualAverageReturn, UILAnnualAverageReturnAddative


def Help():
    print("")
    print("________________________________________________________________________________________________________________________")
    print("                             HELP                              ")
    print("This program calculates the annual Effective Interest and Average Interest for the S&P 500 between the years 1928 and 2019.")
    print("It compares IUL and Standard Index funds side by side")
    print("Effective Interest = The equivalent annual interest rate that you would get if you were invest in a hypothetical market with X% interest rate for Y years")
    print("Average Interest   = The average of the interest rates. Note that this figure is misleading")
    print("________________________________________________________________________________________________________________________")
    print("")
    print("")

def Loop(myData):
    myInput=""
    while True:
        myInput=input("Enter starting year (e.g. \"1950\"): ")
        if myInput=="quit":
            break
        elif myInput=="help":
            Help()
            continue
        startYear=int(myInput)
        myInput=input("Enter ending year (e.g. \"2019\"): ")
        if myInput=="quit":
            break
        elif myInput=="help":
            Help()
            continue
        endYear=int(myInput)
        averageAnnualReturns=GetAverageAnnualReturns(startYear,endYear,myData)
        a=round(averageAnnualReturns[0], 2)
        b=round(averageAnnualReturns[1], 2)
        c=round(averageAnnualReturns[2], 2)
        d=round(averageAnnualReturns[3], 2)
        print("")
        print("________________________________________________________________________________________________________________________")
        print("           AVERAGE ANNUAL INTEREST FROM "+str(startYear)+" - "+str(endYear))
        print()
        print("                    Index Fund    UIL Index")
        print("                   __________________________")
        print("Effective Interest |  {0:>5.2f}%    | {1:>6.2f}%    |".format(a,c))
        print("Average Interest   |  {0:>5.2f}%    | {1:>6.2f}%    |".format(b,d))
        print("                   --------------------------")
        print("________________________________________________________________________________________________________________________")
        print("")
        print("")

def main():
    print("This program calculates the average annual interst rate of investments in a given range inclusive.")
    myData=CreateList()
    print("It currently has the historical data of the S&P 500 from "+str(myData[0][0])+" to "+str(myData[len(myData)-1][0])+".")
    print("To quit, enter \"quit\"")
    print("________________________________________________________________________________________________________________________")
    Loop(myData)

if __name__=="__main__":
    main()