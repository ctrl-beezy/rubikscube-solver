#ifndef STEPCONTR_HPP
#define STEPCONTR_HPP

#include <Arduino.h>
#include <string.h>

void Pin_Reset();
void Schritt(int Zeit);
void Fahren();
void Schritt_vor();
void Schritt_rueck();
void leseSchritt(String movestring);
#endif