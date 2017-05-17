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

char * valid_schemes = "https http scp ftp sftp";

struct URI * parse_uri(char * raw_uri) {
    struct URI *uri = malloc (sizeof (struct URI));

    int uri_len = strlen(raw_uri);

    int scheme_found = 0;
    int scheme_end = 0; //First collon
    int user_found = 0;

    int user_coordinates[2] = {-1};
    int password_cooridnates[2] = {-1};
    int host_cooridnates[2] = {-1};
    int port_coordinates[2] = {-1};
    int path_coordinates[2] = {-1};

    int tmp_collon = -1; 

    int path_start = -1;

    char * tmp_uriptr;
    for (tmp_uriptr = raw_uri; *tmp_uriptr != '\0'; ++tmp_uriptr) {
        if (*tmp_uriptr == ':') {
            if (!scheme_found) { //Parse out scheme
                scheme_end = tmp_uriptr - raw_uri;
                uri->scheme = (char *) malloc(scheme_end);
                strncpy(uri->scheme, raw_uri, scheme_end);
                scheme_found = 1;
            }
            else if (scheme_found && user_found) { //Parse out port
                port_coordinates[0] = tmp_uriptr - raw_uri;
                host_cooridnates[1] = port_coordinates[0] + 1; //this could cause problems
            }
            else if (scheme_found && !user_found) {
                tmp_collon = tmp_uriptr - raw_uri;
            }
        }
        else if (*tmp_uriptr == '@') { //Parse out user and password
            user_found = 1;
            host_cooridnates[0] = tmp_uriptr - raw_uri;
            if (tmp_collon) {
                user_coordinates[0] = scheme_end + 2;
                user_coordinates[1] = tmp_collon;
                password_cooridnates[0] = tmp_collon;
                password_cooridnates[1] = tmp_uriptr - raw_uri;
            }
            else {
                user_coordinates[0] = scheme_end + 2;
                user_coordinates[1] = tmp_uriptr - raw_uri;
            }
        }
        else if ((*tmp_uriptr == '/') && (tmp_uriptr-raw_uri > (scheme_end+2)) && (path_coordinates[0] == -1)) { //Parse out path
            path_coordinates[0] = tmp_uriptr - raw_uri;
            port_coordinates[1] = tmp_uriptr - raw_uri - 1;
        }

    }
    printf("User Coordinates\n");
    printf("Start: %d\nEnd: %d\n", user_coordinates[0], user_coordinates[1]); 
    printf("Password Coordinates\n");
    printf("Start: %d\nEnd: %d\n", password_cooridnates[0], password_cooridnates[1]); 
    printf("Host Coordinates\n");
    printf("Start: %d\nEnd: %d\n", host_cooridnates[0], host_cooridnates[1]); 
    printf("Port Coordinates\n");
    printf("Start: %d\nEnd: %d\n", port_coordinates[0], port_coordinates[1]); 
    printf("Path Coordinates\n");
    printf("Start: %d\nEnd: %d\n", path_coordinates[0], path_coordinates[1]); 
    return uri;
}

int main() {
    char * raw_uri = "scheme://user:passowrd@example.com:123/dir1/dir2/dir3";
    struct URI * parsed_uri;
    printf("Len: %lu\n", strlen(raw_uri));
    printf("Raw: %s\n", raw_uri);
    parsed_uri = parse_uri(raw_uri);
    //printf("%s\n", parsed_uri->scheme);
}

