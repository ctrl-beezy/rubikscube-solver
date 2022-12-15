#include "cubeparser.hpp"
#include <Arduino.h>

movement* cubeparser(movement* lastmovement, String inputString){ // loop over inputString and write movements to array
    int index = 0;
    String substring;
    movement lastmove = *lastmovement;
    movement move;
    do{
        substring = inputString.substring(index, inputString.indexOf(' ', index)); //create substring with one movement
        Serial.println(substring);
        move = movementdecode(substring); // decode single movement
        if(move.angleDegrees == lastmove.angleDegrees && move.direction == lastmove.direction){
            if (checkOpposite(move.axes, lastmove.axes) != none){
                lastmovement->axes = checkOpposite(move.axes,lastmove.axes);
            }

        }
        else if ((lastmovement+1)){ // check if array is full
            lastmovement += 1; //increment array
            *lastmovement = move; //put new move at end of array
            lastmove = move; // save move for next iteration
        }
        else { 
            return lastmovement; // return from function if array is full
        }
            index = inputString.indexOf(' ',index)+1;
        } while((index-1) != -1); // exit loop if String is over
    return lastmovement;
}

movement movementdecode(String movestring){
    movement mymovement;
    switch (movestring[0]){
        case 'F' :  mymovement.axes = front;
        break;
        case 'B' :  mymovement.axes = back;
        break;
        case 'U' :  mymovement.axes = up;
        break;
        case 'D' : mymovement.axes = down;
        break;
        case 'L' : mymovement.axes = left;
        break;
        case 'R' : mymovement.axes = right;
        break;
        default : mymovement.axes = none;
    }
    if (movestring.length() < 2){
        mymovement.angleDegrees = 90;
        mymovement.direction = cw;
        return mymovement;
    }
    if (movestring[1] == '\''){
        mymovement.angleDegrees = 90;
        mymovement.direction = ccw;
        return mymovement;
    }
    if ('0' <= movestring[1] && movestring[1] <= '9'){
        mymovement.angleDegrees = 90 * uint16_t(movestring[1] - '0');
        mymovement.direction = cw;
        return mymovement;
    }
    return mymovement;
}

enum motor checkOpposite(enum motor axes1, enum motor axes2){
    if ((axes1 == front && axes2 == back) || (axes1 == back && axes2 == front))
        return frontBack;
    else if((axes1 == up && axes2 == down) || (axes1 == down && axes2 == up))
        return upDown;
    else if((axes1 == left && axes2 == right) || (axes1 == right && axes2 == left))
        return leftRight;
    else 
        return none;
  
}
