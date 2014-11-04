#if 0
	shc Version 3.8.7, Generic Script Compiler
	Copyright (c) 1994-2009 Francisco Rosales <frosal@fi.upm.es>

	shc -v -r -T -f pystack.sh 
#endif

static  char data [] = 
#define      shll_z	10
#define      shll	((&data[2]))
	"\134\301\023\310\362\264\144\245\220\340\262\316\227\054"
#define      inlo_z	3
#define      inlo	((&data[14]))
	"\043\062\166"
#define      xecc_z	15
#define      xecc	((&data[19]))
	"\144\203\355\373\244\056\301\373\267\267\132\321\070\042\150\000"
	"\241\120\172\022"
#define      tst1_z	22
#define      tst1	((&data[37]))
	"\175\311\246\361\343\271\157\342\060\325\326\202\300\277\325\314"
	"\221\340\057\075\127\027\050\112"
#define      chk2_z	19
#define      chk2	((&data[64]))
	"\375\266\323\312\240\167\365\242\235\175\370\333\305\321\306\041"
	"\022\045\124\212\163\143\246"
#define      text_z	45
#define      text	((&data[84]))
	"\310\320\016\051\015\053\223\215\246\224\212\231\213\101\371\374"
	"\335\343\153\323\264\000\225\155\356\113\352\247\321\357\354\265"
	"\326\014\017\024\264\073\073\327\056\201\213\210\012\250\154\077"
	"\100\230"
#define      chk1_z	22
#define      chk1	((&data[134]))
	"\173\135\016\176\127\124\254\302\073\173\374\343\211\051\022\336"
	"\013\270\063\174\371\124"
#define      opts_z	3
#define      opts	((&data[156]))
	"\033\330\001"
#define      date_z	1
#define      date	((&data[159]))
	"\203"
#define      msg2_z	19
#define      msg2	((&data[161]))
	"\306\237\212\243\127\222\275\116\363\074\311\146\101\254\104\122"
	"\145\330\052\062\273\034\021\264"
#define      tst2_z	19
#define      tst2	((&data[185]))
	"\171\356\051\025\300\200\050\021\366\101\303\262\316\146\261\173"
	"\006\157\311\337\044\131\111"
#define      lsto_z	1
#define      lsto	((&data[207]))
	"\210"
#define      rlax_z	1
#define      rlax	((&data[208]))
	"\133"
#define      pswd_z	256
#define      pswd	((&data[245]))
	"\136\123\002\174\172\077\351\032\217\335\341\112\371\363\377\274"
	"\103\262\066\150\013\177\234\342\161\075\370\243\166\212\354\325"
	"\335\357\121\127\053\161\006\157\062\223\354\231\305\001\225\042"
	"\357\263\205\103\130\361\004\161\144\205\037\051\011\067\035\262"
	"\245\050\120\320\231\126\100\314\352\055\146\257\056\374\322\036"
	"\260\127\141\010\110\146\172\255\354\231\327\365\321\364\250\166"
	"\034\370\107\266\117\207\203\071\264\351\351\343\346\273\001\226"
	"\022\143\237\133\311\031\010\265\263\340\253\205\324\123\374\361"
	"\114\103\250\233\313\053\324\200\025\275\143\373\170\144\221\213"
	"\310\060\346\221\112\356\107\376\317\363\203\243\106\177\224\223"
	"\303\075\056\216\150\002\017\175\300\162\171\071\327\012\304\237"
	"\073\252\061\205\231\171\204\150\154\010\014\263\210\241\106\113"
	"\336\164\332\106\167\351\304\070\133\075\161\063\107\066\322\203"
	"\340\003\010\172\175\215\343\351\225\357\234\035\220\342\151\156"
	"\127\103\264\317\055\171\007\211\266\171\274\376\257\217\201\220"
	"\223\212\012\020\027\355\371\255\335\225\312\155\170\063\333\320"
	"\167\220\237\244\011\247\055\300\040\352\276\320\171\077\140\014"
	"\312\152\034\341\130\025\216\065\253\131\242\044\215\176\364\004"
	"\017\224\251\030\057\073\162\276\030\124\011\021\107\011\316\213"
	"\273\005\363\306\204\220"
