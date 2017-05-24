#include "uri_parser_test.h"
#include "di_uri_parser.c"

//TODO
void display_uri_parsing_test(struct URI_test_results results, struct URI_test expected_vals, URI output) {}

bool compare_null_strings(char * str1, char * str2) {
    if (str1 == NULL) {
        if (str2 == NULL) { return true; }
        else              { return false; }
    }
    else {
        if      (str2 == NULL)            { return false; }
        else if (strcmp(str1, str2) == 0) { return true; }
        else                              { return false; }
    }
}

struct URI_test_results do_uri_test(struct URI_test test_vals) {

    URI * parsed_uri;
    struct URI_test_results results = {false, false, false, false, false, false, false, false};
    if (test_vals.uri != NULL) {
        parsed_uri = parse_uri(test_vals.uri);
    }
    else { return results; }

    results.scheme = compare_null_strings(parsed_uri->scheme, test_vals.scheme);
    results.user = compare_null_strings(parsed_uri->user, test_vals.user);
    results.password = compare_null_strings(parsed_uri->password, test_vals.password);
    results.host = compare_null_strings(parsed_uri->host, test_vals.host);
    results.port = compare_null_strings(parsed_uri->port, test_vals.port);
    results.path = compare_null_strings(parsed_uri->path, test_vals.path);
    results.query = compare_null_strings(parsed_uri->query, test_vals.query);
    results.fragment = compare_null_strings(parsed_uri->fragment, test_vals.fragment);
    
    return results;
}
