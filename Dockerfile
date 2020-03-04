FROM python:3.8
MAINTAINER "ahri"<ahriknow@ahriknow.cn>
RUN apt update -y && apt install tesseract-ocr -y
ADD app.py /project/app.py
ADD Image /project/Image
ADD requirements.txt /project/requirements.txt
COPY pip.conf /etc/pip.conf
COPY ./traineddata/chi_sim.traineddata /usr/share/tessdata/
COPY ./traineddata/eng.traineddata /usr/share/tessdata/
COPY pip.conf /etc/pip.conf
WORKDIR /project
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 9000
ENTRYPOINT ["gunicorn", "-w", "2", "-b", "0.0.0.0:9000", "app:app"]
