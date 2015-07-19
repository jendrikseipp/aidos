#ifndef DOCS_SMAC_PRINTER_H
#define DOCS_SMAC_PRINTER_H

#include "../option_parser_util.h"

namespace docs {

class SmacPrinter : public DocPrinter {
    const std::string separator = ":";
    const std::string lc = "linear_combination";
    const std::string open_list_options = "{off, all_ops, pref_ops, both}";
    const std::string range_off_on = "{off, on}";
    std::vector<std::string> searches;

    std::string get_category(const std::string &type) const;
    std::string get_heuristic(const std::string &nick) const;
    void print_bool(const std::string &parameter) const;
    void print_parameter(const std::string &parameter, const ArgumentInfo &arg);
    void print_condition(const std::string &child,
                         const std::string &parent,
                         std::string condition = "") const;
    void print_helper_parameter(
        const std::string &parent, const std::string &child,
        const std::string &type, const std::string &range,
        const std::string &default_value, const std::string &condition) const;

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
    SmacPrinter(std::ostream &out);
    virtual ~SmacPrinter() override = default;
};

}

#endif
