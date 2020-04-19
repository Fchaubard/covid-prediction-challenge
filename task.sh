#!/bin/sh
BASEDIR=./
REPOSRC=https://github.com/CSSEGISandData/COVID-19.git
LOCALREPO=$BASEDIR/data/covid_truth/jhu/

# We do it this way so that we can abstract if from just git later on
LOCALREPO_VC_DIR=$LOCALREPO/.git

if [ ! -d $LOCALREPO_VC_DIR ]
then
    git clone $REPOSRC $LOCALREPO/
else
    cd $LOCALREPO
    git pull $REPOSRC
    cd -
fi

REPOSRC=https://github.com/nytimes/covid-19-data.git
LOCALREPO=$BASEDIR/data/covid_truth/nyt/

# We do it this way so that we can abstract if from just git later on
LOCALREPO_VC_DIR=$LOCALREPO/.git

if [ ! -d $LOCALREPO_VC_DIR ]
then
    git clone $REPOSRC $LOCALREPO/
else
    cd $LOCALREPO
    git pull $REPOSRC
    cd -
fi


# Now rsync all the submissions
GOOGLESTORAGEPATH=$BASEDIR/data/google_storage_data/
if [ ! -d $GOOGLESTORAGEPATH ]
then
	mkdir $GOOGLESTORAGEPATH
fi

gsutil -m rsync -r gs://covid_website_data/ $GOOGLESTORAGEPATH

python updateresults.py $BASEDIR

# End