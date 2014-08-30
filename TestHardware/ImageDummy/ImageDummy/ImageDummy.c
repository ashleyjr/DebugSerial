#define F_CPU 20000000UL
#define BAUD 115200

#include <avr/io.h>
#include <util/delay.h>
#include <util/setbaud.h>
#include "Lenna.h"

void initUart(void) {
	UBRR1H = UBRRH_VALUE; UBRR1L = UBRRL_VALUE;
	UCSR1A = USE_2X << U2X1;
	UCSR1B = _BV(RXEN1) | _BV(TXEN1);
	UCSR1C = _BV(UCSZ10) | _BV(UCSZ11);
}

void tx(uint8_t b) {
	while(!(UCSR1A & _BV(UDRE1))); UDR1 = b;
}

int main(void)
{
	uint8_t i,j;
	uint8_t data;
	initUart();
	
	while(1){
		
		for(i=0;i<ROW;i++){
			for(j=0;j<COL;j++){
				//_delay_ms(1);
				data = pgm_read_byte(&(Lenna_R[i][j]));
				tx(data);
			}
			tx('\n');
		}
		tx('R');
		tx('\n');
	
		for(i=0;i<ROW;i++){
			for(j=0;j<COL;j++){
				//_delay_ms(1);
				data = pgm_read_byte(&(Lenna_G[i][j]));
				tx(data);
			}
			tx('\n');
		}
		tx('G');
		tx('\n');

		for(i=0;i<ROW;i++){
			for(j=0;j<COL;j++){
				//_delay_ms(1);
				data = pgm_read_byte(&(Lenna_B[i][j]));
				tx(data);
			}
			tx('\n');
		}
		tx('B');
		tx('\n');
	}
}
