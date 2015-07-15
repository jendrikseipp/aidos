#include "option_parser_util.h"

#include <algorithm>
#include <string>
#include <vector>

using namespace std;

string lowercase(string s) {
    transform(s.begin(), s.end(), s.begin(), ::tolower);
    return s;
}

void DocStore::register_object(string k, string type) {
    k = lowercase(k);
    registered[k] = DocStruct();
    registered[k].type = type;
    registered[k].full_name = k;
    registered[k].synopsis = "";
}


void DocStore::add_arg(string k,
                       string arg_name,
                       string help,
                       string type,
                       string default_value,
                       bool mandatory,
                       ValueExplanations value_explanations) {
    registered[k].arg_help.push_back(
        ArgumentInfo(arg_name, help, type, default_value, mandatory,
                     value_explanations));
}

void DocStore::add_value_explanations(string k,
                                      string arg_name,
                                      ValueExplanations value_explanations) {
    vector<ArgumentInfo> &args = registered[k].arg_help;
    for (size_t i = 0; i < args.size(); ++i) {
        if (args[i].kwd.compare(arg_name) == 0) {
            args[i].value_explanations = value_explanations;
            break;
        }
    }
}


void DocStore::set_synopsis(string k,
                            string name, string description) {
    registered[k].full_name = name;
    registered[k].synopsis = description;
}

void DocStore::add_property(string k,
                            string name, string description) {
    registered[k].property_help.push_back(PropertyInfo(name, description));
}

void DocStore::add_feature(string k,
                           string feature, string description) {
    registered[k].support_help.push_back(LanguageSupportInfo(feature,
                                                             description));
}

void DocStore::add_note(string k,
                        string name, string description, bool long_text) {
    registered[k].notes.push_back(NoteInfo(name, description, long_text));
}

void DocStore::hide(std::string k) {
    registered[k].hidden = true;
}


bool DocStore::contains(string k) {
    return registered.find(k) != registered.end();
}

DocStruct DocStore::get(string k) {
    return registered[k];
}

vector<string> DocStore::get_keys() {
    vector<string> keys;
    for (map<string, DocStruct>::iterator it =
             registered.begin();
         it != registered.end(); ++it) {
        keys.push_back(it->first);
    }
    return keys;
}

vector<string> DocStore::get_types() {
    vector<string> types;
    for (map<string, DocStruct>::iterator it =
             registered.begin();
         it != registered.end(); ++it) {
        if (find(types.begin(), types.end(), it->second.type)
            == types.end()) {
            types.push_back(it->second.type);
        }
    }
    return types;
}


DocPrinter::DocPrinter(ostream &out)
    : os(out) {
}

DocPrinter::~DocPrinter() {
}


void DocPrinter::print_all() {
    DocStore *ds = DocStore::instance();
    vector<string> types = ds->get_types();
    for (size_t n = 0; n < types.size(); ++n) {
        // Entries for the category itself have an empty type
        if (!types[n].empty())
            print_category(types[n]);
    }
}

void DocPrinter::print_category(string category_name) {
    print_category_header(category_name);
    DocStore *ds = DocStore::instance();
    print_element("", ds->get(category_name));
    vector<string> keys = ds->get_keys();
    for (size_t i = 0; i < keys.size(); ++i) {
        DocStruct info = ds->get(keys[i]);
        if (info.type.compare(category_name) != 0
            || info.hidden)
            continue;
        print_element(keys[i], info);
    }
    print_category_footer();
}

void DocPrinter::print_element(string call_name, const DocStruct &info) {
    print_synopsis(info);
    print_usage(call_name, info);
    print_arguments(info);
    print_notes(info);
    print_language_features(info);
    print_properties(info);
}

Txt2TagsPrinter::Txt2TagsPrinter(ostream &out)
    : DocPrinter(out) {
}

Txt2TagsPrinter::~Txt2TagsPrinter() {
}

void Txt2TagsPrinter::print_synopsis(const DocStruct &info) {
    if (!info.full_name.empty())
        os << "== " << info.full_name << " ==" << endl;
    if (!info.synopsis.empty())
        os << info.synopsis << endl;
}

void Txt2TagsPrinter::print_usage(string call_name, const DocStruct &info) {
    if (!call_name.empty()) {
        os << "``` " << call_name << "(";
        for (size_t i = 0; i < info.arg_help.size(); ++i) {
            ArgumentInfo arg = info.arg_help[i];
            os << arg.kwd;
            if (!info.arg_help[i].default_value.empty()) {
                os << "=" << info.arg_help[i].default_value;
            } else if (!info.arg_help[i].mandatory) {
                os << "=None";
            }
            if (i != info.arg_help.size() - 1)
                os << ", ";
        }
        os << ")" << endl << endl << endl;
    }
}

static bool is_call(string s) {
    return s.find("(") != string::npos;
}

void Txt2TagsPrinter::print_arguments(const DocStruct &info) {
    for (size_t i = 0; i < info.arg_help.size(); ++i) {
        ArgumentInfo arg = info.arg_help[i];
        os << "- //" << arg.kwd << "// ("
           << arg.type_name << "): "
           << arg.help << endl;
        if (!arg.value_explanations.empty()) {
            for (size_t j = 0; j < arg.value_explanations.size(); ++j) {
                pair<string, string> explanation =
                    arg.value_explanations[j];
                if (is_call(explanation.first)) {
                    os << endl << "```" << endl << explanation.first << endl << "```" << endl
                       << " " << explanation.second << endl;
                } else {
                    os << " - ``" << explanation.first << "``: "
                       << explanation.second << endl;
                }
            }
        }
    }
}

