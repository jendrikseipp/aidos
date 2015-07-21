#include "json_printer.h"

using namespace std;

namespace docs {

static string quote(string s) {
    replace(s.begin(), s.end(), '"', '\"');
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

void JsonPrinter::print_key_value_pair(const string &key, const string &value, bool is_last) const {
    string line = quote(key) + ": " + quote(value);
    if (!is_last)
        line += ",";
    print(line);
}

void JsonPrinter::print_arg(const ArgumentInfo &arg, bool is_last) {
    print(quote(arg.kwd) + ": {");
    ++level;
    print_key_value_pair("type_name", arg.type_name);
    print_key_value_pair("default_value", arg.default_value, true);
    // TODO: Include help and value_explanations? We should probably
    //       use a json library for this.
    // print_key_value_pair("help", arg.help, true);
    --level;
    if (!is_last) {
        print("},");
    } else {
        print("}");
    }
}

void JsonPrinter::print_usage(string plugin, const DocStruct &info) {
    if (plugin.empty())
        return;
    print(quote(plugin) + ": {");
    ++level;
    print_key_value_pair("type", info.type);
    print_key_value_pair("full_name", info.full_name);
    // print_key_value_pair("synopsis", info.synopsis);
    // TODO: Include property_help, support_help and notes?
    print(quote("args") + ": {");
    ++level;
    for (size_t i = 0; i < info.arg_help.size(); ++i) {
        auto &arg = info.arg_help[i];
        bool is_last = i == info.arg_help.size() - 1;
        print_arg(arg, is_last);
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
    //os << endl;
}

void JsonPrinter::print_all() {
    level = 0;
    print("{");
    ++level;
    DocPrinter::print_all();

    // Remove trailing comma.
    long pos = os.tellp();
    os.seekp(pos - 3);
    --level;
    print("}");
    ++level;

    --level;
    print("}");
}

}
