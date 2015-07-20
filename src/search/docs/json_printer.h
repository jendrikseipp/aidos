#ifndef DOCS_JSON_PRINTER_H
#define DOCS_JSON_PRINTER_H

#include "../option_parser_util.h"

#include <map>

namespace docs {

class JsonPrinter : public DocPrinter {
    const std::string separator = ":";
    const std::string on = "true";
    const std::string off = "false";
    const std::string open_list_options = "{" + off + ", all_ops, pref_ops, both}";
    const std::string bool_range = "{" + off + ", " + on + "}";

    void print_arg(const ArgumentInfo &arg) const;
    void print_key_value_pair(const std::string &key, const std::string &value) const;

protected:
    virtual void print_synopsis(const DocStruct &info);
    virtual void print_usage(std::string plugin, const DocStruct &info);
    virtual void print_arguments(const DocStruct &info);
    virtual void print_notes(const DocStruct &info);
    virtual void print_language_features(const DocStruct &info);
    virtual void print_properties(const DocStruct &info);
    virtual void print_category_header(std::string category_name);
    virtual void print_category_footer();

    virtual void print_all() override;

public:
    JsonPrinter(std::ostream &out);
    virtual ~JsonPrinter() override = default;
};

}

#endif
