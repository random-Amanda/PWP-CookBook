# used for testing
FROM python:3.13-alpine

WORKDIR /opt/cookbookapp
COPY . .
RUN pip install -r ../requirements.txt 
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0", "cookbookapp:create_app()"]


# # Install supervisor - new ----
# RUN apt-get update && apt-get install -y supervisor && apt-get clean 

# WORKDIR /opt/cookbookapp

# # Copy requirements first to leverage Docker cache
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy application code
# COPY .cookbookapp/ ./app/

# # Create supervisor configuration directory
# RUN mkdir -p /etc/supervisor/conf.d

# # Add supervisor configuration
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# # Create instance directory and set permissions
# RUN mkdir -p /opt/cookbookapp/instance && \
#     chgrp -R root /opt/cookbookapp && \
#     chmod -R g=u /opt/cookbookapp

# # Run supervisor instead of gunicorn directly
# CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]