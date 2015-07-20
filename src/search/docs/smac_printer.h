#ifndef DOCS_SMAC_PRINTER_H
#define DOCS_SMAC_PRINTER_H

#include "../option_parser_util.h"

namespace docs {

class SmacPrinter : public DocPrinter {
    const std::string separator = ":";
    const std::string lc = "linear_combination";
    const std::string on = "true";
    const std::string off = "false";
    const std::string open_list_options = "{" + off + ", all_ops, pref_ops, both}";
    const std::string bool_range = "{" + off + ", " + on + "}";

    std::string get_category(const std::string &type) const;
    std::string get_heuristic(const std::string &nick) const;
    void print_bool(const std::string &parameter) const;
    void print_parameter(const std::string &parameter, const std::string &feature, const ArgumentInfo &arg);
    void print_condition(const std::string &child,
                         const std::string &parent,
                         std::string condition = "") const;
    void print_weight(const std::string &parent, bool mixed) const;
    void print_helper_parameter(
        const std::string &parent, const std::string &child,
        const std::string &type, const std::string &range,
        const std::string &default_value, const std::string &condition) const;
    void print_heuristic_helper_parameters(const std::string &heuristic_parameter) const;

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
