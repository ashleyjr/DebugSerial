/*
 * DistanceSensor.c
 *
 * Created: 12/06/2014 20:34:21
 *  Author: Ashley
 */ 


#include <avr/io.h>
#define F_CPU 12000000UL
#define BAUD 57600
#include <util/setbaud.h>

void init_uart(void) { /* 8N1 */
	UBRR0H = UBRRH_VALUE; UBRR0L = UBRRL_VALUE;
	UCSR0A = USE_2X << U2X0;
	UCSR0B = _BV(RXEN0) | _BV(TXEN0);
UCSR0C = _BV(UCSZ00) | _BV(UCSZ01); }
void tx(uint8_t b) { while(!(UCSR0A & _BV(UDRE0))); UDR0 = b; }
uint8_t rx(void) { while(!(UCSR0A & _BV(RXC0))); return UDR0; }

	
int main(void)
{
	init_uart();
    while(1)
    {
		tx('A');
    }
}