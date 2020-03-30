#!/bin/sh
BASEDIR=/app
REPOSRC=https://github.com/CSSEGISandData/COVID-19.git
LOCALREPO=$BASEDIR/data

# We do it this way so that we can abstract if from just git later on
LOCALREPO_VC_DIR=$LOCALREPO/.git

if [ ! -d $LOCALREPO_VC_DIR ]
then
    git clone $REPOSRC $LOCALREPO
else
    cd $LOCALREPO
    git pull $REPOSRC
fi


# Now rsync all the submissions
GOOGLESTORAGEPATH=$BASEDIR/data/google_storage_data/
if [ ! -d $GOOGLESTORAGEPATH ]
then
	mkdir $GOOGLESTORAGEPATH
fi

gsutil rsync -r gs://covid_website_data/ $GOOGLESTORAGEPATH

python $BASEDIR/updateresults.py $GOOGLESTORAGEPATH $LOCALREPO
# End