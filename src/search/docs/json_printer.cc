#include "json_printer.h"

using namespace std;

namespace docs {
JsonPrinter::JsonPrinter(ostream &out)
    : DocPrinter(out),
      doc(Jzon::object()) {
}

void JsonPrinter::print_synopsis(const DocStruct &) {
}

Jzon::Node JsonPrinter::get_arg_node(const ArgumentInfo &arg) const {
    Jzon::Node node = Jzon::object();
    node.add("type_name", arg.type_name);
    node.add("default_value", arg.default_value);
    // TODO: Include help and value_explanations?
    return node;
}

void JsonPrinter::print_usage(string plugin, const DocStruct &info) {
    if (plugin.empty())
        return;
    Jzon::Node plugin_node = Jzon::object();
    plugin_node.add("type", info.type);
    plugin_node.add("full_name", info.full_name);
    Jzon::Node property_help = Jzon::object();
    for (auto &prop_info : info.property_help) {
        property_help.add(prop_info.property, prop_info.description);
    }
    plugin_node.add("properties", property_help);
    // plugin_node.add("synopsis", info.synopsis);
    // TODO: Include support_help?
    Jzon::Node notes = Jzon::object();
    for (auto &note : info.notes) {
        notes.add(note.name, note.description);
    }
    plugin_node.add("notes", notes);
    Jzon::Node args_node = Jzon::object();
    for (auto &arg : info.arg_help) {
        args_node.add(arg.kwd, get_arg_node(arg));
    }
    plugin_node.add("args", args_node);
    doc.add(plugin, plugin_node);
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
}

void JsonPrinter::print_all() {
    DocPrinter::print_all();

    Jzon::Format format = {
        true, true, false, 4
    };
    Jzon::Writer writer(format);
    writer.writeStream(doc, os);
    os << endl;
}
}
