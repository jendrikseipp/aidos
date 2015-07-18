#include "smac_printer.h"

using namespace std;

namespace docs {

SmacPrinter::SmacPrinter(ostream &out)
    : DocPrinter(out) {
}

void SmacPrinter::print_synopsis(const DocStruct &info) {
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

string SmacPrinter::get_category(const string &type) const {
    if (type == "Heuristic") {
        return "heuristic";
    } else if (type == "LandmarkGraph") {
        return "landmarks";
    } else if (type == "SearchEngine") {
        return "search";
    } else if (type == "Synergy") {
        return "synergy"; // TODO: Return "heuristic"?
    } else {
        ABORT("Unknown type: " + type);
    }
}

void SmacPrinter::print_parameter(const string &parameter, const ArgumentInfo &arg) {
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
}

void SmacPrinter::print_condition(const string &feature,
                                  const string &type,
                                  const string &parameter) {
    if (type == "Heuristic") {
        os << parameter << " | " << feature << " != off" << endl;
    } else if (type == "SearchEngine") {
        os << parameter << " | search == " << feature << endl;
    } else {
        os << parameter << " | " << feature << " == on" << endl;
    }
}

void SmacPrinter::print_usage(string plugin, const DocStruct &info) {
    if (plugin.empty())
        return;
    string feature = get_category(info.type) + separator + plugin;
    if (info.type == "Heuristic") {
        os << feature
           << " categorical {off, on} [off]" << endl;
        string pref_ops_param = feature + separator + "use_preferred_operators";
        os << pref_ops_param << " categorical {true, false} [false]" << endl;
        os << pref_ops_param << " | " << feature << " != off" << endl;
    } else if (info.type == "SearchEngine") {
        searches.push_back(feature);
    } else if (info.type == "LandmarkGraph") {
        os << feature << " categorical {off, on} [off]" << endl;
        os << feature << " | heuristic" << separator << "lmcount == on" << endl;
    } else if (info.type == "Synergy") {
        os << feature << " categorical {off, on} [off]" << endl;
        os << feature << " | ff != off && lmcount != off" << endl;
    }

    for (const ArgumentInfo &arg : info.arg_help) {
        if (arg.default_value == "<none>") {
            if (arg.type_name.compare("AbstractTask"))
                cerr << "Optional: " << arg.type_name << endl;
            continue;
        }
        string parameter = feature + separator + arg.kwd;
        print_parameter(parameter, arg);
        print_condition(feature, info.type, parameter);
    }
}

void SmacPrinter::print_arguments(const DocStruct &) {
}

void SmacPrinter::print_notes(const DocStruct &) {
}

void SmacPrinter::print_language_features(const DocStruct &) {
}

void SmacPrinter::print_properties(const DocStruct &) {
}

void SmacPrinter::print_category_header(string category_name) {
    os << "# Parameters for " << category_name << endl << endl;
}

void SmacPrinter::print_category_footer() {
    os << endl;
}

void SmacPrinter::print_all() {
    DocPrinter::print_all();
    os << "search categorical {";
    string sep = "";
    for (const string &search : searches) {
        os << sep << search;
        sep = ", ";
    }
    os << "} [TODO]" << endl;
}

}
