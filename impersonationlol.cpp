// impersonationlol.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <Windows.h>
#include <WtsApi32.h>
#pragma comment(lib,"wtsapi32.lib")


int main(int argc, CHAR* argv[])
{
	if(argc==1){
		printf("usage:\n\t%s <path_to_network_directory>\n\t(use quotes if path has spaces)",argv[0]);
		return 0;
	}
	
	HANDLE token;
	char username[42],username2[42];
	DWORD l=42,l2=42,e;
	WIN32_FIND_DATAA fd;
	GetUserNameA(username,&l);
	printf("trying to access %s with %s...\n",argv[1],username);
	FindFirstFileA(argv[1],&fd);
	if(e=GetLastError()){
		printf("error: %d\n",GetLastError());
	}
	else{
		printf("whew it worked!\n");
	}
	WTSQueryUserToken(WTSGetActiveConsoleSessionId(),&token);
	ImpersonateLoggedOnUser(token);
	GetUserNameA(username2,&l2);
	printf("trying to access %s with %s...\n",argv[1],username2);	
	FindFirstFileA(argv[1],&fd);
	if(e=GetLastError()){
		printf("error: %d\n",GetLastError());
	}
	else{
		printf("whew it worked!\n");
	}
	CloseHandle(token);
	return 0;
}

