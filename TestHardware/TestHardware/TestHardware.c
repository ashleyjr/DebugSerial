//	Author: Ashley J. Robinson
//
//	Sine wave generator over uart

#define F_CPU 12000000UL

#define BAUD 9600
#define BAUD 115200

#include <avr/io.h>
#include <util/delay.h>
#include <util/setbaud.h>

#include "Waveforms.h"
	
void init_uart(void) { 
	UBRR0H = UBRRH_VALUE; UBRR0L = UBRRL_VALUE;
	UCSR0A = USE_2X << U2X0;
	UCSR0B = _BV(RXEN0) | _BV(TXEN0);
	UCSR0C = _BV(UCSZ00) | _BV(UCSZ01); 
}

void tx(uint8_t b) { 
	while(!(UCSR0A & _BV(UDRE0))); UDR0 = b;
}

int main(void){
	uint16_t i;
	init_uart();
    while(1){
		for(i=0;i<1024;i++){
			_delay_ms(10);
			tx(0xAA);
		}
    }
}
