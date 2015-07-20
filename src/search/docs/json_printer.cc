#include "json_printer.h"

using namespace std;

namespace docs {

static string quote(const string &s) {
    return "\"" + s + "\"";
}

JsonPrinter::JsonPrinter(ostream &out)
    : DocPrinter(out) {
}

void JsonPrinter::print_synopsis(const DocStruct &) {
}

void JsonPrinter::print_key_value_pair(const string &key, const string &value) const {
    os << quote(key) << ": " << quote(value) << "," << endl;
}

void JsonPrinter::print_arg(const ArgumentInfo &arg) const {
    os << quote(arg.kwd) << ": {" << endl;
    print_key_value_pair("type_name", arg.type_name);
    print_key_value_pair("default_value", arg.default_value);
    os << "}" << endl;
}

void JsonPrinter::print_usage(string plugin, const DocStruct &info) {
    if (plugin.empty() || info.type == "AbstractTask" || info.type == "ScalarEvaluator")
        return;
    os << quote(plugin) << ": {" << endl;
    print_key_value_pair("type", info.type);
    os << quote("args") << ": {" << endl;
    for (auto &arg : info.arg_help) {
        print_arg(arg);
    }
    os << "}" << endl << "}," << endl;
}

void JsonPrinter::print_arguments(const DocStruct &) {
}

void JsonPrinter::print_notes(const DocStruct &) {
}

void JsonPrinter::print_language_features(const DocStruct &) {
}

void JsonPrinter::print_properties(const DocStruct &) {
}

void JsonPrinter::print_category_header(string) {
}

void JsonPrinter::print_category_footer() {
    os << endl;
}

void JsonPrinter::print_all() {
    os << "{" << endl;
    DocPrinter::print_all();
    os << "}" << endl;
}

}
