PYTHON=python

all: pre_deps

clean:
	rm -rf dependencies/ffmpeg-0.11.2/
	rm -rf dependencies/oggvideotools-0.8a/

pre_deps: yasm sys_deps easy_install pip mimetype should_dsl specloud codecs opencv PIL ffmpeg oggVideoTools clean

sys_deps:
	sudo apt-get install g++ cmake libgd2-xpm-dev

yasm:
	sudo apt-get install yasm

easy_install:
	sudo apt-get install python-setuptools

pip:
	sudo easy_install pip

mimetype:
	sudo apt-get install libfile-mimeinfo-perl

should_dsl:
	pip install should_dsl

specloud:
	pip install specloud

codecs:
	sudo apt-get install libtheora-dbg libtheora-dev libtheora-bin libvorbis-dbg libvorbis-dev libvorbis0a libvorbisenc2 libvorbisfile3 ffmpeg2theora

opencv:
	sudo apt-get install libgtk2.0-dev libavcodec-dev libavformat-dev libjpeg62-dev libtiff4-dev libdc1394-22-dev libjasper-dev libgstreamer0.10-dev libgstreamermm-0.10-dev libswscale-dev libv4l-dev libxine-dev libunicap-dev libcv-dev libcv2.1 libcvaux-dev libcvaux2.1 libhighgui-dev libhighgui2.1 opencv-doc python-opencv

PIL:
	sudo easy_install pil

ffmpeg:
	cd dependencies/ && tar -xzvf ffmpeg-0.11.2.tar.gz
	cd dependencies/ffmpeg-0.11.2/ && ./configure --enable-libvorbis --enable-libtheora && sudo make && sudo make install
oggVideoTools:
	cd dependencies/ && tar -xzvf oggvideotools-0.8a.tar.gz
	cd dependencies/oggvideotools-0.8a && mkdir -p build
	cd dependencies/oggvideotools-0.8a/build && cmake .. && make && sudo make install
	sudo ldconfig
