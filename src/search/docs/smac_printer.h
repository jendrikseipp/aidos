#ifndef DOCS_SMAC_PRINTER_H
#define DOCS_SMAC_PRINTER_H

#include "../option_parser_util.h"

namespace docs {

class SmacPrinter : public DocPrinter {
    const std::string separator = ":";

protected:
    virtual void print_synopsis(const DocStruct &info);
    virtual void print_usage(std::string feature, const DocStruct &info);
    virtual void print_arguments(const DocStruct &info);
    virtual void print_notes(const DocStruct &info);
    virtual void print_language_features(const DocStruct &info);
    virtual void print_properties(const DocStruct &info);
    virtual void print_category_header(std::string category_name);
    virtual void print_category_footer();

public:
    SmacPrinter(std::ostream &out);
    virtual ~SmacPrinter() override = default;
};

}

#endif
