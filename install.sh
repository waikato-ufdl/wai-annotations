#!/bin/bash
#
# Script to install all the wai.annotations repos in a virtual environment

# the usage of this script
function usage()
{
   echo
   echo "${0##*/} [-v <dir>] [-p <path>] [-y] [-l] [-h]"
   echo
   echo "Installs all the wai.annotations repos in a virtual environment."
   echo
   echo " -h   this help"
   echo " -v   <dir>"
   echo "      the virtual environment directory to use, default: $VENV_DIR_DEFAULT"
   echo " -p   <path>"
   echo "      the path to the Python interpreter to use, default: $PYTHON_INTERPRETER_DEFAULT"
   echo " -y   whether to assume 'yes' for user prompts, "
   echo "      e.g., if the venv dir already exists and requires deleting"
   echo " -l   whether to install the latest, i.e., straight from the github repositories"
   echo "      rather than using the modules published on PyPI.org."
   echo
}

VENV_DIR_DEFAULT="./venv"
VENV_DIR=$VENV_DIR_DEFAULT
PYTHON_INTERPRETER_DEFAULT="/usr/bin/python3"
PYTHON_INTERPRETER=$PYTHON_INTERPRETER_DEFAULT
ASSUME_YES="no"
LATEST="no"

# interpret parameters
while getopts ":hylv:p:" flag
do
   case $flag in
      v) VENV_DIR=$OPTARG
         ;;
      p) PYTHON_INTERPRETER=$OPTARG
         ;;
      y) ASSUME_YES="yes"
         ;;
      l) LATEST="yes"
         ;;
      h) usage
         exit 0
         ;;
      *) usage
         exit 1
         ;;
   esac
done

echo
echo "wai.annotations installation"
echo "============================"

# delete venv dir
if [ -d "$VENV_DIR" ]
then
  if [ ! "$ASSUME_YES" = "yes" ]
  then
    echo
    read -n 1 -p "Virtual environment '$VENV_DIR' exists - remove (y/n)? " ANSWER
    if [ "$ANSWER" != "y" ]
    then
      echo
      echo "Keeping the virtual environment, exiting script."
      echo
      exit 0
    else
      echo
    fi
  fi
  echo
  echo "Deleting virtual environment: $VENV_DIR"
  rm -R "$VENV_DIR"
fi

PIP="$VENV_DIR/bin/pip"

# create venv
echo
echo "Creating virtual environment: $VENV_DIR"
echo
$PYTHON_INTERPRETER -m venv "$VENV_DIR"

# installing wai.annotation
echo
echo "Installing wai.annotations modules..."
echo
if [ "$LATEST" = "yes" ]
then
  "$PIP" install "numpy<1.23.0" pipdeptree
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-core.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-adams.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-audio.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-bluechannel.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-coco.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-commonvoice.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-festvox.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-generic.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-grayscale.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-imgaug.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-imgstats.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-imgvis.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-indexedpng.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-layersegments.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-opex.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-redis-predictions.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-roi.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-subdir.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-tf.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-vgg.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-video.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-voc.git
  "$PIP" install git+https://github.com/waikato-ufdl/wai-annotations-yolo.git
else
  "$PIP" install wai.annotations
fi

# done
WAIANN="$VENV_DIR/bin/wai-annotations"
if [ -f "$WAIANN" ]
then
  echo
  echo "Installation finished!"
  echo
  echo "You can now use wai.annotations directly as follows:"
  echo "  $WAIANN [options]"
  echo
  echo "Or you can activate the virtual environment using this command:"
  echo "  . $VENV_DIR/bin/activate"
  echo
  echo "And then deactivate it again with this command:"
  echo "  deactivate"
  echo
else
  echo
  echo "Installation failed, check console output!"
  echo
fi
