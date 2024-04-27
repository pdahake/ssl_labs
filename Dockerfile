# Use a lightweight Python image
FROM python:3.12-slim

# you can build a new image by passing different IDs
ARG UID=1000
ARG GID=3000
ARG USERNAME=appuser
ARG GROUPNAME=nonroot
ARG REPORT_PATH=reports

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV REPORT_PATH="reports"
# Install system dependencies
# add nonroot user and group
RUN apt-get update \
    && addgroup --gid $GID $GROUPNAME \
    && adduser --uid $UID --gid $GID --disabled-password $USERNAME 

#set application working directory
WORKDIR /app

# change the ownership of the working directory
RUN chown $USERNAME:$GROUPNAME /app

# Switch to the non-root user
USER $USERNAME

# Copy application files
COPY --chown=$USERNAME:$GROUPNAME src/* /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the Python script
ENTRYPOINT [ "python", "./ssl_scan.py" ]
#CMD ["--hostname", $HOSTNAME, "--email", $EMAIL, "--distribution_email", $DISTRIBUTION_EMAIL, "--first_name", $FIRST_NAME, "--last_name", $LAST_NAME, "--organization", $ORGANIZATION]