#define      msg1_z	42
#define      msg1	((&data[529]))
	"\241\231\104\053\206\031\011\166\153\140\234\321\173\313\320\174"
	"\231\326\040\032\343\313\221\246\117\363\050\010\211\206\161\173"
	"\320\217\176\026\162\252\052\253\027\346\003\017\000\330\366\125"
	"\334\155\153\144\245\246\323\144\277\047\155\321"/* End of data[] */;
#define      hide_z	4096
#define DEBUGEXEC	0	/* Define as 1 to debug execvp calls */
#define TRACEABLE	1	/* Define as 1 to enable ptrace the executable */

/* rtc.c */

#include <sys/stat.h>
#include <sys/types.h>

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

/* 'Alleged RC4' */

static unsigned char stte[256], indx, jndx, kndx;

/*
 * Reset arc4 stte. 
 */
void stte_0(void)
{
	indx = jndx = kndx = 0;
	do {
		stte[indx] = indx;
	} while (++indx);
}

/*
 * Set key. Can be used more than once. 
 */
void key(void * str, int len)
{
	unsigned char tmp, * ptr = (unsigned char *)str;
	while (len > 0) {
		do {
			tmp = stte[indx];
			kndx += tmp;
			kndx += ptr[(int)indx % len];
			stte[indx] = stte[kndx];
			stte[kndx] = tmp;
		} while (++indx);
		ptr += 256;
		len -= 256;
	}
}

/*
 * Crypt data. 
 */
void arc4(void * str, int len)
{
	unsigned char tmp, * ptr = (unsigned char *)str;
	while (len > 0) {
		indx++;
		tmp = stte[indx];
		jndx += tmp;
		stte[indx] = stte[jndx];
		stte[jndx] = tmp;
		tmp += stte[indx];
		*ptr ^= stte[tmp];
		ptr++;
		len--;
	}
}

/* End of ARC4 */

/*
 * Key with file invariants. 
 */
int key_with_file(char * file)
{
	struct stat statf[1];
	struct stat control[1];

	if (stat(file, statf) < 0)
		return -1;

	/* Turn on stable fields */
	memset(control, 0, sizeof(control));
	control->st_ino = statf->st_ino;
	control->st_dev = statf->st_dev;
	control->st_rdev = statf->st_rdev;
	control->st_uid = statf->st_uid;
	control->st_gid = statf->st_gid;
	control->st_size = statf->st_size;
	control->st_mtime = statf->st_mtime;
	control->st_ctime = statf->st_ctime;
	key(control, sizeof(control));
	return 0;
}

#if DEBUGEXEC
void debugexec(char * sh11, int argc, char ** argv)
{
	int i;
	fprintf(stderr, "shll=%s\n", sh11 ? sh11 : "<null>");
	fprintf(stderr, "argc=%d\n", argc);
	if (!argv) {
		fprintf(stderr, "argv=<null>\n");
	} else { 
		for (i = 0; i <= argc ; i++)
			fprintf(stderr, "argv[%d]=%.60s\n", i, argv[i] ? argv[i] : "<null>");
	}
}
#endif /* DEBUGEXEC */

void rmarg(char ** argv, char * arg)
{
	for (; argv && *argv && *argv != arg; argv++);
	for (; argv && *argv; argv++)
		*argv = argv[1];
}

int chkenv(int argc)
{
	char buff[512];
	unsigned long mask, m;
	int l, a, c;
	char * string;
	extern char ** environ;

	mask  = (unsigned long)&chkenv;
	mask ^= (unsigned long)getpid() * ~mask;
	sprintf(buff, "x%lx", mask);
	string = getenv(buff);
#if DEBUGEXEC
	fprintf(stderr, "getenv(%s)=%s\n", buff, string ? string : "<null>");
#endif
	l = strlen(buff);
	if (!string) {
		/* 1st */
		sprintf(&buff[l], "=%lu %d", mask, argc);
		putenv(strdup(buff));
		return 0;
	}
	c = sscanf(string, "%lu %d%c", &m, &a, buff);
	if (c == 2 && m == mask) {
		/* 3rd */
		rmarg(environ, &string[-l - 1]);
		return 1 + (argc - a);
	}
	return -1;
}

#if !TRACEABLE

#define _LINUX_SOURCE_COMPAT
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <unistd.h>

