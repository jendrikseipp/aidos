#ifndef OPERATOR_COST_H
#define OPERATOR_COST_H

class GlobalOperator;

namespace options {
class OptionParser;
}

enum OperatorCost {NORMAL = 0, ONE = 1, PLUSONE = 2, ZERO = 3, MAX_OPERATOR_COST};

int get_adjusted_action_cost(int cost, OperatorCost cost_type);
int get_adjusted_action_cost(const GlobalOperator &op, OperatorCost cost_type);
void add_cost_type_option_to_parser(options::OptionParser &parser);

#endif
