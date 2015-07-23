#ifndef DOCS_JSON_PRINTER_H
#define DOCS_JSON_PRINTER_H

#include "../option_parser_util.h"

#include "../ext/jzon/Jzon.h"

namespace docs {
class JsonPrinter : public DocPrinter {
    Jzon::Node doc;

    Jzon::Node get_arg_node(const ArgumentInfo &arg) const;

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
