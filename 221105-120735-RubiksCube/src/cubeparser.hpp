#ifndef CUBEPARSER_HPP
#define CUBEPARSER_HPP
#include <Arduino.h>

enum motor {
    front = 1,
    back = 2,
    left = 3,
    right = 4,
    up = 5,
    down = 6,
    frontBack = 7,
    leftRight = 8,
    upDown = 9,
    none = 0
};
enum dir {
    cw = 1,
    ccw = 0
};

struct movement {
    uint8_t angleDegrees = 0;
    enum motor axes = none;
    enum dir direction = cw;
};

movement* cubeparser (movement* lastmovement, String inputString);
movement movementdecode(String movestring);
enum motor checkOpposite(enum motor axes1, enum motor axes2);

#endif
