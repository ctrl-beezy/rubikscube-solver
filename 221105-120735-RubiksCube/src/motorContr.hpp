#ifndef MOTORONTR_HPP
#define MOTORCONTR_HPP

#include "cubeparser.hpp"
#include <Arduino.h>
#include <string.h>

void Pin_Reset();
void Schritt(int Zeit);
void Fahren();
void Schritt_vor();
void Schritt_rueck();
void leseSchritt(String movestring);
void runMotors(movement* movementList, movement* lastMovement);
#endif