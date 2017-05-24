#ifndef URI_PARSER_TEST
#define URI_PARSER_TEST

#include <stdbool.h>

struct URI_test {
    char * uri;
    char * info;

    //Acceptable output:
    char * scheme;
    char * user;
    char * password;
    char * host;
    char * port;
    char * path;
    char * query;
    char * fragment;
};

struct URI_test_results {
    //Acceptable output:
    bool scheme;
    bool user;
    bool password;
    bool host;
    bool port;
    bool path;
    bool query;
    bool fragment;
};


const struct URI_test URI_tests[] = {
    {"scheme://example.com", "Simplist valid URI", "scheme", NULL, NULL, "example.com", NULL, NULL, NULL, NULL}, //SIMPLE BASE CASE
    //WITH PORT
    {"scheme://example.com:123", "Simplist valid URI + PORT", "scheme", NULL, NULL, "example.com", "123", NULL, NULL, NULL},
    {"scheme://example.com:123/dir1/dir2", "Simplist valid URI + PORT + PATH", "scheme", NULL, NULL, "example.com", "123", "/dir1/dir2", NULL, NULL},
    {"scheme://example.com:123/dir1/dir2?query", "Simplist valid URI + PORT + PATH + QUERY", "scheme", NULL, NULL, "example.com", "123", "/dir1/dir2", "query", NULL},
    {"scheme://example.com:123/dir1/dir2#fragment", "Simplist valid URI + PORT + PATH + FRAGMENT", "scheme", NULL, NULL, "example.com", "123", "/dir1/dir2", NULL, "fragment"},
    {"scheme://example.com:123/dir1/dir2?query#fragment", "Simplist valid URI + PROT + PATH + QUERY + FRAGMENT", "scheme", NULL, NULL, "example.com", "123", "/dir1/dir2", "query", "fragment"},
    {"scheme://example.com:123?query", "Simplist valid URI + PORT + QUERY", "scheme", NULL, NULL, "example.com", "123", NULL, "query", NULL},
    {"scheme://example.com:123#fragment", "Simplist valid URI + PORT + FRAGMENT", "scheme", NULL, NULL, "example.com", "123", NULL, NULL, "fragment"},
    {"scheme://example.com:123?query#fragment", "Simplist valid URI + PORT + FRAGMENT + QUERY", "scheme", NULL, NULL, "example.com", "123", NULL, "query", "fragment"},

    {"scheme://user@example.com:123", "SCHEME + USER + HOST + PORT", "scheme", "user", NULL, "example.com", "123", NULL, NULL, NULL},
    {"scheme://user@example.com:123/dir1/dir2", "SCHEME + USER + HOST + PORT + PATH", "scheme", "user", NULL, "example.com", "123", "/dir1/dir2", NULL, NULL},
    {"scheme://user@example.com:123/dir1/dir2?query", "SCHEME + USER + HOST + PORT + PATH + QUERY", "scheme", "user", NULL, "example.com", "123", "/dir1/dir2", "query", NULL},
    {"scheme://user@example.com:123/dir1/dir2#fragment", "SCHEME + USER + HOST + PORT + PATH + FRAGMENT", "scheme", "user", NULL, "example.com", "123", "/dir1/dir2", NULL, "fragment"},
    {"scheme://user@example.com:123/dir1/dir2?query#fragment", "SCHEME + USER + HOST + PORT + PATH + QUERY + FRAGMENT", "scheme", "user", NULL, "example.com", "123", "/dir1/dir2", "query", "fragment"},
    {"scheme://user@example.com:123?query", "SCHEME + USER + HOST + PORT + QUERY", "scheme", "user", NULL, "example.com", "123", NULL, "query", NULL},
    {"scheme://user@example.com:123#fragment", "SCHEME + USER + HOST + PORT + FRAGMENT", "scheme", "user", NULL, "example.com", "123", NULL, NULL, "fragment"},
    {"scheme://user@example.com:123?query#fragment", "SCHEME + USER + HOST + PORT + QUERY + FRAGMENT", "scheme", "user", NULL, "example.com", "123", NULL, "query", "fragment"},

    {"scheme://user:password@example.com:123", "SCHEME + USER + PASSWORD + HOST + PORT", "scheme", "user", NULL, "example.com", "123", NULL, NULL, NULL},
    {"scheme://user:password@example.com:123/dir1/dir2", "SCHEME + USER + PASSWORD + HOST + PORT + PATH", "scheme", "user", "password", "example.com", "123", "/dir1/dir2", NULL, NULL},
    {"scheme://user:password@example.com:123/dir1/dir2?query", "SCHEME + USER + PASSWORD + HOST + PORT + PATH + QUERY", "scheme", "user", "password", "example.com", "123", "/dir1/dir2", "query", NULL},
    {"scheme://user:password@example.com:123/dir1/dir2#fragment", "SCHEME + USER + PASSWORD + HOST + PORT + PATH + FRAGMENT", "scheme", "user", "password", "example.com", "123", "/dir1/dir2", NULL, "fragment"},
    {"scheme://user:password@example.com:123/dir1/dir2?query#fragment", "SCHEME + USER + PASSWORD + HOST + PORT + PATH + QUERY + FRAGMENT", "scheme", "user", "password", "example.com", "123", "/dir1/dir2", "query", "fragment"},
    {"scheme://user:password@example.com:123?query", "SCHEME + USER + PASSWORD + HOST + PORT + QUERY", "scheme", "user", "password", "example.com", "123", NULL, "query", NULL},
    {"scheme://user:password@example.com:123#fragment", "SCHEME + USER + PASSWORD + HOST + PORT + FRAGMENT", "scheme", "user", "password", "example.com", "123", NULL, NULL, "fragment"},
    {"scheme://user:password@example.com:123?query#fragment", "SCHEME + USER + PASSWORD + HOST + PORT + QUERY + FRAGMENT", "scheme", "user", "password", "example.com", "123", NULL, "query", "fragment"},

    //WITHOUT PORT
    {"scheme://example.com", "Simplist valid URI + PORT", "scheme", NULL, NULL, "example.com", "123", NULL, NULL, NULL},
    {"scheme://example.com/dir1/dir2", "Simplist valid URI + PATH", "scheme", NULL, NULL, "example.com", "123", "/dir1/dir2", NULL, NULL},
    {"scheme://example.com/dir1/dir2?query", "Simplist valid URI + PATH + QUERY", "scheme", NULL, NULL, "example.com", "123", "/dir1/dir2", "query", NULL},
    {"scheme://example.com/dir1/dir2#fragment", "Simplist valid URI + PATH + FRAGMENT", "scheme", NULL, NULL, "example.com", "123", "/dir1/dir2", NULL, "fragment"},
    {"scheme://example.com/dir1/dir2?query#fragment", "Simplist valid URI + PATH + QUERY + FRAGMENT", "scheme", NULL, NULL, "example.com", "123", "/dir1/dir2", "query", "fragment"},
    {"scheme://example.com?query", "Simplist valid URI +  QUERY", "scheme", NULL, NULL, "example.com", "123", NULL, "query", NULL},
    {"scheme://example.com#fragment", "Simplist valid URI +  FRAGMENT", "scheme", NULL, NULL, "example.com", "123", NULL, NULL, "fragment"},
    {"scheme://example.com?query#fragment", "Simplist valid URI + FRAGMENT + QUERY", "scheme", NULL, NULL, "example.com", "123", NULL, "query", "fragment"},

    {"scheme://user@example.com", "SCHEME + USER + HOST", "scheme", "user", NULL, "example.com", "123", NULL, NULL, NULL},
    {"scheme://user@example.com/dir1/dir2", "SCHEME + USER + HOST + PATH", "scheme", "user", NULL, "example.com", "123", "/dir1/dir2", NULL, NULL},
    {"scheme://user@example.com/dir1/dir2?query", "SCHEME + USER + HOST + PATH + QUERY", "scheme", "user", NULL, "example.com", "123", "/dir1/dir2", "query", NULL},
    {"scheme://user@example.com/dir1/dir2#fragment", "SCHEME + USER + HOST + PATH + FRAGMENT", "scheme", "user", NULL, "example.com", "123", "/dir1/dir2", NULL, "fragment"},
    {"scheme://user@example.com/dir1/dir2?query#fragment", "SCHEME + USER + HOST + PATH + QUERY + FRAGMENT", "scheme", "user", NULL, "example.com", "123", "/dir1/dir2", "query", "fragment"},
    {"scheme://user@example.com?query", "SCHEME + USER + HOST + QUERY", "scheme", "user", NULL, "example.com", "123", NULL, "query", NULL},
    {"scheme://user@example.com#fragment", "SCHEME + USER + HOST + FRAGMENT", "scheme", "user", NULL, "example.com", "123", NULL, NULL, "fragment"},
    {"scheme://user@example.com?query#fragment", "SCHEME + USER + HOST + QUERY + FRAGMENT", "scheme", "user", NULL, "example.com", "123", NULL, "query", "fragment"},

    {"scheme://user:password@example.com", "SCHEME + USER + PASSWORD + HOST", "scheme", "user", NULL, "example.com", "123", NULL, NULL, NULL},
    {"scheme://user:password@example.com/dir1/dir2", "SCHEME + USER + PASSWORD + HOST + PATH", "scheme", "user", "password", "example.com", "123", "/dir1/dir2", NULL, NULL},
    {"scheme://user:password@example.com/dir1/dir2?query", "SCHEME + USER + PASSWORD + HOST + PATH + QUERY", "scheme", "user", "password", "example.com", "123", "/dir1/dir2", "query", NULL},
    {"scheme://user:password@example.com/dir1/dir2#fragment", "SCHEME + USER + PASSWORD + HOST + PATH + FRAGMENT", "scheme", "user", "password", "example.com", "123", "/dir1/dir2", NULL, "fragment"},
    {"scheme://user:password@example.com/dir1/dir2?query#fragment", "SCHEME + USER + PASSWORD + HOST + PATH + QUERY + FRAGMENT", "scheme", "user", "password", "example.com", "123", "/dir1/dir2", "query", "fragment"},
    {"scheme://user:password@example.com?query", "SCHEME + USER + PASSWORD + HOST + QUERY", "scheme", "user", "password", "example.com", "123", NULL, "query", NULL},
    {"scheme://user:password@example.com#fragment", "SCHEME + USER + PASSWORD + HOST + FRAGMENT", "scheme", "user", "password", "example.com", "123", NULL, NULL, "fragment"},
    {"scheme://user:password@example.com?query#fragment", "SCHEME + USER + PASSWORD + HOST + QUERY + FRAGMENT", "scheme", "user", "password", "example.com", "123", NULL, "query", "fragment"},
    NULL
};

#endif // URI_PARSER_TEST
