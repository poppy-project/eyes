#include <stdlib.h>
#include <unistd.h>
#include <linux/i2c.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <string.h>
#include <stdio.h>

int i = 0;
int j = 0;
int k = 0;

int main(void)
{
	char recieveBuffer[32]; //The Buffer that will hold onto recieved data
 	char transferBuffer[32]; //The buffer that holds data that we will send
 	int address = 0x70; //The address of the LED matrix
 	int tenBitAddress = 0; //variable that says we aren’t using 10-bit

 	//addressing
 	//Initialize the I2C channel
 	int i2cHandle = open("/dev/i2c-4",O_RDWR);
	//Tell the I2C channel we aren’t using ten bit addressing
 	ioctl(i2cHandle,I2C_TENBIT,tenBitAddress);
	//Tell the I2C channel we have a slave at Address 70
 	ioctl(i2cHandle,I2C_SLAVE,address);

	//make sure there is no data in our buffers
	memset(recieveBuffer, 0 , sizeof(recieveBuffer));
	memset(transferBuffer,0,sizeof(transferBuffer));
	//start internal oscillator on the LED matrix by sending 0x21 command
	transferBuffer[0] = 0x21;
	write(i2cHandle, transferBuffer, 1);
	//enable display and turn blink off by sending 0x81
	transferBuffer[0] = 0x81;
	write(i2cHandle, transferBuffer,1);
	//set brightness to max by sending 0xEF
	transferBuffer[0] = 0xEF;
	write(i2cHandle, transferBuffer,1);
	//top level loop keeps track of which column we are on
	for(i = 0; i<16;i=i+1)
	{
		for(j = 0; j<9;j++)
		{
			//we send two bytes in this case, so we load the
			//transfer buffer with 2 bytes
			//and set the first Byte to transfer to the column number
			transferBuffer[0] = i;
			//set the second Byte to transfer to the lights to turn on
			transferBuffer[1] |= 0x01 << j;
			write(i2cHandle, transferBuffer,2);
			//wait a while
			usleep(50000);
		}
	//make sure a column is completely off before leaving it
	transferBuffer[1] = 0x00;
	// write(i2cHandle, transferBuffer,2);
	}
	transferBuffer[1] = 0xFF;
	for(i = 0; i<16;i=i+1)
	{
		for(j = 0; j<9;j++)
		{
			//we send two bytes in this case, so we load the
			//transfer buffer with 2 bytes
			//and set the first Byte to transfer to the column number
			transferBuffer[0] = i;
			//set the second Byte to transfer to the lights to turn on
			transferBuffer[1] &= ~(0x01 << j);
			write(i2cHandle, transferBuffer,2);
			//wait a while
			usleep(50000);
		}
	//make sure a column is completely off before leaving it
	transferBuffer[1] = 0xFF;
	// write(i2cHandle, transferBuffer,2);
	}
	return 0;
}
