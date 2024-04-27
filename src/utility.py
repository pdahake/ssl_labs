from datetime import datetime
import logging
from jinja2 import Environment, FileSystemLoader

def setup_logger(logger_name:str)->logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def convert_to_datetime(milliseconds):
    # Convert milliseconds to seconds
    seconds = milliseconds / 1000.0   
    # Convert UTC datetime to local datetime
    local_dt_object = datetime.fromtimestamp(seconds)
    return local_dt_object

"""
Use jinja template to format the output report
"""
def generate_report(api_response:dict) -> str:
    # Preprocess data before rendering the template
    for cert in api_response['certs']:
        cert['expires'] = convert_to_datetime(cert['notAfter'])

    # Load Jinja template from file system
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.jinja')

    # Render template with API response data
    rendered_template = template.render(data=api_response)
    return rendered_template

"""
Save the json file results and the html file results to disk
"""
def save_results(results:dict, hostname:str, logger:logging.Logger, report_path:str):
    if results['status'] == 'READY':
        html_report = generate_report(results)
        # Save rendered template to a file
        filename = f'{report_path}/report-{datetime.now().strftime("%Y%m%d-%H%M%S")}.html' 
        with open(filename, 'w') as f:
            f.write(html_report)

        logger.info(f"Report file {filename} created successfuly")
    else:
        logger.info(f"Scan for {hostname} is still in progress")