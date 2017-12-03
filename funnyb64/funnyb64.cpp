// funnyb64.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <stdlib.h>
#include <Windows.h>
#include <string.h>





static char b64table[66]="NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm5678901234+/=";
static char un64table[128] = {65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,62,65,65,65,63,57,58,59,60,61,52,53,54,55,56,65,65,65,65,65,65,65,13,14,15,16,17,18,19,20,21,22,23,24,25,0,1,2,3,4,5,6,7,8,9,10,11,12,65,65,65,65,65,65,39,40,41,42,43,44,45,
46,47,48,49,50,51,26,27,28,29,30,31,32,33,34,35,36,37,38,65};

char * b64decode(char *text,int len){
	
	
	char *r = (char *)malloc(len);
	ZeroMemory(r,len);
	int i,padding=0;

	for(i=0;i<len-3;i+=4){
		


		*r++ = (un64table[text[i]] << 2) | ((un64table[text[i+1]]) >> 4);

		if(text[i+2]=='='){
			padding=2;
			break;
		}

		*r++ = ((un64table[text[i+1]] & 0x0f) << 4) | ((un64table[text[i+2]]) >> 2);

		if(text[i+3]=='='){
			padding=1;
			break;
		}

		*r++ = ((un64table[text[i+2]] & 0x03) << 6) | ((un64table[text[i+3]]));

	}
	*r++ = '\0';
	int length = ((len)*3/4) - padding;

	return r-length-1;
}



char * b64encode(char *text,int len){
	int i;
	int newlen = len % 3 ?  4*(len-len%3)/3+4 : 4*len/3;

	 char *p=(char *)(malloc(newlen+1));
	
	
	for (i=0;i<len-2;i+=3){
//first thing
		*p++ = b64table[((text[i] & 0xfc)) >> 2];		
		//second thing
		*p++ = b64table[((text[i] & 0x3) << 4) | ((int)((text[i+1] & 0xf0) >> 4))];
			//indenting comments
		*p++ = b64table[((text[i+1] & 0xf) << 2) | ((int)((text[i+2] & 0xc0) >> 6))];
				//is fun
		*p++ = b64table[(text[i+2] & 0x3f)];
					//(hmmm)
	}
	
	if(i<len){
		*p++ = b64table[((text[i] & 0xfc)) >> 2];
		if(i==len-1){
			*p++ = b64table[(text[i] & 0x3) << 4];
			*p++ = '=';
		}
		else{
			*p++ = b64table[((text[i] & 0x3) << 4) | ((int)((text[i+1] & 0xf0) >> 4))];
			*p++ = b64table[((text[i+1] & 0xf) << 2)];
		}
		*p++ = '=';
		
	}
	
	*p++ = '\0';


	
	
	
	return p-newlen-1;
}

wchar_t * b64encodeW(wchar_t* text, int len) {
	char * tempBuf = (char *)malloc(len * 2);
	ZeroMemory(tempBuf, len * 2);
	wchar_t * tempBufW = (wchar_t *)malloc(len * 2);
	ZeroMemory(tempBufW, len * 2);
	wcstombs(tempBuf, text, len);
	tempBuf = b64encode(tempBuf, len);
	mbstowcs(tempBufW, tempBuf, strlen(tempBuf));
	return tempBufW;
}

wchar_t * b64decodeW(wchar_t* text, int len) {
	char * tempBuf = (char *)malloc(len * 2);
	ZeroMemory(tempBuf, len * 2);
	wchar_t * tempBufW = (wchar_t *)malloc(len * 2);
	ZeroMemory(tempBufW, len * 2);
	wcstombs(tempBuf, text, len);
	tempBuf = b64decode(tempBuf, len);
	mbstowcs(tempBufW, tempBuf, strlen(tempBuf));
	return tempBufW;
}

int main(int argc, char* argv[])
{


		char * name=1+strrchr(argv[0],'\\');
		
		if (argc!=3){
		printf("usage:\n %s -e rawdata\n %s -d encodeddata",name,name);
		return 0;
		}
		
		if(argv[1][1]=='d'){
			printf(b64decode(argv[2],strlen(argv[2])));
		}
		if(argv[1][1]=='e'){
			printf(b64encode(argv[2],strlen(argv[2])));
		}


	
}

