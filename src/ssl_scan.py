from api import *
import argparse
import utility
import os

if __name__ == "__main__":
    # Create logger instance
    logger = utility.setup_logger("SSLlabsApiClient")

    # this is the default folder where the report is going to be dumped.
    # make sure to pass REPORT_PATH as env variable which matchs the volume mount name
    report_path = os.getenv("REPORT_PATH", ".")
    try:
        parser = argparse.ArgumentParser(description="SSLLabs cert scanner")
        parser.add_argument("-a", "--action", type=str, default="analyze", choices=['analyze', 'register'], help="which command to execute.")
        parser.add_argument("-n", "--hostname", type=str, default="www.elliottmgmt.com", help="Hostname to check")
        parser.add_argument("-e", "--email", type=str, required=True, help="Email address to use to fetch data")
        parser.add_argument("-f", "--first_name", type=str, default="", help="First Name of user to register for API access")
        parser.add_argument("-l", "--last_name", type=str, default="",  help="Last Name of user to register for API access")
        parser.add_argument("-o", "--organization", type=str, default="",  help="Organization of user to register for API access")
        
        args = parser.parse_args()

        action = args.action
        hostname = args.hostname
        email = args.email
        fName = args.first_name
        lName = args.last_name
        org = args.organization
       
        # Create an instance of SSLlabsApiClient with the base URL
        api_client = SSLlabsApiClient(logger, "https://api.ssllabs.com/api/v4", email)

        # # Check API availability
        if api_client.is_api_available():
            # Register for API (provide your email, first_name, last_name, org name)
            if action == "register":
                api_client.register(firstName=fName, lastName=lName, email=email, organization=org)

            if action == "analyze":
                results = api_client.get_ssl_scan_results(hostname)
                if results:
                    utility.save_results(results, hostname, logger, report_path)
                else:
                    logger.error("No results generated")
    except Exception as e:
        logger.error(e)
    finally:
        logger.info("Exiting program")