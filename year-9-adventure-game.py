import array
import os
import time
from dataclasses import dataclass
from enum import Enum

cardinalDirections = ["NORTH", "SOUTH", "EAST", "WEST"]

def message(interval, msg):
    for i in range(len(msg)):
        print(msg[0:i+1])
        time.sleep(interval)
        clear()
    input(msg)


class player:
    def __init__(self, maxHP, defense):
        self.maxHP = maxHP
        self.HP = self.maxHP
        self.defense = defense
        self.currentLocation = "home"
        self.currentMsg = home.activeMsg[home.arrivalCnt]
        self.mapCollected = False

    def movement(self):
        task = input(self.currentMsg)



        if task in locations[self.currentLocation]["movement options"]:
            self.currentLocationData = locations[self.currentLocation]["movement options"][task]
            self.currentLocation = self.currentLocationData.locationString

            if self.currentLocationData.arrivalCnt >= self.currentLocationData.lastMsgNum:
                if self.currentLocationData.addedOption:
                    self.currentMsg = self.currentLocationData.activeMsg[self.currentLocationData.lastMsgNum]["message"]
                else:
                    self.currentMsg = self.currentLocationData.activeMsg[self.currentLocationData.lastMsgNum]

            elif self.currentLocationData.arrivalCnt >= self.currentLocationData.bridgeMsgNum:
                if self.currentLocationData.addedOption:
                    self.currentMsg = self.currentLocationData.activeMsg[self.currentLocationData.bridgeMsgNum]["message"]
                else:
                    self.currentMsg = self.currentLocationData.activeMsg[self.currentLocationData.bridgeMsgNum]

            else:
                if self.currentLocationData.addedOption:
                    self.currentMsg = self.currentLocationData.activeMsg[self.currentLocationData.arrivalCnt]["message"]
                else:
                    self.currentMsg = self.currentLocationData.activeMsg[self.currentLocationData.arrivalCnt]
                #locations[self.currentLocation]["extra options"][self.currentLocationData.activeMsg[self.currentLocationData.arrivalCnt][self.currentMsg]] = self.currentLocationData.activeMsg[self.currentLocationData.arrivalCnt][self.currentMsg]
            self.currentLocationData.arrivalCnt += 1



        elif task in locations[self.currentLocation]["extra options"]:
            locations[self.currentLocation]["extra options"][task](self)
           



        elif self.currentLocationData.addedOption:
            if self.currentLocationData.arrivalCnt >= self.currentLocationData.lastMsgNum:
                msgNum = self.currentLocationData.lastMsgNum

            elif self.currentLocationData.arrivalCnt >= self.currentLocationData.bridgeMsgNum:
                msgNum = self.currentLocationData.bridgeMsgNum

            else:
                msgNum = self.currentLocationData.arrivalCnt

            if task in self.currentLocationData.activeMsg[msgNum]["added option"]:
                self.currentLocationData.activeMsg[msgNum]["added option"][task](self)

            else:
                print("unrecogonised command")



        else:
            print("unrecognised command")

    def mapPickup(self):
        self.mapCollected = True

    def killSelf(self):
        self.HP = 0

@dataclass
class locationData:
    locationString: str
    arrivalCnt: int
    activeMsg: dict
    bridgeMsgNum: int
    lastMsgNum: int
    addedOption: bool
       
home = locationData("home", 0, {0: "You begin your adventure at home, there is a map chilling [pick up map], where would you like to go? NORTH, SOUTH, EAST or WEST? Or you could [enter basement]", 1: "You are back at home, where would you like to go? NORTH, SOUTH, EAST or WEST?"}, 0, 1, False)

highway = locationData("highway", 0, {0: "you have arrived at the local highway", 1: "you have come back to the local highway"}, 0, 1, False)

road = locationData("road", 0, {0: "you have arrived at road", 1: "you have come back to the road"}, 0, 1, False)

basement = locationData("basement", 0, {0: {"message": "there is literally nothing here, you should [go back]"}, 1: {"message": "why did you come back???? [go back]"}, 3: {"message": "genuinely kill yourself. [kill yourself] or [go back]", "added option": {"kill yourself": player.killSelf}}}, 1, 3, True)




locations = {"home": {"movement options": {"NORTH": road, "SOUTH": highway, "enter basement": basement}, "extra options": {"pick up map": player.mapPickup}},

             "highway": {"movement options": {"NORTH": home}, "extra options": {None}},

             "road": {"movement options": {"SOUTH": home}, "extra options": {None}},

             "basement": {"movement options": {"go back": home}, "extra options": {None}
                        }
             }
     

def clear():
    os.system('cls')


mainPlayer = player(100, 0)
       


message(0.0004, "hello! welcome to my adventure game! press [ENTER] to continue")
message(0.0004, "i hope you have a great time!")
while mainPlayer.HP > 0:
    mainPlayer.movement()
    