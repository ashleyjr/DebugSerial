#define F_CPU 20000000UL
#define BAUD 115200

#include <avr/io.h>
#include <util/delay.h>
#include <util/setbaud.h>
#include "Waveforms.h"

void initUart(void) {
	UBRR1H = UBRRH_VALUE; UBRR1L = UBRRL_VALUE;
	UCSR1A = USE_2X << U2X1;
	UCSR1B = _BV(RXEN1) | _BV(TXEN1);
	UCSR1C = _BV(UCSZ10) | _BV(UCSZ11);
}

void tx(uint8_t b) {
	while(!(UCSR1A & _BV(UDRE1))); UDR1 = b;
}

void initAdc(){
	ADMUX = (1<<REFS0);
	ADCSRA = (1<<ADEN)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);
}

uint16_t readAdc()
{
	ADMUX = 0;
	ADCSRA |= (1<<ADSC);
	while(ADCSRA & (1<<ADSC));
	return (ADCH << 8)|ADC;//(ADCH << 8)|(ADCL);
}

void varyDelay(uint16_t delay){
	uint16_t i;
	for(i=0;i<delay;i++){
		_delay_ms(1);
	}
}

int main(void){
	uint16_t limit = 10;
	uint8_t x;
	uint16_t i;
	initUart();
	initAdc();
	x = 0;
	while(1){
		
		
		// Plot using 255 x 255 
		for(i=0;i<255;i++){
			limit = ((readAdc()/10) + 1);
			tx(0x03);			// Add point code with 1 x byte and 1 y byte
			varyDelay(limit);
			tx(x);
			varyDelay(limit);
			tx(sine[x]);
			varyDelay(limit);
			x++;
			if(255 == x){
				tx(0x0F);		// clear code
				varyDelay(limit);
			}
		}
		
		
		// Plot using 65536 x 65536
		for(i=0;i<10000;i++){
			limit = ((readAdc()/10) + 1);
			tx(0x53);			// Add point code with 2 x bytes and 2 y bytes
			varyDelay(limit);
			tx(x >> 8);
			varyDelay(limit);
			tx(x);
			varyDelay(limit);
			tx(0);
			varyDelay(limit);
			tx(sine[x]);
			x++;
			varyDelay(limit);
			if(65536 == x){
				tx(0x0F);		// clear code
				varyDelay(limit);
			}
		}

		
		
		
		for(i=0;i<255;i++){
			limit = ((readAdc()/10) + 1);
			tx(0xA3);			// Add point code with 3 x bytes and 3 y bytes
			varyDelay(limit);
			tx(x >> 16);
			varyDelay(limit);
			tx(x >> 8);
			varyDelay(limit);
			tx(x);
			varyDelay(limit);
			tx(0);
			varyDelay(limit);
			tx(0);
			varyDelay(limit);
			tx(sine[x]);
			x++;
			varyDelay(limit);
			if(65536 == x){
				tx(0x0F);		// clear code
				varyDelay(limit);
			}
		}

		
	}
}