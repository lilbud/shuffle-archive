from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class BadBoldRule(RulePlugin):
    """Find lines starting with ** but missing ending **."""

    def get_details(self) -> PluginDetails:
        """Define metadata that PyMarkdown reads to register the plugin."""
        return PluginDetails(
            plugin_id="PML102",
            plugin_name="fix-broken-bold",
            plugin_description="Finds and fixes lines starting with ** but missing ending **",
            plugin_version="0.1.0",
            plugin_interface_version=1,
            plugin_url=None,
        )

    def initialize_from_config(self):
        pass

    def next_line(self, line_context, line_text):
        """Look for raw text lines matching your criteria."""
        stripped = line_text.strip()
        if stripped.startswith("**") and not stripped.endswith("**"):
            # Calculate the line index (1-based)
            line_number = line_context.line_number

            # Formulate the automated text fix
            fixed_text = f"{line_text.rstrip()}**\n"

            # Report the error and attach the fix string back to PyMarkdown
            self.report_next_line_error(
                context=line_context,
                line_number=line_number,
                column_number=1,
                error_description="Line starts with bold markers but doesn't close them.",
                fix_action=fixed_text,
            )
