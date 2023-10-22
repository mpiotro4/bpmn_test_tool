def generate_feature(filename, all_paths):
    with open(filename, "w") as file:
        for index, path in enumerate(all_paths):
            generate_test_case(file, path, index)


def generate_test_case(file, path, index):
    file.write(f"Scenario: scenario {index}\n")
    for index, node in enumerate(path):
        generate_prefix(index, file)
        generate_step(node, file)
    # file.write("\n".join(node.name for node in path))
    file.write("\n")


def generate_step(node, file):
    file.write(node.name)
    if node.decision_var is not None:
        if node.decision_var_val is not None:
            file.write(f" {node.decision_var} = {node.decision_var_val} ")
        else:
            file.write(f" {node.decision_var} = ? ")

    file.write("\n")


def generate_prefix(index, file):
    if index == 0:
        file.write("Given ")
    if (index + 1) % 2 == 0:
        file.write("When ")
    else:
        file.write("Then ")


class FeatureGenerator:
    pass
