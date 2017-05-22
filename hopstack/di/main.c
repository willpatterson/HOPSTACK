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

char valid_schemes[] = "https http scp ftp sftp";

struct URI * parse_uri(char * raw_uri) {
    /* Parses raw URI passed in as character array and returns a URI struct
     * with all pieces of the URI in separate character arrays
     * INPUT: CHARACTER ARRAY CONTAINING URI
     * OUTPUT: URI Struct. (fields that are not found are initialized as NULL)
     *
     * POTENTIAL VULERABILITY:
     * Consider what will happen if there isnt a '://' in a uri..
     * How can this caught before memory is allocated and written too
     * This could be a potential vulerability */

    if (raw_uri == NULL) { return NULL; }

    struct URI *uri = calloc (1, sizeof (struct URI));

    int uri_len = strlen(raw_uri);

    int scheme_found = 0;
    int scheme_end = 0; //First collon
    int user_found = 0;
    int tmp_collon = -1; 

    int path_start = -1;
    int port_start = -1;
    int query_start = -1;
    int fragment_start = -1;
    int host_start = -1;

    char * tmp_uriptr;
    char tmp_char;
    int current_index = -1;
    for (tmp_uriptr = raw_uri; *tmp_uriptr != '\0'; ++tmp_uriptr) { //iterate through raw_uri string
        tmp_char = *tmp_uriptr; //Set tmp char so tmp_uriptr doesnt have to be dereferenced multiple times
        current_index =  tmp_uriptr - raw_uri;

        if (tmp_char == ':') {
            if (!scheme_found) { //Parse out scheme 
                scheme_end = tmp_uriptr - raw_uri;

                //Allocate and store scheme
                uri->scheme = (char *) malloc(sizeof(char)*(scheme_end+1));
                strncpy(uri->scheme, raw_uri, scheme_end); 
                scheme_found = 1;
            }
            else if (scheme_found && user_found) { //Parse out host
                port_start = tmp_uriptr - raw_uri+1;

                //Allocate and store hostname
                uri->host = (char *) malloc(sizeof(char)*((tmp_uriptr-raw_uri-host_start)));
                strncpy(uri->host, raw_uri+host_start+1, tmp_uriptr-raw_uri-host_start-1);
            }
            else if (scheme_found && !user_found) { //Set tmp colon
                tmp_collon = tmp_uriptr - raw_uri;
            }
        }
        else if (tmp_char == '@') { //Parse out user and password
            user_found = 1;
            host_start = tmp_uriptr - raw_uri;
            if (tmp_collon != -1) {
                //Allocate and store user
                uri->user = (char *) malloc(sizeof(char)*(tmp_collon-(scheme_end+3)+1));
                strncpy(uri->user, raw_uri+scheme_end+3, tmp_collon-(scheme_end+3)); 
                
                //Allocate and store password
                uri->password = (char *) malloc(sizeof(char)*((tmp_uriptr-raw_uri)-tmp_collon));
                strncpy(uri->password, raw_uri+tmp_collon+1, (tmp_uriptr-raw_uri)-tmp_collon-1);
                tmp_collon = -1;
            }
            else {
                //Allocate and store user
                uri->user = (char *) malloc(sizeof(char)*((tmp_uriptr-raw_uri)-(scheme_end+3)+1));
                strncpy(uri->user, raw_uri+scheme_end+3, (tmp_uriptr-raw_uri)-(scheme_end+3));
            }
        }
        else if ((tmp_char == '/') && (tmp_uriptr-raw_uri > (scheme_end+2)) && (path_start == -1)) {
            path_start = tmp_uriptr - raw_uri;
            if (port_start != -1) {
                //Allocate and store port
                uri->port = (char *) malloc(sizeof(char)*(path_start-port_start)+1);
                strncpy(uri->port, raw_uri+port_start, path_start-port_start);
            }
            else if (tmp_collon != -1) {
                if (user_found == 1) {
                    //Allocate and store hostname
                    uri->host = (char *) malloc(sizeof(char)*(path_start-host_start)+1);
                    strncpy(uri->host, raw_uri+host_start, path_start-host_start);
                }
                else {
                    //Allocate and store port
                    uri->port = (char *) malloc(sizeof(char)*(path_start-tmp_collon)+1);
                    strncpy(uri->port, raw_uri+tmp_collon+1, path_start-tmp_collon-1);
                    //Allocate and store hostname
                    uri->host = (char *) malloc(sizeof(char)*(tmp_collon-(scheme_end+3)+1));
                    strncpy(uri->host, raw_uri+scheme_end+3, tmp_collon-(scheme_end+3));
                }
            }
            else {
                //Allocate and store host
                uri->host = (char *) malloc(sizeof(char)*(path_start-(scheme_end+3)+1));
                strncpy(uri->host, raw_uri+scheme_end+3, path_start-(scheme_end+3));
            }
        }
        else if (tmp_char == '?') { //Parse out query
            query_start = tmp_uriptr - raw_uri;

            if (path_start != -1) {
                //Allocate and store path
                uri->path = (char *) malloc(sizeof(char)*((tmp_uriptr-raw_uri-1)-path_start+1));
                strncpy(uri->path, raw_uri+path_start+1, ((tmp_uriptr-raw_uri-1)-path_start)); 
            }
            else if (tmp_collon != -1) {
                if (user_found == 1) {
                    //Allocate and store hostname
                    //uri->host = (char *) malloc(sizeof(char)*(path_start-host_start)+1);
                    //strncpy(uri->host, raw_uri+host_start, path_start-host_start);
                }
                else {
                    //Allocate and store port
                    uri->port = (char *) malloc(sizeof(char)*(current_index-tmp_collon)+1);
                    strncpy(uri->port, raw_uri+tmp_collon+1, current_index-tmp_collon-1);
                    //Allocate and store hostname
                    uri->host = (char *) malloc(sizeof(char)*(tmp_collon-(scheme_end+3)+1));
                    strncpy(uri->host, raw_uri+scheme_end+3, tmp_collon-(scheme_end+3));
                }
            }
            else if (port_start != -1) { //Not sure if this conditional does anything
                uri->port = (char *) malloc(sizeof(char)*((tmp_uriptr-raw_uri-1)-port_start+1));
                strncpy(uri->port, raw_uri+port_start+1, ((tmp_uriptr-raw_uri-1)-port_start)); 
            }

        } 
        else if (tmp_char == '#') { //Parse out fragment
            fragment_start = tmp_uriptr - raw_uri;

            if (query_start != -1) {
                //Allocate and store query
                uri->query = (char *) malloc(sizeof(char)*((tmp_uriptr-raw_uri-1)-query_start+1));
                strncpy(uri->query, raw_uri+query_start+1, ((tmp_uriptr-raw_uri-1)-query_start));
            }
            else {
                if (path_start != -1) {
                    //Allocate and store path
                    uri->path = (char *) malloc(sizeof(char)*((tmp_uriptr-raw_uri-1)-path_start+1));
                    strncpy(uri->path, raw_uri+path_start+1, ((tmp_uriptr-raw_uri-1)-path_start)); 
                }
            }
        } 
    } //END OF URI ITERATION LOOP

