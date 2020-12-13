FROM python:3

COPY ./init.sh .
RUN sh ./init.sh
RUN pip install \
        gaunit \
        selenium \
        browsermob-proxy
COPY ./samples .
# RUN pip install .
# CMD ["python3", "samples/home_engie_with_perf_log"]