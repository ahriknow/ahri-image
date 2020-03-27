# Ahri Image

## Get pictures through HTTP request. Custom text, graphics, colors, etc.

### [Demo https://api.ahriknow.com/image/](https://api.ahriknow.com/image/)

## Provide picture library

| 图片库名       | 图片数量 |
| -------------- | -------- |
| girl           | 4110     |
| Coming soon... | --       |

## Build the image

```Dockerfile
FROM python:3.8
MAINTAINER "ahri"<ahriknow@ahriknow.cn>
ADD app.py /project/app.py
ADD Image /project/Image
ADD requirements.txt /project/requirements.txt
COPY pip.conf /etc/pip.conf
WORKDIR /project
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 9000
ENTRYPOINT ["gunicorn", "-w", "2", "-b", "0.0.0.0:9000", "app:app"]
```

## Run a container

```bash
docker container run --name image -p 80:9000 -d ahriknow/image:v20200327
```

-   `--name image` 容器名为 image
-   `-p 80:9000` 将容器 9000 端口映射到宿主机 80 端口
-   `-d` 后台运行
-   `ahriknow/image:v20200327` 镜像

## Python requirements.txt

```py
certifi==2019.11.28
chardet==3.0.4
Click==7.0
Flask==1.1.1
gunicorn==20.0.4
idna==2.9
itsdangerous==1.1.0
Jinja2==2.11.1
MarkupSafe==1.1.1
Pillow==7.0.0
pytesseract==0.3.2
requests==2.23.0
urllib3==1.25.8
Werkzeug==1.0.0
```

## How to use

`Get http://ip:port/image/?<option>=<args>&...`

| option      | args                              | explain                                                                                 | other                            |
| ----------- | --------------------------------- | --------------------------------------------------------------------------------------- | -------------------------------- |
| width 或 w  | 100                               | 图片宽                                                                                  | 默认 400                         |
| height 或 h | 100                               | 图片高                                                                                  | 默认 300                         |
| rgb         | 100,100,100                       | RED,GREEN,BLUE                                                                          | 默认 200,200,200                 |
| lines       | 100,100,200,200,200,0,0           | 起点 x,起点 y,终点 x,终点 y,RED,GREEN,BLUE                                              | 多条线以`;`分隔                  |
| ellipses    | 300,300,400,400,150,150,150,0,0,0 | 起点 x,起点 y,终点 x,终点 y,填充 RED,填充 GREEN,填充 BLUE,边框 RED,边框 GREEN,边框 BLUE | 多个椭圆以`;`分隔                |
| rectangles  | 300,300,400,400,150,150,150,0,0,0 | 起点 x,起点 y,终点 x,终点 y,填充 RED,填充 GREEN,填充 BLUE,边框 RED,边框 GREEN,边框 BLUE | 多个矩形以`;`分隔                |
| texts       | 200,200,text,0,0,100,50           | 起点 x,起点 y,文本内容(暂时不支持包含`,`和`;`),填充 RED,填充 GREEN,填充 BLUE,字体大小   | 多个文本以`;`分隔                |
| point       | 0.5                               | 图片明暗                                                                                | point > 0                        |
| opacity     | 100                               | 图片透明度                                                                              | 0 <= opacity <= 255              |
| colour      | 2,100,100,100,200,200,200         | 渐变色方向,起始 RED,起始 GREEN,起始 BLUE,终止 RED,终止 GREEN,终止 BLUE                  | 渐变色,2:由上到下,4:由右到左     |
| store       | scenery,3                         | 图片库名,图片编号                                                                       | 不存在则默认                     |
| album       | girl,1                            | 预设图片类名,该类名图片索引                                                             | 不存在则默认                     |
| original    | true                              | 使用原图大小                                                                            | 默认 true,仅对 store、album 有效 |

## Upload to Store

`POST http://ip:port/image/upload`

| params | explain | other     |
| ------ | ------- | --------- |
| file   | image   | form-data |
| store  | 库名    |           |
| index  | 索引    |           |

## Example

-   渐变色 `https://api.ahriknow.com/image?w=600&h=400&colour=2,254,1,254,0,245,246`

    !["渐变色"](https://api.ahriknow.com/image?w=800&h=400&colour=2,254,1,254,0,245,246)

-   图片库 `https://api.ahriknow.com/image?album=girl,1`

    !["图片库"](https://api.ahriknow.com/image?album=girl,1)

## Powered By ahri 20200327
