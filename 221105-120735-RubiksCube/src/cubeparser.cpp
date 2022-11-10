#include "cubeparser.hpp"

void cubeparser(movement* lastmovement, String inputString){ // loop over inputString and write movements to array
    int index = 0;
    String substring;
    movement lastmove;
    movement move;
    do{
        substring = inputString.substring(index, inputString.indexOf(' ', index)); //create substring with one movement
        move = movementdecode(substring); // decode single movement
        if ((lastmovement+1)) // check if array is full
        {
            lastmovement += 1; //increment array
            *(lastmovement) = move; //put new move at end of array
            lastmove = move; // save move for next iteration
        }
        if(move.angleDegrees == lastmove.angleDegrees && move.direction == lastmove.direction){
                
        }
        else 
            return; // return from function if array is full
        } while((index-1) != -1); // exit loop if String is over
    return;
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
    if ('0' <= movestring[1] <= '9'){
        mymovement.angleDegrees = 90 * uint16_t(movestring[1] - '0');
        mymovement.direction = cw;
        return mymovement;
    }
    return mymovement;
}