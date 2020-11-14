import json

# Indentation and spacing
indent_size = 4
indent_style = 'space'
tab_width = 4

# New line preferences
#end_of_line = 'crlf'
insert_final_newline = False

#### .NET Coding Conventions ####

# Organize usings
dotnet_separate_import_directive_groups = False
dotnet_sort_system_directives_first = False
#file_header_template = None

#### C# Formatting Rules ####

# New line preferences
csharp_new_line_before_catch = True
csharp_new_line_before_else = True
csharp_new_line_before_finally = True
csharp_new_line_before_members_in_anonymous_types = True
csharp_new_line_before_members_in_object_initializers = True
csharp_new_line_before_open_brace = True
csharp_new_line_between_query_expression_clauses = True

# Indentation preferences
csharp_indent_block_contents = 1
csharp_indent_braces = 0
csharp_indent_case_contents = 1
csharp_indent_case_contents_when_block = 0
csharp_indent_labels = 'flush_left' # 'no_change' 'one_less_than_current' 'flush_left'
csharp_indent_switch_labels = 1

# Space preferences
csharp_space_after_cast = False
csharp_space_after_colon_in_inheritance_clause = True
csharp_space_after_comma = True
csharp_space_after_dot = False
csharp_space_after_keywords_in_control_flow_statements = True
csharp_space_after_semicolon_in_for_statement = True
csharp_space_around_binary_operators = True
csharp_space_around_declaration_statements = False
csharp_space_before_colon_in_inheritance_clause = True
csharp_space_before_comma = False
csharp_space_before_dot = False
csharp_space_before_semicolon_in_for_statement = False
csharp_space_before_open_square_brackets = False
csharp_space_between_empty_square_brackets = False
csharp_space_between_square_brackets = True
csharp_space_between_method_call_empty_parameter_list_parentheses = False
csharp_space_between_method_call_name_and_opening_parenthesis = False
csharp_space_between_method_call_parameter_list_parentheses = False
csharp_space_between_method_declaration_empty_parameter_list_parentheses = False
csharp_space_between_method_declaration_name_and_open_parenthesis = False
csharp_space_between_method_declaration_parameter_list_parentheses = False
csharp_space_between_parentheses = True

# Wrapping preferences
csharp_preserve_single_line_blocks = True
csharp_preserve_single_line_statements = True

def parse_template(template_path):
	if not template_path.endswith('.json'):
		print("template file must be in .json format. skipping...")
		return
	with open(template_path, 'r') as file:
		config = json.load(file)
		settings = config['settings']
		indent_size = settings['indent_size']
		tab_width = settings['tab_width']
		insert_final_newline = settings['insert_final_newline']

		#### .NET Coding Conventions ####

		# Organize usings
		#dotnet_separate_import_directive_groups = settings['dotnet_separate_import_directive_groups']
		#dotnet_sort_system_directives_first = settings['dotnet_sort_system_directives_first']
		#file_header_template = None

		#### C# Formatting Rules ####

		# New line preferences
		csharp_new_line_before_catch = settings['csharp_new_line_before_catch']
		csharp_new_line_before_else = settings['csharp_new_line_before_else']
		csharp_new_line_before_finally = settings['csharp_new_line_before_finally']
		csharp_new_line_before_members_in_anonymous_types = settings['csharp_new_line_before_members_in_anonymous_types']
		csharp_new_line_before_members_in_object_initializers = settings['csharp_new_line_before_members_in_object_initializers']
		csharp_new_line_before_open_brace = settings['csharp_new_line_before_open_brace']
		csharp_new_line_between_query_expression_clauses = settings['csharp_new_line_between_query_expression_clauses']

		# Indentation preferences
		csharp_indent_block_contents = settings['csharp_indent_block_contents']
		csharp_indent_braces = settings['csharp_indent_braces']
		csharp_indent_case_contents = settings['csharp_indent_case_contents']
		csharp_indent_case_contents_when_block = settings['csharp_indent_case_contents_when_block']
		csharp_indent_labels = settings['csharp_indent_labels']
		csharp_indent_switch_labels = settings['csharp_indent_switch_labels']

		# Space preferences
		csharp_space_after_cast = settings['csharp_space_after_cast']
		csharp_space_after_colon_in_inheritance_clause = settings['csharp_space_after_colon_in_inheritance_clause']
		csharp_space_after_comma = settings['csharp_space_after_comma']
		csharp_space_after_dot = settings['csharp_space_after_dot']
		csharp_space_after_keywords_in_control_flow_statements = settings['csharp_space_after_keywords_in_control_flow_statements']
		csharp_space_after_semicolon_in_for_statement = settings['csharp_space_after_semicolon_in_for_statement']
		csharp_space_around_binary_operators = settings['csharp_space_around_binary_operators']
		csharp_space_around_declaration_statements = settings['csharp_space_around_declaration_statements']
		csharp_space_before_colon_in_inheritance_clause = settings['csharp_space_before_colon_in_inheritance_clause']
		csharp_space_before_comma = settings['csharp_space_before_comma']
		csharp_space_before_dot = settings['csharp_space_before_dot']
		csharp_space_before_semicolon_in_for_statement = settings['csharp_space_before_semicolon_in_for_statement']
		csharp_space_before_open_square_brackets = settings['csharp_space_before_open_square_brackets']
		csharp_space_between_empty_square_brackets = settings['csharp_space_between_empty_square_brackets']
		csharp_space_between_square_brackets = settings['csharp_space_between_square_brackets']
		csharp_space_between_method_call_empty_parameter_list_parentheses = settings['csharp_space_between_method_call_empty_parameter_list_parentheses']
		csharp_space_between_method_call_name_and_opening_parenthesis = settings['csharp_space_between_method_call_name_and_opening_parenthesis']
		csharp_space_between_method_call_parameter_list_parentheses = settings['csharp_space_between_method_call_parameter_list_parentheses']
		csharp_space_between_method_declaration_empty_parameter_list_parentheses = settings['csharp_space_between_method_declaration_empty_parameter_list_parentheses']
		csharp_space_between_method_declaration_name_and_open_parenthesis = settings['csharp_space_between_method_declaration_name_and_open_parenthesis']
		csharp_space_between_method_declaration_parameter_list_parentheses = settings['csharp_space_between_method_declaration_parameter_list_parentheses']
		csharp_space_between_parentheses = settings['csharp_space_between_parentheses']

		# Wrapping preferences
		csharp_preserve_single_line_blocks = settings['csharp_preserve_single_line_blocks']
		csharp_preserve_single_line_statements = settings['csharp_preserve_single_line_statements']