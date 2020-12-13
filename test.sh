BMP_VERSION=2.1.4
# wget -O browsermob-proxy.zip https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-$BMP_VERSION/browsermob-proxy-$BMP_VERSION-bin.zip
wget -N https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-$BMP_VERSION/browsermob-proxy-$BMP_VERSION-bin.zip -P ~/
unzip -q ~/browsermob-proxy-$BMP_VERSION-bin.zip -d ~/
rm ~/browsermob-proxy-$BMP_VERSION-bin.zip
mv -f ~/browsermob-proxy-$BMP_VERSION ~/browsermob-proxy


export PATH=~/browsermob-proxy/bin:$PATH