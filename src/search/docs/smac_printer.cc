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

string SmacPrinter::get_heuristic(const string &nick) const {
    return "heuristic" + separator + nick;
}

string SmacPrinter::get_category(const string &type) const {
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

void SmacPrinter::print_condition(const string &child,
                                  const string &parent,
                                  string condition) const {
    if (condition.empty())
        condition = parent + " == " + on;
    os << child << " | " << condition << endl;
}

void SmacPrinter::print_helper_parameter(
    const string &parent, const string& child, const string &type,
    const string &range, const string &default_value, const string &condition) const {
    string param = parent + separator + child;
    os << param << " " << type << " " << range << " [" << default_value << "]" << endl;
    print_condition(param, parent, condition);
}

void SmacPrinter::print_weight(const string &parent, bool mixed) const {
    string weight_param = parent + separator + "weight";
    os << weight_param << " ";
    if (mixed) {
        os << "real [0.1, 20] [1]";
    } else {
        os << "integer [1, 10] [1]";
    }
    os << endl;
    print_condition(weight_param, parent);
}

void SmacPrinter::print_heuristic_helper_parameters(const string &heuristic_parameter) const {
    // Add heuristic to search engine's preferred list.
    string preferred_param = heuristic_parameter + separator + "preferred";
    print_bool(preferred_param);
    print_condition(preferred_param, heuristic_parameter);

    // Use heuristic for (weighted) estimates.
    string single_param = heuristic_parameter + separator + "single";
    os << single_param << " categorical " << open_list_options << " [both]" << endl;
    print_condition(single_param, heuristic_parameter);
    print_weight(single_param, false);

    // Use heuristic in linear combination or pareto open list.
    for (string &open_list : vector<string>({lc, "pareto"})) {
        string use_in_open_list_param = heuristic_parameter + separator + open_list;
        print_bool(use_in_open_list_param);
        print_condition(use_in_open_list_param, heuristic_parameter);

        print_weight(use_in_open_list_param, false);
    }
}

void SmacPrinter::print_bool(const string &parameter) const {
    os << parameter << " categorical " << bool_range << " [" << off << "]" << endl;
}

void SmacPrinter::print_usage(string plugin, const DocStruct &info) {
    if (plugin.empty() || info.type == "AbstractTask" || info.type == "ScalarEvaluator")
        return;
    string feature = get_category(info.type) + separator + plugin;
    if (info.type == "Heuristic") {
        print_bool(feature);
        print_heuristic_helper_parameters(feature);
    } else if (info.type == "OpenList") {
        // We add parameters for choosing open lists elsewhere.
    } else if (info.type == "SearchEngine") {
        searches.push_back(feature);
    } else if (info.type == "LandmarkGraph") {
        print_bool(feature);
        print_condition(feature, get_heuristic("lmcount"));
    } else if (info.type == "Synergy") {
        print_bool(feature);
        print_condition(feature, "",
            get_heuristic("ff") + " == " + on + " && " +
            get_heuristic("lmcount") + " == " + on);
    }

    for (const ArgumentInfo &arg : info.arg_help) {
        if (arg.default_value == "<none>") {
            if (arg.type_name.compare("AbstractTask"))
                cerr << "Optional: " << arg.type_name << endl;
            continue;
        }
        string parameter = feature + separator + arg.kwd;
        print_parameter(parameter, arg);
        print_condition(parameter, feature);
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
    os << "} [TODO]" << endl << endl;

    // Additional open lists.
    vector<string> open_lists = {lc, "pareto"};

    for (auto &open_list : open_lists) {
        string open_list_param = "openlist" + separator + open_list;
        os << open_list_param << " " << open_list_options << " [" << off << "]" << endl;

        string open_list_g = open_list_param + separator + "g";
        print_bool(open_list_g);
        print_condition(open_list_g, open_list_param);

        print_weight(open_list_g, false);
        os << endl;
    }
}

}
