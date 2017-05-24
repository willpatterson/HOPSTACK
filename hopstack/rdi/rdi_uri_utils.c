#include "rdi_uri_utils.h"

short validate_uri(URI uri) { /*TODO*/ return 0; }

void display_URI(URI * uri) {
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

void deallocate_uri(URI * uri) {
    if (uri == NULL) { return; }

    if (uri->scheme != NULL) {
        free(uri->scheme); 
        uri->scheme = NULL;
    }
    if (uri->user != NULL) {
        free(uri->user);
        uri->scheme = NULL;
    }
    if (uri->password != NULL) { 
        free(uri->password);
        uri->scheme = NULL;
    }
    if (uri->host != NULL) {
        free(uri->host);
        uri->scheme = NULL;
    }
    if (uri->port != NULL) {
        free(uri->port); 
        uri->scheme = NULL;
    }
    if (uri->path != NULL) {
        free(uri->path); 
        uri->scheme = NULL;
    }
    if (uri->query != NULL) {
        free(uri->query); 
        uri->scheme = NULL;
    }
    if (uri->fragment != NULL) {
        free(uri->fragment); 
        uri->scheme = NULL;
    }
    free(uri);
    uri = NULL;
    return;
}
