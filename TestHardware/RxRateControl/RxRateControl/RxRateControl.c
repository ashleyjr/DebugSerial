#define F_CPU 20000000UL
#define BAUD 115200

#include <avr/io.h>
#include <util/delay.h>
#include <util/setbaud.h>

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

int main(void){
	uint16_t i;
	uint16_t limit = 10;
	initUart();
	initAdc();
	while(1){
		limit = ((readAdc()/100) + 1);
		for(i=0;i<limit;i++){
			_delay_ms(1);
		}
		tx(rand());
	}
}