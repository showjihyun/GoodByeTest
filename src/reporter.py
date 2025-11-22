
import os
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
from datetime import datetime

class Reporter:
    def __init__(self, template_dir="src/templates", output_dir="reports/history"):
        self.template_dir = template_dir
        self.output_dir = output_dir
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_report(self, data):
        """
        Generates both HTML and PDF reports.
        Returns the paths to the generated files.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html_content = self._render_html(data)
        
        html_path = os.path.join(self.output_dir, f"report_{timestamp}.html")
        pdf_path = os.path.join(self.output_dir, f"report_{timestamp}.pdf")
        
        # Save HTML
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        # Save PDF
        self._convert_html_to_pdf(html_content, pdf_path)
        
        # Update latest link (optional)
        self._update_latest_link(html_path, "latest_report.html")
        
        return html_path, pdf_path

    def _render_html(self, data):
        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template("report.html")
        return template.render(data)

    def _convert_html_to_pdf(self, source_html, output_filename):
        with open(output_filename, "w+b") as result_file:
            pisa_status = pisa.CreatePDF(
                source_html,                # the HTML to convert
                dest=result_file            # file handle to recieve result
            )
        return pisa_status.err

    def _update_latest_link(self, target_path, link_name):
        link_path = os.path.join(os.path.dirname(self.output_dir), link_name) # Save latest in reports/ root
        # On Windows, symlinks require admin, so we'll just copy for now or create a redirect html
        # Simple redirect HTML
        redirect_content = f'<html><head><meta http-equiv="refresh" content="0; url=history/{os.path.basename(target_path)}" /></head></html>'
        with open(link_path, "w") as f:
            f.write(redirect_content)