    //BEGIN Post Iteration Allocation:
    if ((query_start != -1) && (fragment_start == -1)) { //If URI ends with query
        //Allocate and store query
        uri->query = (char *) malloc(sizeof(char)*(uri_len-query_start+1));
        strncpy(uri->query, raw_uri+query_start+1, uri_len-query_start);

        //Allocate and store host
        uri->host = (char *) malloc(sizeof(char)*(query_start-(scheme_end+3))+1);
        strncpy(uri->host, raw_uri+scheme_end+3, query_start-(scheme_end+3));
    }
    else if (fragment_start != -1) { //If URI ends with fragment
        //Allocate and store fragment
        uri->fragment = (char *) malloc(sizeof(char)*(uri_len-fragment_start+1));
        strncpy(uri->fragment, raw_uri+fragment_start+1, (uri_len-fragment_start));
        if ((path_start == -1) && (tmp_collon == -1)) {
            //Allocate and store host
            if (query_start == -1) {
                uri->host = (char *) malloc(sizeof(char)*(fragment_start-(scheme_end+3))+1);
                strncpy(uri->host, raw_uri+scheme_end+3, fragment_start-(scheme_end+3));
            }
            else {
                uri->host = (char *) malloc(sizeof(char)*(query_start-(scheme_end+3))+1);
                strncpy(uri->host, raw_uri+scheme_end+3, query_start-(scheme_end+3));
            }
        }
    }
    else if ((fragment_start == -1) && (query_start == -1)){ //If URI ends with neither query or fragment
        if (path_start != -1) {
            //Allocate and store path
            uri->path = (char *) malloc(sizeof(char)*(uri_len-path_start+1));
            strncpy(uri->path, raw_uri+path_start+1, (uri_len-path_start)); 
        }
        else if (tmp_collon != -1) {
            //Allocate and store port
            uri->port = (char *) malloc(sizeof(char)*(uri_len-tmp_collon)+1);
            strncpy(uri->port, raw_uri+tmp_collon+1, uri_len-tmp_collon);

            if (user_found == 1) {
                //Allocate and store host
                uri->host = (char *) malloc(sizeof(char)*(tmp_collon-host_start)+1);
                strncpy(uri->host, raw_uri+host_start, tmp_collon-host_start);
            }
            else {
                //Allocate and store host
                uri->host = (char *) malloc(sizeof(char)*(tmp_collon-(scheme_end+3))+1);
                strncpy(uri->host, raw_uri+scheme_end+3, tmp_collon-(scheme_end+3));
            }
        }
        else {
            //Allocate and store host
            uri->host = (char *) malloc(sizeof(char)*(uri_len-(scheme_end+3))+1);
            strncpy(uri->host, raw_uri+scheme_end+3, uri_len-(scheme_end+3));
        }
    }
    return uri;
}

