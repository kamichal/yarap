import os

def get_output_file_path(file_name):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    sphinx_static_dir = os.path.join(os.path.dirname(this_dir), "source", "_static")
    output_file_path = os.path.join(sphinx_static_dir, file_name)
    return output_file_path
