#ifndef DOCS_JSON_PRINTER_H
#define DOCS_JSON_PRINTER_H

#include "../option_parser_util.h"

#include "../ext/jzon/Jzon.h"


namespace docs {
class JsonPrinter : public DocPrinter {
    Jzon::Node doc;
    Jzon::Node plugin_node;

    Jzon::Node get_arg_node(const ArgumentInfo &arg) const;

protected:
    virtual void print_synopsis(const DocStruct &info) override;
    virtual void print_usage(std::string plugin, const DocStruct &info) override;
    virtual void print_arguments(const DocStruct &info) override;
    virtual void print_notes(const DocStruct &info) override;
    virtual void print_language_features(const DocStruct &info) override;
    virtual void print_properties(const DocStruct &info) override;
    virtual void print_category_header(std::string category_name) override;
    virtual void print_category_footer() override;

public:
    JsonPrinter(std::ostream &out);
    virtual ~JsonPrinter() override = default;

    virtual void print_element(std::string plugin, const DocStruct &info) override;
    virtual void print_all() override;
};
}

#endif
