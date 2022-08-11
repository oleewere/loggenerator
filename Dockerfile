FROM python:alpine3.16
ENV JSON_FORMAT=false
ENV BROKEN_JSON=false
ENV SLEEP_INTERVAL_SEC=10
ENV REPEAT_MESSAGES_BETWEEN_SLEEPS=1
ADD loggenerator.py /loggenerator.py
RUN chmod +x /loggenerator.py
RUN chown -R root:root /loggenerator.py
CMD ["python3", "/loggenerator.py"]