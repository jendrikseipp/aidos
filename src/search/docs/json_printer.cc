#include "json_printer.h"

using namespace std;

namespace docs {

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

void JsonPrinter::print_helper_parameter(
    const string &parent, const string& child, const string &type,
    const string &range, const string &default_value, const string &condition) const {
    string param = parent + separator + helper + child;
    os << param << " " << type << " " << range << " [" << default_value << "]" << endl;
    print_condition(param, parent, condition);
}

void JsonPrinter::print_weight(const string &parent, bool mixed) const {
    string weight_param = parent + separator + helper + "weight";
    os << weight_param << " ";
    if (mixed) {
        os << "real [0.1, 20] [1]";
    } else {
        os << "integer [1, 10] [1]";
    }
    os << endl;
    print_condition(weight_param, parent);
}

void JsonPrinter::print_heuristic_helper_parameters(const string &heuristic_parameter) const {
    // Add heuristic to search engine's preferred list.
    string preferred_param = heuristic_parameter + separator + helper + "preferred";
    print_bool(preferred_param);
    print_condition(preferred_param, heuristic_parameter);

    // Use heuristic for (weighted) estimates.
    string single_param = heuristic_parameter + separator + helper + "single";
    os << single_param << " categorical " << open_list_options << " [both]" << endl;
    print_condition(single_param, heuristic_parameter);
    print_weight(single_param, false);

    // Use heuristic for single(sum(weight(g(), gw), weight(H, w)) open lists.
    string sum_param = heuristic_parameter + separator + helper + "sum";
    os << sum_param << " categorical " << open_list_options << " [" << off << "]" << endl;
    print_condition(sum_param, heuristic_parameter);
    print_weight(sum_param, true);

    // Use heuristic for tiebreaking([sum(weight(g(), gw), weight(H, w)), H]) open lists.
    string tb_param = heuristic_parameter + separator + helper + "tiebreaking";
    os << tb_param << " categorical " << open_list_options << " [" << off << "]" << endl;
    print_condition(tb_param, heuristic_parameter);
    print_weight(tb_param, true);
    string tb_on_h_param = tb_param + separator + helper + "on_h";
    print_bool(tb_on_h_param);
    print_condition(tb_on_h_param, tb_param);

    // Use heuristic in linear combination or pareto open list.
    for (string &open_list : vector<string>({lc, "pareto"})) {
        string use_in_open_list_param = heuristic_parameter + separator + helper + open_list;
        print_bool(use_in_open_list_param);
        print_condition(use_in_open_list_param, heuristic_parameter);

        print_weight(use_in_open_list_param, false);
    }
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
        for (auto plugin : param_map) {
            const string &key = plugin.first;
            const string &value = plugin.second;
            os << key << " = " << value << endl;
        }
    }
}

}
