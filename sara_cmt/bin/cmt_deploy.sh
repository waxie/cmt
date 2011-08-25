#!/bin/sh
#
#
# Author: Dennis Stam
# 
# $Id$
# $URL$

# change te permissions
perms(){
    echo "Ensuring correct permissions"
    chmod 0500 "${DESTDIR}/sara_cmt/cmt.py"
    chmod 0600 "${DESTDIR}/sara_cmt/sara_cmt/settings_db.py"
}

# create an db file when we install for the first time
create_db_file(){
    echo "Creating settings_db.py file"
    read -p "Database username, followed by [ENTER]: " db_user
    read -p "Database password, followed by [ENTER]: " db_pass

    cat > "${DESTDIR}/sara_cmt/sara_cmt/settings_db.py" <<DELIM
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sara_cmt',
        'USER': '${db_user}',
        'PASSWORD': '${db_pass}',
        'HOST': 'cmt.hpcv.sara.nl'
    }
}
DELIM

}

# create a symlink in /usr/sbin
create_link(){
    
    if [ ! -e "/usr/sbin/sara_cmt" ]
    then
        ln -s "${DESTDIR}/sara_cmt/cmt.py" /usr/sbin/sara_cmt
    else
        echo "Link/file already exists, skipping create_link step"
    fi
}

# copy the files to the destination
copy_files(){
    echo "Copying files"
    
    if [ -e "${DESTDIR}" ]
    then
        mkdir -p $DESTDIR
    fi

    echo "cp -r \"${TMPDIR}/cmt-export\" \"${DESTDIR}/sara_cmt\""
    cp -r "${TMPDIR}/cmt-export" "${DESTDIR}/sara_cmt"
    
}

get_files(){
    # exporting the svn tree
    echo "svn export -r \"${REVISION}\" --username \"${USER}\" \"${SRC_URL}\" ${TMPDIR}/cmt-export"
    svn export -r "${REVISION}" --username "${USER}" "${SRC_URL}" ${TMPDIR}/cmt-export

    # Removing the files
    echo "\n data exported from svn, removing server/development specific files:"
    echo "  ${TMPDIR}/cmt-export/doc (Available at http://cmt.hpcv.sara.nl/doc/ )"
    echo "  ${TMPDIR}/cmt-export/sara_cmt/apache"
    echo "  ${TMPDIR}/cmt-export/sara_cmt/api"
    echo "  ${TMPDIR}/cmt-export/sara_cmt/log"
    echo "  ${TMPDIR}/cmt-export/sara_cmt/fixtures"
    echo "  ${TMPDIR}/cmt-export/sara_cmt/cluster/migrations"
    echo "\n again a sleep for 2 sec"
    sleep 3
    rm -rf "${TMPDIR}/cmt-export/doc" \
        "${TMPDIR}/cmt-export/sara_cmt/apache" \
        "${TMPDIR}/cmt-export/sara_cmt/api" \
        "${TMPDIR}/cmt-export/sara_cmt/log" \
        "${TMPDIR}/cmt-export/sara_cmt/log" \
        "${TMPDIR}/cmt-export/sara_cmt/fixtures" \
        "${TMPDIR}/cmt-export/sara_cmt/cluster/migrations"
}

set_template_dir(){

    echo "Creating a template dir"
    read -p "Enter your clustername, followed by [ENTER]: " cluster

}

# A very very simple argument parser
while true
do
    case "${1}" in
        -d|--destdir)
            OPT_DEST=$2
            shift 2
        ;;
        -u|--user)
            OPT_USER=$2
            shift 2
        ;;
        -r|--revision)
            OPT_REVISION=$2
            shift 2
        ;;
        -u|--url|--src)
            OPT_SRC=$2
            shift 2
        ;;
        -t|--tmp)
            OPT_TMP=$2
            shift 2
        ;;
        *)
            break
        ;;
    esac
done

# Store the information we need, if not specified use the default value
DESTDIR="${OPT_DEST:=/opt}"
USER="${OPT_USER:=$(whoami)}"
REVISION="${OPT_REVISION:=5900}"
TMP_DEFAULT="/tmp/sara_cmt-$(tr -cd 0-9 </dev/urandom | head -c 3)"
TMPDIR="${OPT_TMP:=$TMP_DEFAULT}"
SRC_URL=${OPT_SRC:="https://subtrac.sara.nl/osd/beowulf/svn/trunk/sara_cmt"}

# CUA does not have a root login, so when someone is root ask his realname
if [ -z "${USER}" -o "x${USER}" = "xroot" ]
then
    echo "You did not specify a username or your username is root!"
    read -p "Your CUA username, followed by [ENTER]: " USER
fi

# Create the tmpdir
if [ ! -e "${TMPDIR}" ]
then
    mkdir $TMPDIR
fi

## Some information
echo "Using the following information:"
echo "  Source          : ${SRC_URL}"
echo "  Revision        : ${REVISION}"
echo "  Destination     : ${DESTDIR}"
echo "  CUA username    : ${USER}"
echo "  TMP destination : ${TMPDIR}"
echo "\n sleeping for 2 sec to allow you to read the above information!"
sleep 2

# Check if we already have an installation
if [ -e "${DESTDIR}/sara_cmt/revision" ]
then

    if [ "$(cat ${DESTDIR}/sara_cmt/revision)" = "${REVISION}" ]
    then
        echo "You already have the 'latest' version"
    else
        echo "You already have sara_cmt, backing up some files:"
        echo "  ${DESTDIR}/sara_cmt/sara_cmt/settings.py"
        echo "  ${DESTDIR}/sara_cmt/sara_cmt/settings_db.py"
        cp "${DESTDIR}/sara_cmt/sara_cmt/settings.py" "${DESTDIR}/sara_cmt/sara_cmt/settings_db.py" "${TMPDIR}/"
        rm -rf "${DESTDIR}/sara_cmt"
        get_files
        copy_files
        cp "${TMPDIR}/settings.py" "${TMPDIR}/settings_db.py" "${DESTDIR}/sara_cmt/sara_cmt/"
        perms
        create_link
        echo "${REVISION}" > "${DESTDIR}/sara_cmt/revision"
    fi
else
    get_files
    copy_files
    create_db_file
    perms
    create_link

    echo "Please adjust settings.py in ${DESTDIR}/sara_cmt/sara_cmt to the correct template directory"

    echo "${REVISION}" > "${DESTDIR}/sara_cmt/revision"
fi

## Cleaning up
rm -rf $TMPDIR


