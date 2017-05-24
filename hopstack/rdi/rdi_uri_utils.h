#ifndef URI_UTILS
#define URI_UTILS

#include <string.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

typedef struct {
    char * scheme;
    char * user;
    char * password;
    char * host;
    char * port;
    char * path;
    char * query;
    char * fragment;
}URI;

typedef struct {
    char * name;
    char * rule;
    char * levels;
    char * priority;
}rule;

typedef struct {
    URI * uris;
    rule * rules;
}URP;

short validate_uri(URI uri);
void display_URI(URI * uri);
void deallocate_uri(URI * uri);

#endif // URI_UTILS
