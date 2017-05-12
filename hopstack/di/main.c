#include <stdio.h>
#include <string.h>
#include <stdlib.h>

struct URI {
    char * scheme;
    char * user;
    char * password;
    char * host;
    char * port;
    char * path;
    char * query;
    char * fragment;
};

struct rule {
    char * name;
    char * rule;
    char * levels;
    char * priority;
};

struct URP {
    struct URI uri;
    struct rule * rules;
};

struct URI * parse_uri(char * raw_uri) {
    struct URI *uri = malloc (sizeof (struct URI));

    int scheme_found = 0;
    int scheme_end = 0;
    char * tmp_uriptr;
    for (tmp_uriptr = raw_uri; *tmp_uriptr != '\0'; ++tmp_uriptr) {
        if (*tmp_uriptr == ':') {
            if (!scheme_found) {
                scheme_end = tmp_uriptr - raw_uri;
                uri->scheme = (char *) malloc(scheme_end);
                strncpy(uri->scheme, raw_uri, scheme_end);
                scheme_found = 1;
            }
        }
    }
    return uri;
}

int main() {
    char * raw_uri = "scheme://dir1/dir2/dir3";
    struct URI * parsed_uri;
    parsed_uri = parse_uri(raw_uri);
    printf("%s\n", parsed_uri->scheme);
}

