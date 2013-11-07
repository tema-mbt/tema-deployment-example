#!/bin/bash

set -e
pushd $HOME
if ! [ -d ./bin ] ; then
    mkdir -p ./bin
    export PATH=${HOME}/bin:$PATH
fi
popd
cd ..
if ! [ -e ${HOME}/bin/tema ] ; then
    git clone https://github.com/tema-tut/tema-tg.git
    pushd tema-tg
    git checkout devel
    ln -s "`pwd -P`/TemaLib/tema/tematool.py" "${HOME}/bin/tema"
    popd
fi

if ! [ -e ./tema-adapterlib ] ; then 
    git clone https://github.com/tema-tut/tema-adapterlib.git
fi

if ! [ -e ${HOME}/bin/tema.modeldesigner ] ; then
    if [ "x86_64" == `uname -p` ] ; then
	wget http://tema.cs.tut.fi/downloads/ModelDesigner-linux.gtk.x86_64.zip
	unzip ./ModelDesigner-linux.gtk.x86_64.zip
	echo "Done extracting"
    else
	wget http://tema.cs.tut.fi/downloads/ModelDesigner-linux.gtk.x86.zip
	unzip ./ModelDesigner-linux.gtk.x86.zip
	echo "Done extracting"
    fi
    cat > ./ModelDesigner/tema.modeldesigner <<EOF
#!/bin/bash
set -e

umask 007
CMD=\$(python -c "import os ; print os.path.realpath(\"\$0\")" )
WDIR=\$(dirname "\$CMD")
cd "\$WDIR"
exec ./ModelDesigner
EOF
ln -s "`pwd -P`/ModelDesigner/tema.modeldesigner" "${HOME}/bin/"
chmod u+x ./ModelDesigner/tema.modeldesigner
fi
