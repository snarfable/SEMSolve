%{
	#include <stdio.h>
	#include <stdlib.h>
	#include "parse_symb.h"
%}

%%
commands:
	| commands command
	;
command:
	
	;
%%
