import threading
class Menu:
    def __init__(self,featureList):
        self.featureList=featureList

    def start(self):
        threadPointer=list()
        for x in self.featureList:
            if x.state:
                threadPointer.append(threading.Thread(target=x.arrFunc))
                threadPointer[len(threadPointer)-1].start()
                print("Start {}".format(x.label))
            else:
                threadPointer.append(None)

        return threadPointer

    def showFeatures(self):
        print("-" * 50)
        print("{:<10}{:<20}{}".format("No.","Features",'Toggle (ON / OFF)'))
        print("-" * 50)
        for i,x in enumerate(self.featureList):
            print("{:<10}{:<20}{}".format(i+1,x.label,'ON' if x.state else 'OFF'))
        print("-" * 50)
        print("To Start Cheat: {:>24}".format("Type start"))
        print("For Instructions: {:>21}".format("Type help"))

    def displayMenu(self):
        while True:
            self.showFeatures()
            choice=input("\n\nEnter input:")
            try:
                if choice.lower() == "start":
                    self.start()
                    break

                elif choice.lower()== "help":
                    pass

                elif int(choice)-1<len(self.featureList) and int(choice)-1>=0:
                    self.featureList[int(choice)-1].toggle()
                    print("Toggle {}\n".format('ON' if self.featureList[int(choice)-1].state else 'OFF'))

                else:
                    print("Index not Found. Enter a valid Index\n")

            except(ValueError):
                print("Enter the index number in the list to toggle ON / OFF.\n")