short validate_uri(struct URI uri) { /*TODO*/ return 0; }

void deallocate_uri(struct URI * uri) {
    if (uri == NULL) { return; }

    if (uri->scheme != NULL) { free(uri->scheme); }
    if (uri->user != NULL) { free(uri->user); }
    if (uri->password != NULL) { free(uri->password); }
    if (uri->host != NULL) { free(uri->host); }
    if (uri->port != NULL) { free(uri->port); }
    if (uri->path != NULL) { free(uri->path); }
    if (uri->query != NULL) { free(uri->query); }
    if (uri->fragment != NULL) { free(uri->fragment); }
    free(uri);
    return;
}

void display_URI(struct URI * uri) {
    if (uri == NULL) {
        printf("EMPTY URI POINTER\n");
        return;
    }
    printf("Scheme  : ");
    if (uri->scheme != NULL) { printf("%s\n", uri->scheme); }
    else { printf("NONE\n"); }

    printf("User    : ");
    if (uri->user != NULL) { printf("%s\n", uri->user); }
    else { printf("NONE\n"); }

    printf("Password: ");
    if (uri->password != NULL) { printf("%s\n", uri->password); }
    else { printf("NONE\n"); }

    printf("Hostname: ");
    if (uri->host != NULL) { printf("%s\n", uri->host); }
    else { printf("NONE\n"); }

    printf("Port    : ");
    if (uri->port != NULL) { printf("%s\n", uri->port); }
    else { printf("NONE\n"); }
    
    printf("Path    : ");
    if (uri->path != NULL) { printf("%s\n", uri->path); }
    else { printf("NONE\n"); }

    printf("Query   : ");
    if (uri->query!= NULL) { printf("%s\n", uri->query); }
    else { printf("NONE\n"); }

    printf("Fragment: ");
    if (uri->fragment!= NULL) { printf("%s\n", uri->fragment); }
    else { printf("NONE\n"); }

    return;
}


int main() {
    char * URIs[] = {"scheme://user:passowrd@example.com:123/dir1/dir2/dir3?query#fragment", //Passing
                     "scheme://user@example.com:123/dir1/dir2/dir3?query#fragment",          //Passing
                     "scheme://example.com:123/dir1/dir2/dir3?query#fragment",               //Passing
                     "scheme://example.com/dir1/dir2/dir3?query#fragment",                   //Passing
                     "scheme://example.com/dir1/dir2/dir3?query",                            //Passing
                     "scheme://example.com/dir1/dir2/dir3#fragment",                         //Passing
                     "scheme://example.com/dir1/dir2/dir3",                                  //Passing
                     "scheme://example.com",                                                 //Passing
                     "scheme://example.com:123",                                             //Passing
                     "scheme://example.com:123?query#fragment",                              //Passing
                     "scheme://example.com?query",                                           //Passing
                     "scheme://example.com#fragment",                                        //Passing
                     "scheme://example.com?query#fragment",                                  //Passing
                     NULL};

    struct URI * parsed_uri;
    char ** tmp_uriptr;
    for (tmp_uriptr = URIs; *tmp_uriptr != NULL; ++tmp_uriptr) { //iterate through raw_uri string
        printf("////////////////////////////////////////////////////////\n");
        printf("Raw URI: %s\n", *tmp_uriptr);
        printf("Length : %lu\n", strlen(*tmp_uriptr));
        parsed_uri = parse_uri(*tmp_uriptr);
        display_URI(parsed_uri);
        deallocate_uri(parsed_uri);
    }
    printf("////////////////////////////////////////////////////////\n");
}

