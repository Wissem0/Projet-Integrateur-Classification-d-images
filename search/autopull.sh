#!/bin/sh

REPO_OWNER="Wissem0"
REPO="Projet-Integrateur-Classification-d-images"
COMPONENT="search"

function usage {
    echo "./$(basename $0) -h : show help."    
    echo "./$(basename $0) -d : download and install neccessary components."
    echo "./$(basename $0) -s : clone/pull code if necessary and restart service."
}

function deploy {
    # Setting up environnement
    echo "sudo apt-get install git python pip"
    echo "pip install flask"
    FLASK_APP=$COMPONENT

    # Git Setup & Pull
    mkdir -p ~/service
    yes | rm -r *
    cd ~/service
    git init
    git config core.sparsecheckout true
    echo $COMPONENT >> .git/info/sparse-checkout
    git remote add -f origin https://github.com/$REPO_OWNER/$REPO
    git pull origin main
    flask run & export $FLASK_PID=$!
}

function update {   :
    L=`cd ~/service && git log --format="%H" -n 1 && cd ..`
    cd ~/service && git pull origin main && cd .. 
    N=`cd ~/service && git log --format="%H" -n 1 && cd ..`
    if [ $L = $N ]; then 
        date +"%Y-%m-%d %T : Nothing new." >> autobuild_log 
    else 
	    date +"%Y-%m-%d %T : Pulling $N" >> autobuild_log
        kill $FLASK_PID
        git pull origin main
        flask run & export $FLASK_PID=$! 
    fi
}


# list of arguments expected in the input
optstring="hds"
if [[ -z $1 ]];
then
    echo "$0: Must supply an argument."
    usage
    exit 1 
fi

while getopts ${optstring} arg; do
  case ${arg} in
    h)
        echo "Autobuild - a script to build our project."
        usage
        ;;
    d)
        deploy
        ;;
    s)
        update
        ;;        
    ?)
        usage
        exit 2
         ;;
    esac
done
