#ifndef URI_PARSER
#define URI_PARSER

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include "di_uri_utils.h"

const char valid_schemes[] = "https http scp ftp sftp";

short allocate_and_copy_str(char ** copy_to, char * copy_from, int length);
URI * parse_uri(char * raw_uri);

#endif // URI_PARSER
