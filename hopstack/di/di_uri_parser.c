#include "di_uri_parser.h"
#include "di_uri_utils.h"

short allocate_and_copy_str(char ** copy_to, char * copy_from, int length) {
    if ((copy_from == NULL) || (copy_to == NULL)) { return -1; }

    *copy_to = (char *) malloc((sizeof(char)*length)+1);
    strncpy(*copy_to, copy_from, length); 
    return 0;
}

URI * parse_uri(char * raw_uri) {
    /* Parses raw URI passed in as character array and returns a URI struct
     * with all pieces of the URI in separate character arrays
     * INPUT: CHARACTER ARRAY CONTAINING URI
     * OUTPUT: URI Struct. (fields that are not found are initialized as NULL)
     *
     * POTENTIAL VULERABILITY:
     * Consider what will happen if there isnt a '://' in a uri..
     * How can this caught before memory is allocated and written too
     * This could be a potential vulerability 
     * 
     * TODO:
     * - Impelment support for IPV6
     */

    if (raw_uri == NULL) { return NULL; }

    URI *uri = calloc (1, sizeof (URI));

    int uri_len = strlen(raw_uri);

    int test = 22;
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
        current_index = tmp_uriptr - raw_uri;

        if (tmp_char == ':') {
            if (!scheme_found) { //Parse out scheme 
                scheme_end = current_index;

                //Allocate and store scheme
                allocate_and_copy_str(&uri->scheme, raw_uri, scheme_end); 
                scheme_found = 1;
            }
            else if (scheme_found && user_found) { //Parse out host
                port_start = current_index+1;

                //Allocate and store hostname
                allocate_and_copy_str(&uri->host, raw_uri+host_start+1, current_index-host_start-1);
            }
            else if (scheme_found && !user_found) { //Set tmp colon
                tmp_collon = current_index;
            }
        }
        else if (tmp_char == '@') { //Parse out user and password
            user_found = 1;
            host_start = current_index;
            if (tmp_collon != -1) {
                //Allocate and store user
                allocate_and_copy_str(&uri->user, raw_uri+scheme_end+3, tmp_collon-(scheme_end+3)); 
                
                //Allocate and store password
                allocate_and_copy_str(&uri->password, raw_uri+tmp_collon+1, (current_index)-tmp_collon-1);
                tmp_collon = -1;
            }
            else {
                //Allocate and store user
                allocate_and_copy_str(&uri->user, raw_uri+scheme_end+3, (current_index)-(scheme_end+3));
            }
        }
        else if ((tmp_char == '/') && (current_index > (scheme_end+2)) && (path_start == -1)) {
            path_start = current_index;
            if (port_start != -1) {
                //Allocate and store port
                allocate_and_copy_str(&uri->port, raw_uri+port_start, path_start-port_start);
            }
            else if (tmp_collon != -1) {
                if (user_found == 1) {
                    //Allocate and store hostname
                    allocate_and_copy_str(&uri->host, raw_uri+host_start, path_start-host_start);
                }
                else {
                    //Allocate and store port
                    allocate_and_copy_str(&uri->port, raw_uri+tmp_collon+1, path_start-tmp_collon-1);
                    //Allocate and store hostname
                    allocate_and_copy_str(&uri->host, raw_uri+scheme_end+3, tmp_collon-(scheme_end+3));
                }
            }
            else {
                //Allocate and store host
                allocate_and_copy_str(&uri->host, raw_uri+scheme_end+3, path_start-(scheme_end+3));
            }
        }
        else if (tmp_char == '?') { //Parse out query
            query_start = current_index;

           if (path_start != -1) {
                //Allocate and store path
                allocate_and_copy_str(&uri->path, raw_uri+path_start+1, ((current_index-1)-path_start)); 
            }
            else if (tmp_collon != -1) {
                if (user_found == 1) { //TODO
                    //Allocate and store hostname
                    allocate_and_copy_str(&uri->host, raw_uri+host_start, path_start-host_start);
                }
                else {
                    //Allocate and store port
                    allocate_and_copy_str(&uri->port, raw_uri+tmp_collon+1, current_index-tmp_collon-1);
                    //Allocate and store hostname
                    allocate_and_copy_str(&uri->host, raw_uri+scheme_end+3, tmp_collon-(scheme_end+3));
                }
            }
            else if (port_start != -1) { //Not sure if this conditional does anything
                allocate_and_copy_str(&uri->port, raw_uri+port_start+1, ((current_index-1)-port_start)); 
            }

        } 
        else if (tmp_char == '#') { //Parse out fragment
            fragment_start = current_index;

            if (query_start != -1) {
                //Allocate and store query
                allocate_and_copy_str(&uri->query, raw_uri+query_start+1, ((current_index-1)-query_start));
            }
            else {
                if (path_start != -1) {
                    //Allocate and store path
                    allocate_and_copy_str(&uri->path, raw_uri+path_start+1, ((current_index-1)-path_start)); 
                }
            }
        } 
    } //END OF URI ITERATION LOOP

    //BEGIN Post Iteration Allocation:
    if ((query_start != -1) && (fragment_start == -1)) { //If URI ends with query
        //Allocate and store query
        allocate_and_copy_str(&uri->query, raw_uri+query_start+1, uri_len-query_start);

        //Allocate and store host
        allocate_and_copy_str(&uri->host, raw_uri+scheme_end+3, query_start-(scheme_end+3));
    }
    else if (fragment_start != -1) { //If URI ends with fragment
        //Allocate and store fragment
        allocate_and_copy_str(&uri->fragment, raw_uri+fragment_start+1, (uri_len-fragment_start));
        if ((path_start == -1) && (tmp_collon == -1)) {
            //Allocate and store host
            if (query_start == -1) {
                allocate_and_copy_str(&uri->host, raw_uri+scheme_end+3, fragment_start-(scheme_end+3));
            }
            else {
                allocate_and_copy_str(&uri->host, raw_uri+scheme_end+3, query_start-(scheme_end+3));
            }
        }
    }
    else if ((fragment_start == -1) && (query_start == -1)){ //If URI ends with neither query or fragment
        if (path_start != -1) {
            //Allocate and store path
            allocate_and_copy_str(&uri->path, raw_uri+path_start+1, (uri_len-path_start)); 
        }
        else if (tmp_collon != -1) {
            //Allocate and store port
            allocate_and_copy_str(&uri->port, raw_uri+tmp_collon+1, uri_len-tmp_collon);

            if (user_found == 1) {
                //Allocate and store host
                allocate_and_copy_str(&uri->host, raw_uri+host_start, tmp_collon-host_start);
            }
            else {
                //Allocate and store host
                allocate_and_copy_str(&uri->host, raw_uri+scheme_end+3, tmp_collon-(scheme_end+3));
            }
        }
        else {
            //Allocate and store host
            allocate_and_copy_str(&uri->host, raw_uri+scheme_end+3, uri_len-(scheme_end+3));
        }
    }
    return uri;
}

