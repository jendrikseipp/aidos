#include "json_printer.h"

using namespace std;

namespace docs {

static void print_map(ostream &stream, const map<string, string> &dict) {
    stream << "{";
    string sep = "";
    for (auto &pair : dict) {
        stream << sep << "\"" << pair.first << "\": \"" << pair.second << "\"";
        sep = ", ";
    }
    stream << "}";
}

JsonPrinter::JsonPrinter(ostream &out)
    : DocPrinter(out) {
}

void JsonPrinter::print_synopsis(const DocStruct &info) {
    if (!info.full_name.empty())
        os << "# " << info.full_name << endl;
}

static string expand_infinity(const string &value) {
    const int smac_infinity = numeric_limits<int>::max();
    stringstream ss;
    if (!value.compare("infinity")) {
        ss << smac_infinity;
    } else {
        ss << value;
    }
    return ss.str();
}

static string get_upper_bound(const string &value) {
    if (!value.compare("infinity")) {
        return expand_infinity(value);
    } else {
        return "TODO";
    }
}

string JsonPrinter::get_heuristic(const string &nick) const {
    return "heuristic" + separator + nick;
}

string JsonPrinter::get_category(const string &type) const {
    if (type == "Heuristic") {
        return "heuristic";
    } else if (type == "Labels") {
        return "label_reduction";
    } else if (type == "LandmarkGraph") {
        return "landmarks";
    } else if (type == "MergeStrategy") {
        return "merge_strategy";
    } else if (type == "OpenList") {
        return "openlist";
    } else if (type == "SearchEngine") {
        return "search";
    } else if (type == "ShrinkStrategy") {
        return "shrink_strategy";
    } else if (type == "Synergy") {
        return "synergy"; // TODO: Return "heuristic"?
    } else {
        ABORT("Unknown type: " + type);
    }
}

void JsonPrinter::print_parameter(const string &parameter, const string &feature, const ArgumentInfo &arg) {
    string type;
    string domain;
    // TODO: We assume all integer and double params are >= 0.
    if (!arg.type_name.compare("int")) {
        type = "integer";
        stringstream ss;
        ss << "[0, " << get_upper_bound(arg.default_value) << "]";
        domain = ss.str();
    } else if (!arg.type_name.compare("double")) {
        type = "real";
        stringstream ss;
        ss << "[0.0, " << get_upper_bound(arg.default_value) << "]";
        domain = ss.str();
    } else if (!arg.type_name.compare("bool")) {
        type = "categorical";
        domain = "{false, true}";
    } else if (!arg.type_name.compare(0, 1, "{")) {
        type = "categorical";
        // Keep curly braces.
        domain = lowercase(arg.type_name);
    } else {
        cerr << "Unrecognized type: " << arg.type_name << endl;
        return;
    }

    os << parameter << " " << type << " " << domain << " ["
       << lowercase(expand_infinity(arg.default_value))
       << "]" << endl;
    print_condition(parameter, feature);
}

void JsonPrinter::print_condition(const string &child,
                                  const string &parent,
                                  string condition) const {
    if (condition.empty())
        condition = parent + " != " + off;
    os << child << " | " << condition << endl;
}

void JsonPrinter::print_bool(const string &parameter) const {
    os << parameter << " categorical " << bool_range << " [" << off << "]" << endl;
}

void JsonPrinter::print_usage(string plugin, const DocStruct &info) {
    if (plugin.empty() || info.type == "AbstractTask" || info.type == "ScalarEvaluator")
        return;
    map<string, string> param_map;
    types[info.type] = param_map;
}

void JsonPrinter::print_arguments(const DocStruct &) {
}

void JsonPrinter::print_notes(const DocStruct &) {
}

void JsonPrinter::print_language_features(const DocStruct &) {
}

void JsonPrinter::print_properties(const DocStruct &) {
}

void JsonPrinter::print_category_header(string category_name) {
    os << "# Parameters for " << category_name << endl << endl;
}

void JsonPrinter::print_category_footer() {
    os << endl;
}

void JsonPrinter::print_all() {
    DocPrinter::print_all();
    for (auto &pair : types) {
        const string &type = pair.first;
        os << type << endl;
        const auto &param_map = pair.second;
        print_map(os, param_map);
    }
}

}
