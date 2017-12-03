// process_thing.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <Windows.h>
#include <WtsApi32.h>
#include <stdio.h>
#include <UserEnv.h>

void debug(char *output){
	FILE* lol;
	lol=fopen("C:\\users\\public\\music\\errors","a");
	fputs(output,lol);
	fclose(lol);
	
}
int main(int argc, CHAR* argv[])
{
	//argv[1] is session id, argv[2] is username, argv[3] is cmd
	DWORD sessionId = atoi(argv[1]);
	printf("%d\n",argc);
	printf("session id: %d\n",sessionId);
	printf("username: %s\n",argv[2]);
	printf("ps cmd: %s\n",argv[3]);
	
	PROFILEINFOA prof;
	ZeroMemory(&prof,sizeof(PROFILEINFO));
	prof.dwSize = sizeof(PROFILEINFO);
	prof.lpUserName = argv[2];
	
	char err[256]={0};
	//char params[512] = "-c \"whoami >> C:\\users\\public\\music\\output\"";
	char params[8192] = {0};
	sprintf(params," -enc %s",argv[3]);
	HANDLE token,temp;
	PROCESS_INFORMATION pi = {0};
	STARTUPINFOA si = {sizeof(STARTUPINFO)};
	si.wShowWindow = SW_HIDE;
	si.lpDesktop = "";
	//random experiments start here!
	//!!@!@!or maybe they were too stupid and i deleted them

	//si.hStdOutput = GetStdHandle(STD_OUTPUT_HANDLE);
	//si.hStdError = GetStdHandle(STD_ERROR_HANDLE);
	//random experiments end here
	
	if(!WTSQueryUserToken(sessionId,&temp)){
		sprintf(err,"wts error: %d\n",GetLastError());
		debug(err);
	}
	if(!DuplicateTokenEx(temp, TOKEN_ALL_ACCESS, NULL, SecurityIdentification, TokenPrimary,&token)){
		sprintf(err,"dup error: %d\n",GetLastError());
		debug(err);
	}
	CloseHandle(temp);
	
	if(!LoadUserProfileA(token,&prof)){
		sprintf(err,"load error: %d\n",GetLastError());
		debug(err);
	}

	
	char spacedPath[8193] = {0};//params
	sprintf(spacedPath, " %s", params);
	if(!CreateProcessAsUserA(token, "C:\\windows\\system32\\windowspowershell\\v1.0\\powershell.exe",params, NULL,NULL,TRUE,CREATE_NO_WINDOW,NULL,NULL,&si,&pi)){
		sprintf(err,"create error: %d\n",GetLastError());
		debug(err);
	}
	if(!UnloadUserProfile(token,prof.hProfile)){
		sprintf(err,"unload error: %d\n",GetLastError());
		debug(err);
	}
		
	
	CloseHandle(token);

	return 0;
}

