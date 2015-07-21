#include "json_printer.h"

using namespace std;

namespace docs {

static string quote(const string &s) {
    return "\"" + s + "\"";
}

JsonPrinter::JsonPrinter(ostream &out)
    : DocPrinter(out),
      level(0) {
}

void JsonPrinter::print_synopsis(const DocStruct &) {
}

void JsonPrinter::print(const string &s) const {
    assert(level >= 0);
    for (int i = 0; i < level; ++i) {
        os << indent;
    }
    os << s << endl;
}

void JsonPrinter::print_key_value_pair(const string &key, const string &value) const {
    print(quote(key) + ": " + quote(value) + ",");
}

void JsonPrinter::print_arg(const ArgumentInfo &arg) {
    print(quote(arg.kwd) + ": {");
    ++level;
    print_key_value_pair("type_name", arg.type_name);
    print_key_value_pair("default_value", arg.default_value);
    --level;
    print("}");
}

void JsonPrinter::print_usage(string plugin, const DocStruct &info) {
    if (plugin.empty() || info.type == "AbstractTask" || info.type == "ScalarEvaluator")
        return;
    print(quote(plugin) + ": {");
    ++level;
    print_key_value_pair("type", info.type);
    print(quote("args") + ": {");
    ++level;
    for (auto &arg : info.arg_help) {
        print_arg(arg);
    }
    --level;
    print("}");
    --level;
    print("},");
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
    level = 0;
    print("{");
    ++level;
    DocPrinter::print_all();
    --level;
    print("}");
}

}