void Txt2TagsPrinter::print_notes(const DocStruct &info) {
    for (size_t i = 0; i < info.notes.size(); ++i) {
        NoteInfo note = info.notes[i];
        if (note.long_text) {
            os << "=== " << note.name << " ===" << endl
               << note.description << endl << endl;
        } else {
            os << "**" << note.name << ":** " << note.description << endl << endl;
        }
    }
}

void Txt2TagsPrinter::print_language_features(const DocStruct &info) {
    if (!info.support_help.empty()) {
        os << "Language features supported:" << endl;
    }
    for (size_t i = 0; i < info.support_help.size(); ++i) {
        LanguageSupportInfo ls = info.support_help[i];
        os << "- **" << ls.feature << ":** " << ls.description << endl;
    }
}

void Txt2TagsPrinter::print_properties(const DocStruct &info) {
    if (!info.property_help.empty()) {
        os << "Properties:" << endl;
    }
    for (size_t i = 0; i < info.property_help.size(); ++i) {
        PropertyInfo p = info.property_help[i];
        os << "- **" << p.property << ":** " << p.description << endl;
    }
}


void Txt2TagsPrinter::print_category_header(string category_name) {
    os << ">>>>CATEGORY: " << category_name << "<<<<" << endl;
}

void Txt2TagsPrinter::print_category_footer() {
    os << endl
       << ">>>>CATEGORYEND<<<<" << endl;
}

PlainPrinter::PlainPrinter(ostream &out, bool pa)
    : DocPrinter(out),
      print_all(pa) {
}

void PlainPrinter::print_synopsis(const DocStruct &info) {
    if (!info.full_name.empty())
        os << "== " << info.full_name << " ==" << endl;
    if (print_all && !info.synopsis.empty()) {
        os << info.synopsis << endl;
    }
}

void PlainPrinter::print_usage(string call_name, const DocStruct &info) {
    if (!call_name.empty()) {
        os << call_name << "(";
        string sep = "";
        for (const ArgumentInfo &arg : info.arg_help) {
            os << sep;
            os << arg.kwd;
            if (!arg.default_value.empty()) {
                os << "=" << arg.default_value;
            } else if (!arg.mandatory) {
                os << "=None";
            }
            sep = ", ";
        }
        os << ")" << endl;
    }
}

void PlainPrinter::print_arguments(const DocStruct &info) {
    for (const ArgumentInfo &arg : info.arg_help) {
        os << " " << arg.kwd << "("
           << arg.type_name << "): "
           << arg.help << endl;
    }
}

void PlainPrinter::print_notes(const DocStruct &info) {
    if (print_all) {
        for (size_t i = 0; i < info.notes.size(); ++i) {
            NoteInfo note = info.notes[i];
            if (note.long_text) {
                os << "=== " << note.name << " ===" << endl
                   << note.description << endl << endl;
            } else {
                os << " * " << note.name << ": " << note.description << endl << endl;
            }
        }
    }
}

void PlainPrinter::print_language_features(const DocStruct &info) {
    if (print_all) {
        if (!info.support_help.empty()) {
            os << "Language features supported:" << endl;
        }
        for (size_t i = 0; i < info.support_help.size(); ++i) {
            LanguageSupportInfo ls = info.support_help[i];
            os << " * " << ls.feature << ": " << ls.description << endl;
        }
    }
}

void PlainPrinter::print_properties(const DocStruct &info) {
    if (print_all) {
        if (!info.property_help.empty()) {
            os << "Properties:" << endl;
        }
        for (size_t i = 0; i < info.property_help.size(); ++i) {
            PropertyInfo p = info.property_help[i];
            os << " * " << p.property << ": " << p.description << endl;
        }
    }
}


void PlainPrinter::print_category_header(string category_name) {
    os << "Help for " << category_name << endl << endl;
}

void PlainPrinter::print_category_footer() {
    os << endl;
}


SmacPrinter::SmacPrinter(ostream &out)
    : DocPrinter(out) {
}

void SmacPrinter::print_synopsis(const DocStruct &info) {
    if (!info.full_name.empty())
        os << "== " << info.full_name << " ==" << endl;
}

void SmacPrinter::print_usage(string call_name, const DocStruct &) {
    current_call_name = call_name;
}

void SmacPrinter::print_arguments(const DocStruct &info) {
    for (const ArgumentInfo &arg : info.arg_help) {
        if (!arg.mandatory) {
            assert(!arg.type_name.compare("AbstractTask"));
            continue;
        }

        string type;
        string domain;
        if (!arg.type_name.compare("int")) {
            type = "integer";
            domain = "[TODO, TODO]";
        } else if (!arg.type_name.compare("double")) {
            type = "real";
            domain = "[TODO, TODO]";
        } else if (!arg.type_name.compare("bool")) {
            type = "categorical";
            domain = "{false, true}";
        } else if (!arg.type_name.compare(0, 1, "{")) {
            type = "categorical";
            // Keep curly braces.
            domain = lowercase(arg.type_name);
        } else {
            os << "Unrecognized type: " << arg.type_name << endl;
            continue;
            //ABORT("Unrecognized type: " + arg.type_name);
        }

        assert(!arg.default_value.empty());
        os << current_call_name << separator << arg.kwd << " "
           << type << " " << domain << " ["
           << lowercase(arg.default_value) << "]" << endl;
    }
}

void SmacPrinter::print_notes(const DocStruct &) {
}

void SmacPrinter::print_language_features(const DocStruct &) {
}

void SmacPrinter::print_properties(const DocStruct &) {
}


void SmacPrinter::print_category_header(string category_name) {
    os << "Help for " << category_name << endl << endl;
}

void SmacPrinter::print_category_footer() {
    os << endl;
}
