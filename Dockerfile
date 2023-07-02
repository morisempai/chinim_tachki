FROM ubuntu
# Install python, pip
RUN apt update && apt install -y python3 pip
# Create workdir, copy files
WORKDIR chinim_tachki
ADD ./ ./
# Install dependencies
RUN pip install -r requirements.txt

# Create non root user
RUN useradd chinim_tachki
USER chinim_tachki

EXPOSE 80
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:80", "app:app"]