#if !defined(PTRACE_ATTACH) && defined(PT_ATTACH)
#	define PTRACE_ATTACH	PT_ATTACH
#endif
void untraceable(char * argv0)
{
	char proc[80];
	int pid, mine;

	switch(pid = fork()) {
	case  0:
		pid = getppid();
		/* For problematic SunOS ptrace */
#if defined(__FreeBSD__)
		sprintf(proc, "/proc/%d/mem", (int)pid);
#else
		sprintf(proc, "/proc/%d/as",  (int)pid);
#endif
		close(0);
		mine = !open(proc, O_RDWR|O_EXCL);
		if (!mine && errno != EBUSY)
			mine = !ptrace(PTRACE_ATTACH, pid, 0, 0);
		if (mine) {
			kill(pid, SIGCONT);
		} else {
			perror(argv0);
			kill(pid, SIGKILL);
		}
		_exit(mine);
	case -1:
		break;
	default:
		if (pid == waitpid(pid, 0, 0))
			return;
	}
	perror(argv0);
	_exit(1);
}
#endif /* !TRACEABLE */

char * xsh(int argc, char ** argv)
{
	char * scrpt;
	int ret, i, j;
	char ** varg;

	stte_0();
	 key(pswd, pswd_z);
	arc4(msg1, msg1_z);
	arc4(date, date_z);
	if (date[0] && (atoll(date)<time(NULL)))
		return msg1;
	arc4(shll, shll_z);
	arc4(inlo, inlo_z);
	arc4(xecc, xecc_z);
	arc4(lsto, lsto_z);
	arc4(tst1, tst1_z);
	 key(tst1, tst1_z);
	arc4(chk1, chk1_z);
	if ((chk1_z != tst1_z) || memcmp(tst1, chk1, tst1_z))
		return tst1;
	ret = chkenv(argc);
	arc4(msg2, msg2_z);
	if (ret < 0)
		return msg2;
	varg = (char **)calloc(argc + 10, sizeof(char *));
	if (!varg)
		return 0;
	if (ret) {
		arc4(rlax, rlax_z);
		if (!rlax[0] && key_with_file(shll))
			return shll;
		arc4(opts, opts_z);
		arc4(text, text_z);
		arc4(tst2, tst2_z);
		 key(tst2, tst2_z);
		arc4(chk2, chk2_z);
		if ((chk2_z != tst2_z) || memcmp(tst2, chk2, tst2_z))
			return tst2;
		if (text_z < hide_z) {
			/* Prepend spaces til a hide_z script size. */
			scrpt = malloc(hide_z);
			if (!scrpt)
				return 0;
			memset(scrpt, (int) ' ', hide_z);
			memcpy(&scrpt[hide_z - text_z], text, text_z);
		} else {
			scrpt = text;	/* Script text */
		}
	} else {			/* Reexecute */
		if (*xecc) {
			scrpt = malloc(512);
			if (!scrpt)
				return 0;
			sprintf(scrpt, xecc, argv[0]);
		} else {
			scrpt = argv[0];
		}
	}
	j = 0;
	varg[j++] = argv[0];		/* My own name at execution */
	if (ret && *opts)
		varg[j++] = opts;	/* Options on 1st line of code */
	if (*inlo)
		varg[j++] = inlo;	/* Option introducing inline code */
	varg[j++] = scrpt;		/* The script itself */
	if (*lsto)
		varg[j++] = lsto;	/* Option meaning last option */
	i = (ret > 1) ? ret : 0;	/* Args numbering correction */
	while (i < argc)
		varg[j++] = argv[i++];	/* Main run-time arguments */
	varg[j] = 0;			/* NULL terminated array */
#if DEBUGEXEC
	debugexec(shll, j, varg);
#endif
	execvp(shll, varg);
	return shll;
}

int main(int argc, char ** argv)
{
#if DEBUGEXEC
	debugexec("main", argc, argv);
#endif
#if !TRACEABLE
	untraceable(argv[0]);
#endif
	argv[1] = xsh(argc, argv);
	fprintf(stderr, "%s%s%s: %s\n", argv[0],
		errno ? ": " : "",
		errno ? strerror(errno) : "",
		argv[1] ? argv[1] : "<null>"
	);
	return 1;
}
