# NOTES:

## Build the docker image.

### Default docker build
```
docker build . -t ssl_scanner:1.0
```
```
-t is used to tag the image

Arguments which can be overridden during build:
- UID: user id of non root user 
- GID: group id of non root user
- USERNAME: username of non root user
- GROUPNAME: group name to which the non root user belongs to
You can override the default values by using build-args flag
```
### Docker buiild using override flags
```
$ docker build . ssl_scanner:2.0 --build-arg UID=5000 --build-arg GID=6000
```

## Check the available flags:
```
$ docker run --name scanner ssl_scanner:1.0 -h
usage: ssl_scan.py [-h] [-a {analyze,register}] [-n HOSTNAME] -e EMAIL
                   [-f FIRST_NAME] [-l LAST_NAME] [-o ORGANIZATION]

SSLLabs cert scanner

options:
  -h, --help            show this help message and exit
  -a {analyze,register}, --action {analyze,register}
                        which command to execute.
  -n HOSTNAME, --hostname HOSTNAME
                        Hostname to check
  -e EMAIL, --email EMAIL
                        Email address to use to fetch data
  -f FIRST_NAME, --first_name FIRST_NAME
                        First Name of user to register for API access
  -l LAST_NAME, --last_name LAST_NAME
                        Last Name of user to register for API access
  -o ORGANIZATION, --organization ORGANIZATION
                        Organization of user to register for API access

```

## Register an email to use the APIs
- The use of email services such as Gmail, Yahoo, or Hotmail not allowed.
```
docker run --rm --name scanner ssl_scanner:1.0 --email="jdoe@someoraganizationemail.com" --first_name="John" --last_name="Doe" --organization="Some Organization"
```

## Run the analysis report
- Make sure to use a valid registered email. The program will show you an error if invalid email is used.
```
docker run --rm -v /tmp:/app/reports -e REPORT_PATH=reports --name scanner ssl_scanner:1.0 --hostname="www.elliottmgmt.com" --email="jdoe@someoraganizationemail.com"
```

- -v mounts the /tmp folder on host to "reports" folder inside container
- -e flag is used if you decide to map the /tmp folder to some other directory inside container
  - "reports" is the default directory inside the working directory
- the HTML formatted report should be in /tmp folder on host

```
- The reason why I am writing to /tmp is cause the user is running as non-root and does not have access to any folder on the host filesystem except /tmp
- Another approach would have been to upload the report to S3
- Yet another approach would have been to create a folder on the host and give the UID and GID used by the docker container access to it.
- Emailing the report from within the docker container was also considered, but organizations have issues with smtp servers and they typically block those emails
    - If Emailing is necessary I would consider something like AWS SES leveraging the report in S3
```

See sample [report](report.html)