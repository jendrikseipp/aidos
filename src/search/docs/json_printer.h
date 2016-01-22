#ifndef DOCS_JSON_PRINTER_H
#define DOCS_JSON_PRINTER_H

#include "../options/doc_printer.h"

#include "../ext/jzon/Jzon.h"

namespace options {
struct ArgumentInfo;
struct DocStruct;
}

using options::DocStruct;

namespace docs {
class JsonPrinter : public options::DocPrinter {
    Jzon::Node doc;
    Jzon::Node plugin_node;

    Jzon::Node get_arg_node(const options::ArgumentInfo &arg) const;

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