int main() {
    char * URIs[] = {"scheme://example.com",                                                 //Passing

                     //BEGIN ALL POSSIBILITIES WITH PORT
                     "scheme://example.com:123",                                             //Passing
                     "scheme://example.com:123/dir1/dir2/dir3",
                     "scheme://example.com:123/dir1/dir2/dir3?query",
                     "scheme://example.com:123/dir1/dir2/dir3#fragment",
                     "scheme://example.com:123/dir1/dir2/dir3?query#fragment",
                     "scheme://example.com:123?query",
                     "scheme://example.com:123#fragment",
                     "scheme://example.com:123?query#fragment",                              //Passing

                     "scheme://user@example.com:123",
                     "scheme://user@example.com:123/dir1/dir2/dir3",
                     "scheme://user@example.com:123/dir1/dir2/dir3?query",
                     "scheme://user@example.com:123/dir1/dir2/dir3#fragment",
                     "scheme://user@example.com:123/dir1/dir2/dir3?query#fragment",
                     "scheme://user@example.com:123?query",
                     "scheme://user@example.com:123#fragment",
                     "scheme://user@example.com:123?query#fragment",

                     "scheme://user:password@example.com:123",
                     "scheme://user:password@example.com:123/dir1/dir2/dir3",
                     "scheme://user:password@example.com:123/dir1/dir2/dir3?query",
                     "scheme://user:password@example.com:123/dir1/dir2/dir3#fragment",
                     "scheme://user:password@example.com:123/dir1/dir2/dir3?query#fragment", //Passing (FULL URI)
                     "scheme://user:password@example.com:123?query",
                     "scheme://user:password@example.com:123#fragment",
                     "scheme://user:password@example.com:123?query#fragment",
                     //END 
                     
                     //BEGIN ALL POSSIBILITIES WITHOUT PORT
                     "scheme://example.com/dir1/dir2/dir3",                                  //Passing
                     "scheme://example.com/dir1/dir2/dir3?query",                            //Passing
                     "scheme://example.com/dir1/dir2/dir3#fragment",                         //Passing
                     "scheme://example.com/dir1/dir2/dir3?query#fragment",                   //Passing
                     "scheme://example.com?query",                                           //Passing
                     "scheme://example.com#fragment",                                        //Passing
                     "scheme://example.com?query#fragment",                                  //Passing

                     "scheme://user@example.com",
                     "scheme://user@example.com/dir1/dir2/dir3",
                     "scheme://user@example.com/dir1/dir2/dir3?query",
                     "scheme://user@example.com/dir1/dir2/dir3#fragment",
                     "scheme://user@example.com/dir1/dir2/dir3?query#fragment",
                     "scheme://user@example.com?query",
                     "scheme://user@example.com#fragment",
                     "scheme://user@example.com?query#fragment",

                     "scheme://user:password@example.com",
                     "scheme://user:password@example.com/dir1/dir2/dir3",
                     "scheme://user:password@example.com/dir1/dir2/dir3?query",
                     "scheme://user:password@example.com/dir1/dir2/dir3#fragment",
                     "scheme://user:password@example.com/dir1/dir2/dir3?query#fragment",
                     "scheme://user:password@example.com?query",
                     "scheme://user:password@example.com#fragment",
                     "scheme://user:password@example.com?query#fragment",

                     //OLD
                     "scheme://user:passowrd@example.com:123/dir1/dir2/dir3?query#fragment", //Passing
                     "scheme://user@example.com:123/dir1/dir2/dir3?query#fragment",          //Passing
                     "scheme://example.com:123/dir1/dir2/dir3?query#fragment",               //Passing
                     "scheme://example.com/dir1/dir2/dir3?query#fragment",                   //Passing
                     "scheme://example.com/dir1/dir2/dir3?query",                            //Passing
                     "scheme://example.com/dir1/dir2/dir3#fragment",                         //Passing
                     "scheme://example.com/dir1/dir2/dir3",                                  //Passing
                     "scheme://example.com?query",                                           //Passing
                     "scheme://example.com#fragment",                                        //Passing
                     "scheme://example.com?query#fragment",                                  //Passing
                     "scheme://user@example.com:123",
                     "scheme://user:password@example.com:123",
                     NULL};

    URI * parsed_uri;
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

