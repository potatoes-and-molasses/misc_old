// ConsoleApplication4.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <Windows.h>
#include <TlHelp32.h>
#include <sddl.h>

DWORD getprocid(WCHAR *procname){
	DWORD procid=-1;
	HANDLE hProcs;
	PROCESSENTRY32 pe;
	pe.dwSize = sizeof(PROCESSENTRY32);
	if((hProcs = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS,0))==INVALID_HANDLE_VALUE){
		
		return procid;	
	}
	do{
		
		if(!wcscmp(pe.szExeFile,procname)){
			procid = pe.th32ProcessID;
			break;
		}
	}while(Process32Next(hProcs,&pe));

	return procid;

	
}

int list32procs(void){
	HANDLE hProcs,hCurrent,hToken;
	PROCESSENTRY32 pe;
	DWORD res,dwReq=0;
	PTOKEN_USER pUserToken;
	pe.dwSize = sizeof(PROCESSENTRY32);
	LPTSTR pszSID;
	TCHAR szUserSID[1024] = {0};
	if((hProcs = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS,0))==INVALID_HANDLE_VALUE){
		
		return 0;	
	}
	do{
		
			hCurrent = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION,0,pe.th32ProcessID);
			res = OpenProcessToken(hCurrent,TOKEN_QUERY,&hToken);
			res = GetTokenInformation(hToken, TokenUser, pUserToken, 0, &dwReq);
			pUserToken = (PTOKEN_USER) HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, dwReq);
			if(NULL != pUserToken){
				if(GetTokenInformation(hToken, TokenUser, pUserToken, dwReq, &dwReq)){
				ConvertSidToStringSid(pUserToken->User.Sid,&pszSID);
				_tprintf(L"%s;%d;%s\n",pe.szExeFile,pe.th32ProcessID,pszSID);
			
				}
				HeapFree(GetProcessHeap(),0,pUserToken);
			}
			
			
			
			

			CloseHandle(hCurrent);
	}while(Process32Next(hProcs,&pe));
	CloseHandle(hProcs);
}
BOOL SetPrivilege(HANDLE hToken, LPCTSTR priv, BOOL enable){
	LUID luid;
	

	if(LookupPrivilegeValue(NULL,priv,&luid)){
		TOKEN_PRIVILEGES tp;
		tp.PrivilegeCount=1;
		tp.Privileges[0].Luid=luid;
		tp.Privileges[0].Attributes = enable ? SE_PRIVILEGE_ENABLED : 0;
		if (AdjustTokenPrivileges(hToken,0,&tp,sizeof(TOKEN_PRIVILEGES),(PTOKEN_PRIVILEGES)NULL,(PDWORD)NULL)){
		return 1;}


	}
	return 0;
}

typedef NTSTATUS (WINAPI *LPFUN_NtCreateThreadEx)(
	OUT PHANDLE hThread,
	IN ACCESS_MASK DesiredAccess,
	IN LPVOID ObjectAttributes,
	IN HANDLE ProcessHandle,
	IN LPTHREAD_START_ROUTINE lpStartAddress,
	IN LPVOID lpParameter,
	IN BOOL CreateSuspended,
	IN ULONG StackZeroBits,
	IN ULONG SizeOfStackCommit,
	IN ULONG SizeOfStackReserve,
	OUT LPVOID lpBytesBuffer);

void usage(WCHAR *name){
	printf("usage: \n%ws <process name/pid> <dll> -- inject dll to process\n%ws -list  -- show running 32bit process list\n",name,name);
		
}


static char b64table[66]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
static char un64table[128] = {65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,62,65,65,65,63,52,53,54,55,56,57,58,59,60,61,65,65,65,65,65,65,65,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,65,65,65,65,65,65,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,
46,47,48,49,50,51,65};

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
	printf("newlen: %d\n",newlen);
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

char * enc(char * st,BOOL mode){
	char * k = "<assembly xmlns=\"urn:schemas-microsoft-com:asm.v1\" manifestVersion=\"1.0\"><assemblyIdentity version=\"1.0.0.0\" processorArchitecture=\"X86\" name=\"mspdbsrv\"";
	if(mode==1){
		st=b64decode(st,strlen(st));
	}
	char *res = (char *)(malloc(strlen(st)));
	
	for(int i=0;i<strlen(st);i++){
		res[i] = (char)(k[i % strlen(k)]^st[i]);
		if (res[i] == 0){
			res[i] ^= k[i%strlen(k)];
	
		}
	}
	res[strlen(st)]=0;
	if(mode==0){
		res = b64encode(res,strlen(res));
	}
	return res;

}

int wmain(int argc, WCHAR* argv[])
{
	
	
	
	HANDLE hToken,hThisProc = GetCurrentProcess();
	OpenProcessToken(hThisProc,TOKEN_ADJUST_PRIVILEGES,&hToken);
	SetPrivilege(hToken,SE_DEBUG_NAME,1);
	CloseHandle(hToken);
	
	if (argc==2 && wcsstr(argv[1],L"list")){
	list32procs();
	return 0;
	}

	if(argc != 3){			
		usage(1+wcsrchr(argv[0],'\\'));
		return 0;
	}
	
	
	WCHAR *wProcName = argv[1];
	char dllPath[_MAX_PATH] = {0};
	wcstombs(dllPath,argv[2],_MAX_PATH);

	
	
	
	
	
	LPVOID remoteAddr;
	DWORD procId;
	HMODULE hKernel32 = GetModuleHandle(TEXT("Kernel32"));
	HMODULE hNtDll = GetModuleHandle(TEXT("ntdll.dll"));

	LPFUN_NtCreateThreadEx funNtCreateThreadEx = (LPFUN_NtCreateThreadEx)(GetProcAddress(hNtDll,("NtCreateThreadEx")));
	
	
	if((procId=getprocid(wProcName))==-1){
		if((procId=_wtol(wProcName))==0){
	printf("no process with such name is running");	
	return 0;
		}
	}
	
	


	
	HANDLE hProc = OpenProcess(PROCESS_ALL_ACCESS,0,procId);
	if(hProc==NULL){
		printf("OpenProcess failed: %d",GetLastError());
		return GetLastError();
	}
	
	remoteAddr = (LPVOID)VirtualAllocEx(hProc,NULL,strlen(dllPath)*2,MEM_RESERVE | MEM_COMMIT,PAGE_EXECUTE_READWRITE);
	
	BOOL hmm = WriteProcessMemory(hProc,remoteAddr,dllPath,strlen(dllPath),NULL);
	if (hmm==0){
		printf("WriteProcessMemory failed: %d",GetLastError());
		return GetLastError();
	}
	LPTHREAD_START_ROUTINE s = (LPTHREAD_START_ROUTINE)GetProcAddress(hKernel32,"LoadLibraryA");
	
	printf("\nhProc: %d",hProc);
	
	HANDLE hThread;// = CreateRemoteThread(hProc,NULL,0,s,remoteAddr,0,NULL);
	
	
	

	printf("\nhThread: %d",hThread);
	NTSTATUS stat = funNtCreateThreadEx(&hThread,GENERIC_ALL,NULL,hProc,s,remoteAddr,FALSE,NULL,NULL,NULL,NULL);
	
	printf("\nhThread: %d",hThread);
	if (hThread == NULL){
		printf("\nCreateRemoteThread failed: %d",GetLastError());
		return GetLastError();
	}
	//WaitForSingleObject(hThread,INFINITE);
	CloseHandle(hProc);
	printf("\nit worked, rejoice!");


	
	

	return 0;
}

